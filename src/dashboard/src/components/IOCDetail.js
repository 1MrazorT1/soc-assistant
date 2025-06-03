// src/components/IOCDetail.js

import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import './IOCDetail.css'; // optional: IOC detail–specific styling

export default function IOCDetail() {
  const { id } = useParams();           // read `:id` from URL
  const [eventData, setEventData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/dashboard_data.json')
      .then((res) => res.json())
      .then((json) => {
        // find the event whose `id` matches the URL param
        const found = json.find((evt) => evt.id === id);
        setEventData(found || null);
        setLoading(false);
      });
  }, [id]);

  if (loading) {
    return (
      <div className="ioc-detail-page">
        <p>Loading...</p>
      </div>
    );
  }

  if (!eventData) {
    return (
      <div className="ioc-detail-page">
        <p>No event found with ID “{id}”.</p>
        <Link to="/">◀ Back to Events</Link>
      </div>
    );
  }

  return (
    <div className="ioc-detail-page">
      <h1>IOCs for: {eventData.name}</h1>
      <p>
        <strong>Source:</strong> {eventData.source} |{' '}
        <strong>Date:</strong> {eventData.date} |{' '}
        <strong>IOC Count:</strong> {eventData.ioc_count}
      </p>
      {eventData.iocs?.length > 0 ? (
        <table className="ioc-table">
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
            {eventData.iocs.map((ioc, index) => (
              <tr key={index}>
                <td>
                  <Link
                    to={`/vt?type=${encodeURIComponent(ioc.type)}&value=${encodeURIComponent(ioc.value)}`}
                  >
                    {ioc.value}
                  </Link>
                </td>
                <td>{ioc.type}</td>
                <td>{ioc.category || '-'}</td>
                <td>
                  {ioc.to_ids === true
                    ? '✅'
                    : ioc.to_ids === false
                    ? '❌'
                    : '-'}
                </td>
                <td>{ioc.first_seen || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No IOCs available for this event.</p>
      )}
      <p style={{ marginTop: '16px' }}>
        <Link to="/">◀ Back to Events</Link>
      </p>
    </div>
  );
}
