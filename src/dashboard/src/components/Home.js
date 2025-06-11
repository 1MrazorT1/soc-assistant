// src/components/Home.js

import React from "react";
import { Link } from "react-router-dom";
import "./Home.css";

export default function Home() {
  return (
    <div className="home-page" style={pageStyle}>
      <h1>Threat Intelligence Dashboard</h1>
      <p>Please choose what to view:</p>
      <div style={buttonContainerStyle}>
        <Link to="/events" style={buttonStyle}>
          Events / IOCs
        </Link>
        <Link to="/cves" style={buttonStyle}>
          CVEs
        </Link>
        <Link to="/malicious-urls" style={buttonStyle}>
          View Malicious URLs
        </Link>
      </div>
    </div>
  );
}

const pageStyle = {
  textAlign: "center",
  padding: "40px",
  fontFamily: "Arial, sans-serif",
};

const buttonContainerStyle = {
  marginTop: "30px",
};

const buttonStyle = {
  display: "inline-block",
  margin: "0 20px",
  padding: "15px 30px",
  backgroundColor: "#165797",
  color: "white",
  textDecoration: "none",
  borderRadius: "6px",
  fontSize: "1.1rem",
};

