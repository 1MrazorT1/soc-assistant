// src/components/VTDetail.js
import React, { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';

export default function VTDetail() {
  const [searchParams] = useSearchParams();
  const type  = searchParams.get('type');   // example: "sha256" or "domain" or "ip"
  const value = searchParams.get('value');  // the IOC itself
  const [vtData, setVtData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!type || !value) return;
    fetch(`http://127.0.0.1:5000/api/vt?type=${encodeURIComponent(type)}&value=${encodeURIComponent(value)}`)
      .then((res) => res.json())
      .then((json) => {
        setVtData(json);
        setLoading(false);
      })
      .catch(() => {
        setVtData({ error: 'Erreur lors de l’appel à VirusTotal' });
        setLoading(false);
      });
  }, [type, value]);

  if (loading) return <p>Loading VT data…</p>;
  if (!vtData) return <p>Aucune donnée reçue.</p>;

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>VirusTotal Details</h1>
      <p>
        <strong>Type:</strong> {type} <br />
        <strong>Value:</strong> {value}
      </p>

      {vtData.error ? (
        <p style={{ color: 'red' }}>
          Erreur : {vtData.error.message || vtData.error}
        </p>
      ) : (
        <>
          <h2>Analysis Stats</h2>
          <ul>
            {vtData.last_analysis_stats
              ? Object.entries(vtData.last_analysis_stats).map(
                  ([engine, count]) => (
                    <li key={engine}>
                      {engine}: {count}
                    </li>
                  )
                )
              : <li>Aucune statistique disponible.</li>
            }
          </ul>

          <h2>Last Analysis Date</h2>
          <p>
            {vtData.last_analysis_date
              ? new Date(vtData.last_analysis_date * 1000).toLocaleString()
              : 'N/A'}
          </p>

          <h2>Categories</h2>
          <pre
            style={{
              background: '#f7f7f7',
              padding: '10px',
              borderRadius: '4px',
              maxHeight: '400px',
              overflow: 'auto'
            }}
          >
            {JSON.stringify(vtData.categories || {}, null, 2)}
          </pre>
        </>
      )}

      <p style={{ marginTop: '20px' }}>
        <Link to="/">◀ Retour à la liste des événements</Link>
      </p>
    </div>
  );
}
