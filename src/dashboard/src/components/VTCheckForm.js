import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function VTCheckForm() {
  const [input, setInput] = useState('');
  const [type, setType] = useState('url'); // default type
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input || !type) return;

    // Redirect to the VTDetail page with query params
    navigate(`/vt?type=${encodeURIComponent(type)}&value=${encodeURIComponent(input)}`);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Check an Indicator with VirusTotal</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Type:
          <select value={type} onChange={(e) => setType(e.target.value)} style={{ margin: '0 10px' }}>
            <option value="url">URL</option>
            <option value="domain">Domain</option>
            <option value="ip">IP Address</option>
            <option value="sha256">SHA256</option>
            <option value="md5">MD5</option>
            <option value="sha1">SHA1</option>
          </select>
        </label>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter value to check"
          style={{ margin: '0 10px', width: '300px' }}
        />
        <button type="submit">Check</button>
      </form>
    </div>
  );
}
