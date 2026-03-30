// App.js (simplified)
import React, { useState } from 'react';
import axios from 'axios';
import DetectionResult from './components/DetectionResult';
import toast, { Toaster } from 'react-hot-toast';

function App() {
  const [input, setInput] = useState('');
  const [type, setType] = useState('sms');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const detect = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/detect', {
        type,
        content: input
      });
      setResult(response.data);
    } catch (error) {
      toast.error('Detection failed');
    } finally {
      setLoading(false);
    }
  };

  const sendFeedback = async (requestId, isSafe) => {
    try {
      await axios.post('http://localhost:8000/feedback', {
        request_id: requestId,
        feedback_label: isSafe ? 'safe' : 'phishing'
      });
    } catch (error) {
      toast.error('Feedback could not be sent');
    }
  };

  return (
    <div className="container mx-auto p-4">
      <Toaster />
      <h1 className="text-2xl font-bold mb-4">PhishShield-Lite</h1>
      <div className="mb-4">
        <select value={type} onChange={e => setType(e.target.value)} className="border p-2 rounded mr-2">
          <option value="sms">SMS</option>
          <option value="email">Email</option>
          <option value="url">URL</option>
        </select>
        <textarea
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Enter SMS, email or URL"
          rows="4"
          className="border p-2 rounded w-full"
        />
        <button
          onClick={detect}
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded mt-2 disabled:opacity-50"
        >
          {loading ? 'Detecting...' : 'Detect'}
        </button>
      </div>
      {result && <DetectionResult result={result} onSubmitFeedback={sendFeedback} />}
    </div>
  );
}

export default App;