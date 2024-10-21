{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run StoryCraftr Extension",
            "program": "${workspaceFolder}/vscode/extension.js",
            "type": "extensionHost",
            "sourceMaps": true,
            "request": "launch",
            "runtimeExecutable": "${execPath}",
            "args": [
                "--extensionDevelopmentPath=${workspaceFolder}"
            ],
            "outFiles": [
                "${workspaceFolder}/out/**/*.js"
            ],
            "preLaunchTask": "npm: compile"
        }
    ]
}
