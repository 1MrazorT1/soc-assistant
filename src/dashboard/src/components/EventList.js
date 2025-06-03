// src/components/EventList.js

import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './EventList.css'; // optional: event-specific CSS (you can also keep everything in App.css)

export default function EventList() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('/dashboard_data.json')
      .then((res) => res.json())
      .then((json) => setData(json));
  }, []);

  return (
    <div className="event-list-page">
      <h1>Threat Intelligence Dashboard</h1>
      <div className="event-list-container">
        <h2>Events / Pulses</h2>
        <table className="event-table">
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
              <tr key={event.id} className="clickable-row">
                <td>
                  {/* Wrap the Name (or entire row) in a Link so clicking navigates */}
                  <Link to={`/event/${event.id}`} className="event-link">
                    {event.name}
                  </Link>
                </td>
                <td>{event.source}</td>
                <td>{event.date}</td>
                <td>{event.ioc_count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
