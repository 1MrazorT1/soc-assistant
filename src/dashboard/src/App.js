// src/App.js

import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import EventList from './components/EventList';
import IOCDetail from './components/IOCDetail';
import VTDetail  from './components/VTDetail';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Route for the main event list */}
        <Route path="/" element={<EventList />} />

        {/* Route for IOC detail page */}
        <Route path="/event/:id" element={<IOCDetail />} />
        <Route path="/vt"        element={<VTDetail />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
