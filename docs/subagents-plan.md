# Sub-Agent Execution Plan (StoryCraftr Chat)

## Objectives
- Allow authors to offload long-running StoryCraftr commands to background “sub-agents” without freezing the chat.
- Keep sub-agents fully deterministic by restricting them to StoryCraftr CLI commands (e.g., `!outline`, `!chapters`, `!iterate`, `!publish`, `!reload-files`).
- Store every role definition and log inside the project so that pipx users and source installs behave identically.

## Command Syntax (Canonical)
```
:sub-agent !command [role] [command arguments...]
```
- `!command` must be one of the chat-supported StoryCraftr commands (`!outline`, `!chapters`, `!iterate`, `!world`, `!publish`, `!reload-files`, `!characters`, `!synopsis`, etc.).
- `role` is optional; if omitted, the dispatcher auto-selects a role whose description best matches the command payload.
- Meta-commands (no background job):
  - `:sub-agent !list`
  - `:sub-agent !describe <role>`
  - `:sub-agent !status`
  - `:sub-agent !logs <role>`
  - `:sub-agent !seed [--language es|en|...]`

### Concrete Examples
- `:sub-agent !outline editor --chapter 3 --style "tight third-person"`
- `:sub-agent !chapters continuity add "Battle of Khaos" --summary "Need stronger stakes"`
- `:sub-agent !iterate marketing --scene "prologue.md" --goal "Create teaser copy"`
- `:sub-agent !publish qa --format epub --dry-run`

## Workstreams

### 1. Role Definitions & Workspace Layout
- During `storycraftr init`, scaffold `.storycraftr/subagents/<role>.yaml` plus `.storycraftr/subagents/logs/`.
- YAML schema:
  ```yaml
  name: "Continuity Editor"
  command_whitelist: ["!chapters", "!outline", "!iterate"]
  system_prompt: "...domain-specific guidance..."
  language: "en"
  persona: "Keeps POV consistent and timeline coherent."
  ```
- Provide `storycraftr sub-agents seed --language <code>` to reapply defaults or localize prompts.

### 2. Parser & Validation
- Extend the chat command parser to:
  - Recognize the `:sub-agent` prefix.
  - Assert the first token after `:sub-agent` is a valid StoryCraftr command or supported meta-command.
  - Validate the specified role exists and that the requested command sits inside the role’s whitelist.
- Return actionable errors (`Unknown role`, `Command !iterate not allowed for Research role`, etc.).

### 3. Background Job Manager
- Introduce an async job queue (thread pool runner) dedicated to sub-agent tasks.
- Job structure: `id`, `role`, `command`, `args`, `state`, `started_at`, `ended_at`, `log_path`, `stdout`, `stderr`.
- Persist job metadata inside `.storycraftr/subagents/logs/<role>/<timestamp>.json` and append markdown outputs for human review.
- Allow `:sub-agent !status` to stream queue state and `:sub-agent !logs continuity` to tail the most recent files.

### 4. LangChain Graph Alignment
- Each role instantiates a LangChain Runnable graph:
  1. Inject role system prompt + persona.
  2. Load project docs from the existing Chroma retriever (no fallbacks).
  3. Prepare the CLI command payload and invoke the corresponding StoryCraftr command pipeline.
  4. Package the output with citation metadata and save it to the job log.
- All graphs must surface retriever errors immediately; no silent degradation.

### 5. Chat Renderer Enhancements
- While a job runs, show inline badges such as `[Editor ⏳ !outline chapter 3]`.
- When finished, collapse the output inside the chat transcript with a header `[Editor ✅]` plus a link to the log file.
- Keep the main chat responsive so users can continue free-form conversation or launch more sub-agents.

### 6. Testing Matrix
- **Unit**: YAML loader, parser validation, command whitelist enforcement.
- **Integration**: Spin up two concurrent sub-agents (`editor` + `marketing`) from a sample novel and verify chat remains interactive.
- **Persistence**: Restart a chat session and confirm queued/completed jobs reload from log files.

## Success Criteria
- Users can issue `:sub-agent !iterate editor ...` while still chatting normally.
- Every sub-agent execution is traceable through log files with reproducible command payloads.
- Roles are editable per project, yet defaults remain available via `storycraftr sub-agents seed`.
