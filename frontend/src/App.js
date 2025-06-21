// import logo from './logo.svg';
import './App.css';
import React, { useState } from "react";
import axios from "axios";

function App() {

  const [url, setUrl] = useState("");
  const [scanning, setScanning] = useState(false);
  const [message, setMessage] = useState("");
  const [vulnerabilities, setVulnerabilities] = useState([]);
  const [reportUrl, setReportUrl] = useState(null);

  const handleScan = async () => {
  setScanning(true);
  setMessage("Scanning...");
  setVulnerabilities([]);
  setReportUrl(null);

  try {
    const res = await fetch("http://localhost:8000/scan", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        target_url: url,
        max_depth: 2,
        delay: 1.0,
        mock_vulns: [
          { type: "SQL Injection", path: "/products?id=1'" },
          { type: "XSS", path: "/search?q=<script>alert(1)</script>" }
    ]
      }),
    });

    if (!res.ok) throw new Error("Scan failed");

    const blob = await res.blob();
    const fileURL = URL.createObjectURL(blob);
    setReportUrl(fileURL);

    setVulnerabilities([
      { type: "SQL Injection", path: "/products?id=1'" },
      { type: "XSS", path: "/search?q=<script>alert(1)</script>" },
    ]);
    setMessage("Scan complete.");
  } catch (err) {
    console.error(err);
    setMessage("Error running scan");
  } finally {
    setScanning(false);
  }
};
  return (

    <div className="container">
      {scanning && (
  <div style={{ margin: "20px 0" }}>
    <label>Scanning in progress...</label>
    <progress style={{ width: "100%", height: "10px" }} />
  </div>
)}


    <div style={{ padding: 40 }}>
      <h1>Web Security Scanner</h1>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter target URL"
        style={{ width: 300, marginRight: 10 }}
      />
      <button onClick={handleScan} disabled={scanning}>
        {scanning ? "Scanning..." : "Start Scan"}
      </button>
      <p>{message}</p>

      {vulnerabilities.length > 0 && (
        <div>
          <h2>Vulnerabilities Found</h2>
          <table border="1" cellPadding="5">
            <thead>
              <tr>
                <th>Type</th>
                <th>Path</th>
              </tr>
            </thead>
            <tbody>
              {vulnerabilities.map((vuln, index) => (
                <tr key={index}>
                  <td>{vuln.type}</td>
                  <td>{vuln.path}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {reportUrl && (
        <div style={{ marginTop: 20 }}>
          <a href={reportUrl} download="report.pdf">
            Download PDF Report
          </a>
        </div>
      )}
    </div>
    </div>
  );
  
}

export default App;
