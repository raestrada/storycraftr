import * as vscode from 'vscode';
import { getNonce } from './getNonce';

// This method is called to create the webview panel
export function createPanel(context: vscode.ExtensionContext) {
    const panel = vscode.window.createWebviewPanel(
        'storycraftrPanel', // Identifies the type of the webview
        'StoryCraftr Control Panel', // Title of the panel
        vscode.ViewColumn.One, // Editor column to show the new webview panel in.
        {
            // Enable scripts in the webview
            enableScripts: true,
            localResourceRoots: [
                vscode.Uri.file(context.extensionPath)
            ]
        }
    );

    // Set the HTML content for the webview
    panel.webview.html = getWebviewContent(panel.webview, context);
    
    // Set up the message listener for communication between webview and extension
    panel.webview.onDidReceiveMessage(
        message => {
            switch (message.command) {
                case 'runCommand':
                    vscode.window.showInformationMessage(`Running command: ${message.text}`);
                    break;
            }
        },
        undefined,
        context.subscriptions
    );
}

// Function to define the HTML and load the React app from the webview folder
function getWebviewContent(webview: vscode.Webview, context: vscode.ExtensionContext): string {
    const scriptUri = webview.asWebviewUri(
        vscode.Uri.joinPath(context.extensionUri, 'webview', 'dist', 'bundle.js')
    );
    
    const nonce = getNonce();
    
    return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>StoryCraftr Panel</title>
            <script nonce="${nonce}" src="${scriptUri}"></script>
        </head>
        <body>
            <div id="root"></div>
        </body>
        </html>`;
}
