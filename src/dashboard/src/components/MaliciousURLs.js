// src/components/MaliciousURLs.js
import React, { useEffect, useState } from 'react';
import './EventList.css';

export default function MaliciousURLs() {
  const [urls, setUrls] = useState([]);

  useEffect(() => {
    fetch('/URLhaus_data.json')
      .then((res) => res.json())
      .then((data) => setUrls(data));
  }, []);

  return (
    <div className="event-list-page">
      <h1>Malicious URLs (from URLHaus)</h1>
      <table className="event-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>URL</th>
            <th>Threat</th>
            <th>Status</th>
            <th>Tags</th>
            <th>Last Online</th>
          </tr>
        </thead>
        <tbody>
          {urls.map((entry) => (
            <tr key={entry.id}>
              <td>{entry.id}</td>
              <td><a href={entry.url} target="_blank" rel="noopener noreferrer">{entry.url}</a></td>
              <td>{entry.threat}</td>
              <td>{entry.status}</td>
              <td>{entry.tags}</td>
              <td>{entry.last_online}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
