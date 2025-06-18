import React from "react";
import { Link } from "react-router-dom";
import "./Home.css";

export default function Home() {
  return (
    <div className="home-page" style={pageStyle}>
      <h1 style={{ color: "#222" }}>Threat Intelligence Dashboard</h1>
      <p style={{ color: "#444" }}>Please choose what to view:</p>
      <div style={buttonContainerStyle}>
        <Link to="/events" className="button-86" role="button">
          Events / IOCs
        </Link>
        <Link to="/cves" className="button-86" role="button">
          CVEs
        </Link>
        <Link to="/malicious-urls" className="button-86" role="button">
          View Malicious URLs
        </Link>
        <Link to="/vt-check" className="button-86" role="button">
          Check a certain link
        </Link>
      </div>
    </div>
  );
}

const pageStyle = {
  textAlign: "center",
  padding: "40px",
  fontFamily: "Arial, sans-serif",
  backgroundColor: "#f4f4f4",
  minHeight: "100vh",
};

const buttonContainerStyle = {
  marginTop: "30px",
  display: "flex",
  flexWrap: "wrap",
  gap: "20px",
  justifyContent: "center",
};
