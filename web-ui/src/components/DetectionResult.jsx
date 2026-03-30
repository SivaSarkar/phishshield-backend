import React, { useState, useEffect } from 'react';
import toast from 'react-hot-toast';

const DetectionResult = ({ result, onSubmitFeedback }) => {
  const [showDelay, setShowDelay] = useState(false);
  const [feedbackGiven, setFeedbackGiven] = useState(false);

  useEffect(() => {
    if (result?.risk_level === 'HIGH') {
      setShowDelay(true);
      const timer = setTimeout(() => setShowDelay(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [result]);

  if (!result) return null;

  const { risk_level, confidence, explanation, cognitive_score, adversarial_detected } = result;

  const riskColors = {
    HIGH: 'bg-red-100 border-red-500 text-red-800',
    MEDIUM: 'bg-yellow-100 border-yellow-500 text-yellow-800',
    LOW: 'bg-green-100 border-green-500 text-green-800'
  };

  const handleFeedback = (isSafe) => {
    if (feedbackGiven) return;
    onSubmitFeedback(result.request_id, isSafe);
    setFeedbackGiven(true);
    toast.success('Thank you for your feedback!');
  };

  return (
    <div className={`p-4 border-l-4 rounded-lg ${riskColors[risk_level]}`}>
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold">Risk Level: {risk_level}</h2>
        <span className="text-sm">Confidence: {(confidence * 100).toFixed(0)}%</span>
      </div>
      <div className="mt-2">
        <strong>Explanation:</strong>
        <ul className="list-disc list-inside mt-1">
          {explanation.map((item, i) => <li key={i}>{item}</li>)}
        </ul>
      </div>
      <div className="mt-2 text-sm text-gray-600">
        <div>Cognitive Risk Score: {cognitive_score}</div>
        <div>Adversarial Detected: {adversarial_detected ? 'Yes' : 'No'}</div>
      </div>

      {risk_level === 'HIGH' && showDelay && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl max-w-md text-center">
            <h3 className="text-2xl font-bold text-red-600 mb-4">⚠️ HIGH RISK DETECTED</h3>
            <p className="mb-4">This content appears to be a phishing attempt. Do not proceed.</p>
            <div className="animate-pulse text-gray-500 mb-4">Please wait 3 seconds...</div>
            <div className="flex gap-4 justify-center">
              <button
                onClick={() => handleFeedback(true)}
                className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
              >
                It's Safe
              </button>
              <button
                onClick={() => handleFeedback(false)}
                className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
              >
                It's Phishing
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DetectionResult;