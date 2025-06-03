import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);

  useEffect(() => {
    fetch('/dashboard_data.json')
      .then((res) => res.json())
      .then((json) => setData(json));
  }, []);

  return (
    <div className="app">
      <h1>Threat Intelligence Dashboard</h1>
      <div className="container">
        <div className="event-list">
          <h2>Events / Pulses</h2>
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Source</th>
                <th>Date</th>
                <th>IOC Count</th>
              </tr>
            </thead>
            <tbody>
              {data.map((event) => (
                <tr key={event.id} className={selectedEvent?.id === event.id ? 'selected' : ''} onClick={() => {setSelectedEvent(event); setTimeout(() => {document.getElementById('ioc-panel')?.scrollIntoView({ behavior: 'smooth' });}, 100);}}>
                  <td>{event.name}</td>
                  <td>{event.source}</td>
                  <td>{event.date}</td>
                  <td>{event.ioc_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {selectedEvent && (
          <div id="ioc-panel" className="ioc-detail">
            <h2>IOCs for: {selectedEvent.name}</h2>
            <table>
              <thead>
                <tr>
                  <th>Value</th>
                  <th>Type</th>
                  <th>Category</th>
                  <th>To_IDs</th>
                  <th>First Seen</th>
                </tr>
              </thead>
              <tbody>
                {selectedEvent.iocs.map((ioc, index) => (
                  <tr key={index}>
                    <td>{ioc.value}</td>
                    <td>{ioc.type}</td>
                    <td>{ioc.category || '-'}</td>
                    <td>{ioc.to_ids === true ? '✅' : ioc.to_ids === false ? '❌' : '-'}</td>
                    <td>{ioc.first_seen || '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
