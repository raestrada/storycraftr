import * as fs from "fs";
import * as path from "path";
import { TextDecoder } from "util";
import * as vscode from "vscode";

const decoder = new TextDecoder();
const TRANSCRIPT_SCHEME = "storycraftr-transcript";

interface StoryCraftrEvent {
  event: string;
  payload: Record<string, any>;
}

interface JobSummary {
  pending: number;
  running: number;
  succeeded: number;
  failed: number;
}

class TranscriptProvider implements vscode.TextDocumentContentProvider {
  private buffer = "";
  private emitter = new vscode.EventEmitter<vscode.Uri>();
  readonly uri = vscode.Uri.parse(`${TRANSCRIPT_SCHEME}:/active`);
  readonly onDidChange = this.emitter.event;

  reset() {
    this.buffer = "";
    this.emitter.fire(this.uri);
  }

  append(block: string) {
    this.buffer += block;
    this.emitter.fire(this.uri);
  }

  provideTextDocumentContent(): string {
    return this.buffer || "StoryCraftr transcript will appear here.";
  }
}

class EventStreamWatcher {
  private previousContent = "";

  constructor(
    private readonly uri: vscode.Uri,
    private readonly onEvent: (
      event: string,
      payload: Record<string, any>,
      raw: string,
    ) => void,
  ) {}

  async initialise(processExisting: boolean) {
    await this.refresh(processExisting);
  }

  async refresh(processExisting = false) {
    try {
      const data = await vscode.workspace.fs.readFile(this.uri);
      const text = decoder.decode(data);
      if (!processExisting && this.previousContent.length === 0) {
        this.previousContent = text;
        return;
      }

      if (text.length < this.previousContent.length) {
        this.previousContent = "";
      }

      const newText = text.slice(this.previousContent.length);
      this.previousContent = text;
      newText
        .split(/\r?\n/)
        .map((line) => line.trim())
        .filter(Boolean)
        .forEach((line) => {
          try {
            const parsed = JSON.parse(line) as StoryCraftrEvent;
            this.onEvent(parsed.event, parsed.payload ?? {}, line);
          } catch (err) {
            console.warn(
              `Failed to parse StoryCraftr event line (${this.uri.fsPath}):`,
              err,
            );
          }
        });
    } catch (err) {
      console.warn("Unable to read StoryCraftr event stream:", err);
    }
  }

  dispose() {
    // nothing yet
  }
}

let outputChannel: vscode.OutputChannel;
let statusItem: vscode.StatusBarItem;
const watchers = new Map<string, EventStreamWatcher>();
const disposables: vscode.Disposable[] = [];
const jobStates = new Map<string, string>();
const jobSummary: JobSummary = {
  pending: 0,
  running: 0,
  succeeded: 0,
  failed: 0,
};
let extensionContext: vscode.ExtensionContext | undefined;
let transcriptProvider: TranscriptProvider;

function getConfig<T>(key: string, fallback: T): T {
  return (
    vscode.workspace.getConfiguration("storycraftr").get<T>(key) ?? fallback
  );
}

function updateStatusBar() {
  statusItem.text = `StoryCraftr: $(rocket) ${jobSummary.running} running · ${jobSummary.pending} pending`;
  statusItem.tooltip = `Completed: ${jobSummary.succeeded}, Failed: ${jobSummary.failed}`;
  statusItem.show();
}

function resetJobSummary() {
  jobSummary.pending = 0;
  jobSummary.running = 0;
  jobSummary.succeeded = 0;
  jobSummary.failed = 0;
  jobStates.clear();
  updateStatusBar();
}

function applyJobState(jobId: string, state: string | undefined) {
  const previous = jobStates.get(jobId);
  if (previous && previous in jobSummary) {
    jobSummary[previous as keyof JobSummary] = Math.max(
      0,
      jobSummary[previous as keyof JobSummary] - 1,
    );
  }

  if (state && state in jobSummary) {
    jobSummary[state as keyof JobSummary] =
      (jobSummary[state as keyof JobSummary] ?? 0) + 1;
    jobStates.set(jobId, state);
  } else {
    jobStates.delete(jobId);
  }
  updateStatusBar();
}

async function openLog(logPath: string | undefined) {
  if (!logPath) {
    return;
  }
  try {
    const uri = vscode.Uri.file(logPath);
    const doc = await vscode.workspace.openTextDocument(uri);
    await vscode.window.showTextDocument(doc, { preview: false });
  } catch (err) {
    vscode.window.showWarningMessage(
      `Unable to open StoryCraftr log ${logPath}: ${String(err)}`,
    );
  }
}

async function handleEvent(
  event: string,
  payload: Record<string, any>,
  raw: string,
) {
  switch (event) {
    case "session.started": {
      outputChannel.appendLine("=== StoryCraftr session started ===");
      resetJobSummary();
      transcriptProvider.reset();
      if (getConfig("transcript.autoShow", true)) {
        await showTranscriptDocument();
      }
      break;
    }
    case "session.ended": {
      outputChannel.appendLine("=== StoryCraftr session ended ===");
      break;
    }
    case "chat.command": {
      const input = payload.input ?? "";
      outputChannel.appendLine(`> ${input}`);
      break;
    }
    case "chat.turn": {
      const user = payload.user ?? "";
      const answer = payload.answer ?? "";
      outputChannel.appendLine(`You: ${user}`);
      outputChannel.appendLine(`StoryCraftr:\n${answer}\n`);
      transcriptProvider.append(
        `You: ${user}\nStoryCraftr:\n${answer}\n\n`,
      );
      break;
    }
    case "sub_agent.queued":
    case "sub_agent.running":
    case "sub_agent.succeeded":
    case "sub_agent.failed": {
      const jobId = payload.job_id ?? "(unknown)";
      const role = payload.role_name ?? payload.role ?? "sub-agent";
      const command = payload.command_text ?? "";
      outputChannel.appendLine(
        `[${role}] ${command} · ${event.replace("sub_agent.", "")}`,
      );
      applyJobState(jobId, payload.status);
      if (event === "sub_agent.succeeded" || event === "sub_agent.failed") {
        const status =
          event === "sub_agent.succeeded"
            ? "completed successfully"
            : "failed";
        const message = `[${role}] ${command} ${status}`;
        const logPath = payload.log_path as string | undefined;
        const autoOpen =
          getConfig("eventStream.autoOpenLogs", true) && Boolean(logPath);
        if (autoOpen) {
          const choice = await vscode.window.showInformationMessage(
            message,
            "Open log",
            "Dismiss",
          );
          if (choice === "Open log") {
            await openLog(logPath);
          }
        } else {
          vscode.window.showInformationMessage(message);
        }
      }
      break;
    }
    case "sub_agent.logs": {
      const files = (payload.files as string[]) ?? [];
      if (!files.length) {
        vscode.window.showInformationMessage(
          "StoryCraftr log list requested but no files were provided.",
        );
        return;
      }
      const items = files.map((file) => ({
        label: path.basename(file),
        description: vscode.workspace.asRelativePath(file, false),
        file,
      }));
      const choice = await vscode.window.showQuickPick(items, {
        placeHolder: "Select a StoryCraftr log to open",
      });
      if (choice) {
        await openLog(choice.file);
      }
      break;
    }
    case "sub_agent.status": {
      const jobs = (payload.jobs as Record<string, any>[]) ?? [];
      resetJobSummary();
      for (const job of jobs) {
        const jobId = job.job_id;
        const status = job.status;
        if (jobId && status) {
          applyJobState(jobId, status);
        }
      }
      break;
    }
    default: {
      outputChannel.appendLine(`[event:${event}] ${JSON.stringify(payload)}`);
      break;
    }
  }
}

async function discoverEventStreams(
  dispatch: (
    event: string,
    payload: Record<string, any>,
    raw: string,
  ) => void,
) {
  const uris = await vscode.workspace.findFiles(
    "**/.storycraftr/vscode-events.jsonl",
  );
  for (const uri of uris) {
    attachWatcher(uri, dispatch);
  }

  const watcher = vscode.workspace.createFileSystemWatcher(
    "**/.storycraftr/vscode-events.jsonl",
  );
  extensionContext?.subscriptions.push(watcher);
  watcher.onDidCreate((uri) => attachWatcher(uri, dispatch));
  watcher.onDidChange((uri) => watchers.get(uri.fsPath)?.refresh());
}

function attachWatcher(
  uri: vscode.Uri,
  dispatch: (event: string, payload: Record<string, any>, raw: string) => void,
) {
  const key = uri.fsPath;
  if (watchers.has(key)) {
    return;
  }

  const watcher = new EventStreamWatcher(uri, dispatch);
  watchers.set(key, watcher);
  watcher.initialise(true);

  let fsWatcher: fs.FSWatcher | undefined;
  try {
    fsWatcher = fs.watch(uri.fsPath, { persistent: false }, () => {
      watcher.refresh();
    });
  } catch (err) {
    console.warn("Failed to watch StoryCraftr event stream:", err);
    watcher.dispose();
    watchers.delete(key);
    return;
  }

  const disposer = new vscode.Disposable(() => {
    fsWatcher?.close();
    watcher.dispose();
    watchers.delete(key);
  });
  disposables.push(disposer);
  extensionContext?.subscriptions.push(disposer);
}

async function showTranscriptDocument() {
  const doc = await vscode.workspace.openTextDocument(transcriptProvider.uri);
  await vscode.window.showTextDocument(doc, { preview: true });
}

function setupMarkdownWatcher() {
  const watcher = vscode.workspace.createFileSystemWatcher("**/*.md");
  const handle = (uri: vscode.Uri) => {
    void maybeOpenMarkdown(uri);
  };
  watcher.onDidCreate(handle);
  watcher.onDidChange(handle);
  extensionContext?.subscriptions.push(watcher);
}

async function maybeOpenMarkdown(uri: vscode.Uri) {
  if (uri.scheme !== "file") {
    return;
  }
  if (!getConfig("files.autoOpenMarkdown", true)) {
    return;
  }

  const fsPath = uri.fsPath;
  if (fsPath.includes(`${path.sep}.git${path.sep}`)) {
    return;
  }
  const normalized = fsPath.replace(/\\/g, "/");
  const looksInteresting =
    normalized.includes("/chapters/") ||
    normalized.includes("/storycraftr/") ||
    normalized.includes("/behaviors/");
  if (!looksInteresting) {
    return;
  }

  const alreadyVisible = vscode.window.visibleTextEditors.some(
    (editor) => editor.document.uri.fsPath === fsPath,
  );
  if (alreadyVisible) {
    return;
  }

  try {
    const doc = await vscode.workspace.openTextDocument(uri);
    await vscode.window.showTextDocument(doc, { preview: false });
  } catch (err) {
    console.warn("Unable to open markdown file:", err);
  }
}

export function activate(context: vscode.ExtensionContext) {
  extensionContext = context;
  outputChannel = vscode.window.createOutputChannel("StoryCraftr");
  statusItem = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Left,
    10,
  );
  transcriptProvider = new TranscriptProvider();

  context.subscriptions.push(
    outputChannel,
    statusItem,
    vscode.workspace.registerTextDocumentContentProvider(
      TRANSCRIPT_SCHEME,
      transcriptProvider,
    ),
    vscode.commands.registerCommand("storycraftr.showEventLog", () => {
      outputChannel.show();
    }),
  );

  updateStatusBar();
  setupMarkdownWatcher();

  void discoverEventStreams((event, payload, raw) =>
    handleEvent(event, payload, raw),
  );

  const configListener = vscode.workspace.onDidChangeConfiguration((e) => {
    if (
      e.affectsConfiguration("storycraftr.files.autoOpenMarkdown") ||
      e.affectsConfiguration("storycraftr.transcript.autoShow")
    ) {
      // values are read lazily; nothing to do
    }
  });
  context.subscriptions.push(configListener);
}

export function deactivate() {
  for (const disposable of disposables.splice(0, disposables.length)) {
    try {
      disposable.dispose();
    } catch (err) {
      console.warn("Failed to dispose StoryCraftr resource:", err);
    }
  }
  watchers.clear();
  jobStates.clear();
  extensionContext = undefined;
}
