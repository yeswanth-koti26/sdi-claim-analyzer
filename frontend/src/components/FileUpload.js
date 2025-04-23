import React, { useState } from "react";

function FileUpload({ onUploadComplete }) {
  const [claimId, setClaimId] = useState("");
  const [files, setFiles] = useState([]);

  const handleDrop = (e) => {
    e.preventDefault();
    setFiles([...e.dataTransfer.files]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!claimId || files.length === 0) {
      alert("Please enter Claim ID and drop/select files.");
      return;
    }

    const formData = new FormData();
    formData.append("claim_id", claimId);
    files.forEach(file => formData.append("files", file));

    try {
      const response = await fetch("http://127.0.0.1:8000/api/claims/analyze", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      onUploadComplete(result);
    } catch (err) {
      console.error("Upload failed", err);
      alert("Upload failed");
    }
  };

  return (
    <form className="upload-form" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Claim ID"
        value={claimId}
        onChange={(e) => setClaimId(e.target.value)}
      />

      <div
        className="drop-zone"
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
        style={{
          border: "2px dashed gray",
          padding: "20px",
          marginTop: "10px",
          marginBottom: "10px",
          textAlign: "center",
        }}
      >
        Drag and drop files here or{" "}
        <input
          type="file"
          multiple
          onChange={(e) => setFiles([...e.target.files])}
        />
      </div>

      <button type="submit">Upload & Analyze</button>
    </form>
  );
}

export default FileUpload;
