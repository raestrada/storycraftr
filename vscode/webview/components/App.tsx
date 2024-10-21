import * as React from "react";

interface vscode {
  postMessage(message: any): void;
}
declare const vscode: vscode;

const sendMessage = () => {
  console.log("button clicked");
  vscode.postMessage({ command: "testing" });
};

const App = () => {
  const [buttonText, setButtonText] = React.useState("The brain is pending");

  React.useEffect(() => {
    window.addEventListener("message", (event) => {
      const message = event.data; // The json data that the extension sent
      switch (message.command) {
        case "refactor":
          setButtonText("The brain is working");
          break;
      }
    });
  });

  return (
    <div>
      <h1>Functional Components Work!</h1>
      <button onClick={sendMessage}>{buttonText}</button>
    </div>
  );
};

export default App;
