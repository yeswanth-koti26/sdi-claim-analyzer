import React, { useState } from "react";
import FileUpload from "./components/FileUpload";
import ResultDisplay from "./components/ResultDisplay";
import "./styles/styles.css";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="app-container">
      <h1>SDI Claim Analyzer</h1>
      <FileUpload onUploadComplete={setResult} />
      {result && <ResultDisplay data={result} />}
    </div>
  );
}

export default App;
