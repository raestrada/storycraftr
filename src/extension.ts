import * as vscode from "vscode";
import * as fs from "fs";
import * as path from "path";
import { exec } from "child_process";

// Function to check if Python, pipx, and StoryCraftr are installed
function checkPythonDependencies(): Promise<void> {
  return new Promise((resolve, reject) => {
    // Check if Python is installed
    exec("python3 --version", (error, stdout, stderr) => {
      if (error) {
        vscode.window.showErrorMessage(
          "Python is not installed. Please install Python.",
        );
        return reject("Python not installed");
      }

      // Check if pipx is installed
      exec("pipx --version", (error, stdout, stderr) => {
        if (error) {
          vscode.window.showWarningMessage(
            "pipx not installed, installing pipx...",
          );
          // Install pipx
          exec("python -m pip install --user pipx", (error, stdout, stderr) => {
            if (error) {
              vscode.window.showErrorMessage("Failed to install pipx.");
              return reject("Failed to install pipx");
            }

            // Ensure pipx is added to PATH
            exec("python -m pipx ensurepath", (error, stdout, stderr) => {
              if (error) {
                vscode.window.showErrorMessage("Failed to add pipx to PATH.");
                return reject("Failed to add pipx to PATH");
              }

              vscode.window.showInformationMessage(
                "pipx installed successfully.",
              );
              checkStoryCraftr(resolve, reject); // Proceed to check StoryCraftr
            });
          });
        } else {
          checkStoryCraftr(resolve, reject); // pipx already installed, check StoryCraftr
        }
      });
    });
  });
}

// Function to check if StoryCraftr is installed
function checkStoryCraftr(
  resolve: () => void,
  reject: (reason: any) => void,
): void {
  exec("pipx list", (error, stdout, stderr) => {
    if (!stdout.includes("storycraftr")) {
      vscode.window.showWarningMessage(
        "StoryCraftr not installed, installing StoryCraftr...",
      );
      exec("pipx install storycraftr", (error, stdout, stderr) => {
        if (error) {
          vscode.window.showErrorMessage("Failed to install StoryCraftr.");
          return reject("Failed to install StoryCraftr");
        }
        vscode.window.showInformationMessage(
          "StoryCraftr installed successfully.",
        );
        resolve();
      });
    } else {
      resolve();
    }
  });
}

// Function to open a StoryCraftr terminal in VS Code
function openStoryCraftrTerminal(workspaceFolder: string): void {
  const terminal = vscode.window.createTerminal("StoryCraftr");
  terminal.sendText(`storycraftr chat --book-path "${workspaceFolder}"`);
  terminal.show();
}

// Activate the extension
export function activate(context: vscode.ExtensionContext): void {
  let disposable = vscode.commands.registerCommand("storycraftr.start", () => {
    const workspaceFolders = vscode.workspace.workspaceFolders;

    if (workspaceFolders) {
      const workspaceFolder = workspaceFolders[0].uri.fsPath;
      const storyCraftrConfigPath = path.join(
        workspaceFolder,
        "storycraftr.json",
      );

      // Check if storycraftr.json exists in the root of the workspace
      if (fs.existsSync(storyCraftrConfigPath)) {
        checkPythonDependencies()
          .then(() => {
            vscode.window.showInformationMessage("Launching StoryCraftr...");
            openStoryCraftrTerminal(workspaceFolder);
          })
          .catch((err) => {
            vscode.window.showErrorMessage(`Error: ${err}`);
          });
      } else {
        vscode.window.showErrorMessage(
          "StoryCraftr is not initialized. Please ensure storycraftr.json exists in the project.",
        );
      }
    } else {
      vscode.window.showErrorMessage("No workspace folder is open.");
    }
  });

  context.subscriptions.push(disposable);
}

// Deactivate the extension
export function deactivate(): void {}
