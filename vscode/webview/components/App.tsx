import * as vscode from 'vscode';
import * as React from 'react';
import { useState, useEffect } from 'react';

function App() {
    const [output, setOutput] = useState<string>('');

    const sendCommand = (command: string) => {
        const vscode = acquireVsCodeApi();
        vscode.postMessage({ command: 'runCommand', text: command });
    };

    useEffect(() => {
        window.addEventListener('message', event => {
            const { result } = event.data;
            setOutput(prev => prev + result + '\n');
        });
    }, []);

    return (
        <div>
            <h1>StoryCraftr Control Panel</h1>
            <button onClick={() => sendCommand('outline general-outline "Summarize the plot"')}>
                Generate General Outline
            </button>
            <button onClick={() => sendCommand('chapters chapter 1 "Write chapter 1 based on synopsis"')}>
                Generate Chapter 1
            </button>
            <pre>{output}</pre>
        </div>
    );
}

export default App;
