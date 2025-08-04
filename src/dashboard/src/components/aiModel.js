import React, { useState, useEffect } from 'react';
import { Link } from "react-router-dom";

export default function AiModel() {
  const [inputText, setInputText] = useState("");
  const [result, setResult] = useState(null);
  const [serverStatus, setServerStatus] = useState("Checking...");

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/status")
      .then((res) => res.ok ? res.json() : Promise.reject())
      .then(() => setServerStatus("🟢 Model is online"))
      .catch(() => setServerStatus("🔴 Model is offline"));
  }, []);


  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch("http://127.0.0.1:5000/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: inputText }),
    });
    const data = await res.json();
    setResult(data);
  };

  return (
    <div style={{ padding: "30px" }}>
      <h2>Analyze with AI</h2>
      <p><strong>Status:</strong> {serverStatus}</p>
      <form onSubmit={handleSubmit}>
        <textarea
          rows="6"
          style={{ width: "100%", fontSize: "16px" }}
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Paste your threat report or text here..."
        />
        <br />
        <button type="submit" style={{ marginTop: "10px" }}>Analyze</button>
      </form>
      <p><Link to="/">◀ Back to Home</Link></p>

      {result && (
         <div style={{ marginTop: "20px" }}>
           <h3>Extracted Entities:</h3>
           <ul>
             {result.entities.map((ent, i) => (
               <li key={i}>
                 <strong>{ent.text}</strong> — <em>{ent.label}</em>
               </li>
             ))}
           </ul>
         </div>
        )}
    </div>
  );
}
