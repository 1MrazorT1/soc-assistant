// src/App.js

import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Home          from './components/Home';
import EventList     from './components/EventList';
import IOCDetail     from './components/IOCDetail';
import VTDetail      from './components/VTDetail';
import AbuseDetail   from './components/AbuseDetail';
import CveList       from './components/CveList';
import MaliciousURLs from './components/MaliciousURLs';
import VTCheckForm from './components/VTCheckForm';

import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Landing / Selection page */}
        <Route path="/" element={<Home />} />

        {/* Events / IOCs */}
        <Route path="/events" element={<EventList />} />
        <Route path="/event/:id" element={<IOCDetail />} />

        {/* VirusTotal detail (from IOCDetail links) */}
        <Route path="/vt" element={<VTDetail />} />

        {/* AbuseIPDB detail (from IOCDetail links) */}
        <Route path="/abuse" element={<AbuseDetail />} />

        {/* CVEs page */}
        <Route path="/cves" element={<CveList />} />
        <Route path="/malicious-urls" element={<MaliciousURLs />} />
        <Route path="/vt-check" element={<VTCheckForm  />} />
        {/* Fallback: any unknown URL → Home */}
        <Route path="*" element={<Home />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
