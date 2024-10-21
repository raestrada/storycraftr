import * as vscode from 'vscode';
import { createPanel } from './panel'; // Importing the panel function

export function activate(context: vscode.ExtensionContext) {
    // Register the command that triggers the webview panel
    const disposable = vscode.commands.registerCommand('storycraftr.openPanel', () => {
        createPanel(context); // Call the createPanel function
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}
