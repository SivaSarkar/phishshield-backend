import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [inputType, setInputType] = useState('sms');
  const [content, setContent] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/detect', {
        type: inputType,
        content: content,
      });
      setResult(response.data);
    } catch (error) {
      console.error('Detection failed', error);
      setResult({ error: 'Failed to connect to backend. Is the API running?' });
    }
    setLoading(false);
  };

  return (
    <div className="App" style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>PhishShield-Lite</h1>
      <p>Enter SMS, Email, or URL to detect phishing</p>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Input Type: </label>
          <select value={inputType} onChange={(e) => setInputType(e.target.value)}>
            <option value="sms">SMS</option>
            <option value="email">Email</option>
            <option value="url">URL</option>
          </select>
        </div>
        <div>
          <label>Content: </label>
          <textarea
            rows={5}
            cols={50}
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Paste the suspicious message or URL here..."
            required
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Detect Phishing'}
        </button>
      </form>

      {result && (
        <div style={{ marginTop: '20px', border: '1px solid #ccc', padding: '15px', borderRadius: '8px' }}>
          <h2>Result</h2>
          {result.error ? (
            <p style={{ color: 'red' }}>{result.error}</p>
          ) : (
            <>
              <p><strong>Decision:</strong> <span style={{ color: result.decision === 'phishing' ? 'red' : 'green' }}>{result.decision.toUpperCase()}</span></p>
              <p><strong>Risk Score:</strong> {result.risk_score}</p>
              <p><strong>Explanation:</strong> {result.explanation.join(', ')}</p>
              <p><strong>Cognitive Risk:</strong> {result.cognitive_risk}</p>
              <p><strong>Latency:</strong> {result.latency_ms} ms</p>
              <p><strong>Request ID:</strong> {result.request_id}</p>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;