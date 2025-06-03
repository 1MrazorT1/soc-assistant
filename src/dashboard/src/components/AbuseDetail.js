// src/components/AbuseDetail.js

import React, { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';

export default function AbuseDetail() {
  const [searchParams] = useSearchParams();
  const ip = searchParams.get('ip');    // ex: "8.8.8.8"
  const [abuseData, setAbuseData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!ip) return;
    fetch(`http://127.0.0.1:5001/api/abuse?ip=${encodeURIComponent(ip)}`)
      .then((res) => res.json())
      .then((json) => {
        setAbuseData(json);
        setLoading(false);
      })
      .catch(() => {
        setAbuseData({ error: 'Erreur lors de l’appel à AbuseIPDB' });
        setLoading(false);
      });
  }, [ip]);

  if (loading) return <p>Loading AbuseIPDB data…</p>;
  if (!abuseData) return <p>Aucune donnée reçue.</p>;

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>AbuseIPDB Details</h1>
      <p>
        <strong>IP:</strong> {ip}
      </p>

      {abuseData.error ? (
        <p style={{ color: 'red' }}>
          Erreur : {abuseData.error.message || abuseData.error}
        </p>
      ) : (
        <>
          <h2>Abuse Confidence Score</h2>
          <p>{abuseData.data?.abuseConfidenceScore ?? 'N/A'}</p>

          <h2>Country & ISP</h2>
          <p>
            {abuseData.data?.countryCode ?? '—'} |{' '}
            {abuseData.data?.isp ?? '—'}
          </p>

          <h2>Usage Type</h2>
          <p>{abuseData.data?.usageType ?? '—'}</p>

          {/* You can display more fields as needed: */}
          {/* {abuseData.data?.lastReportedAt && (
                <p><strong>Last Reported At:</strong> {abuseData.data.lastReportedAt}</p>
              )} */}
        </>
      )}

      <p style={{ marginTop: '20px' }}>
        <Link to="/">◀ Retour à la liste des événements</Link>
      </p>
    </div>
  );
}
