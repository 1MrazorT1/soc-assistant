// src/components/CveList.js

import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./CveList.css"; // (optional styling)

export default function CveList() {
  const [cves, setCves] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/cve_data.json")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to load CVE data");
        return res.json();
      })
      .then((data) => {
        setCves(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError("Error fetching CVE data");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="cve-list-page" style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
        <p>Loading CVEs…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="cve-list-page" style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
        <p style={{ color: "red" }}>{error}</p>
        <Link to="/">◀ Back to Home</Link>
      </div>
    );
  }

  return (
    <div className="cve-list-page" style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>CVE List</h1>
      <p>
        <Link to="/">◀ Back to Home</Link>
      </p>

      <table className="cve-table" style={tableStyle}>
        <thead>
          <tr>
            <th style={thStyle}>CVE ID</th>
            <th style={thStyle}>Description</th>
            <th style={thStyle}>Published Date</th>
            <th style={thStyle}>CVSS Score</th>
            <th style={thStyle}>Severity</th>
          </tr>
        </thead>
        <tbody>
          {cves.map((item) => (
            <tr key={item.cve_id}>
              <td style={tdStyle}>{item.cve_id}</td>
              <td style={tdStyle}>{item.description}</td>
              <td style={tdStyle}>{item.published_date.split("T")[0]}</td>
              <td style={tdStyle}>{item.cvss_score ?? "-"}</td>
              <td style={tdStyle}>{item.cvss_severity ?? "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const tableStyle = {
  width: "100%",
  borderCollapse: "collapse",
  marginTop: "16px",
};

const thStyle = {
  border: "1px solid #ccc",
  padding: "8px",
  backgroundColor: "#f5f5f5",
  textAlign: "left",
  fontWeight: "600",
};

const tdStyle = {
  border: "1px solid #ccc",
  padding: "8px",
  textAlign: "left",
};
