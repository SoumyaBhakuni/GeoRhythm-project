import React, { useState } from "react";
import axios from "axios";

const API_BASE = "http://localhost:5000";

export default function InferencePanel() {
  const [jsonInput, setJsonInput] = useState("[]");
  const [summary, setSummary] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");

  const handleUSGSPredict = async () => {
    setError(""); setSummary(""); setPrediction(null);
    try {
      const res = await axios.get(`${API_BASE}/predict-latest-usgs`);
      setSummary(res.data.natural_language_summary);
      setPrediction(res.data.prediction);
    } catch (err) {
      setError(err.response?.data?.error || "Failed to fetch prediction.");
    }
  };

  const handleRandomFetch = async () => {
    setError("");
    try {
      const res = await axios.get(`${API_BASE}/fetch-random-sequence`);
      setJsonInput(JSON.stringify(res.data.sequence, null, 2));
    } catch (err) {
      setError("Failed to fetch random data.");
    }
  };

  const handleManualPredict = async () => {
    setError(""); setSummary(""); setPrediction(null);
    try {
      const input = JSON.parse(jsonInput);
      const res = await axios.post(`${API_BASE}/predict`, input);
      setSummary(res.data.natural_language_summary);
      setPrediction(res.data.prediction);
    } catch (err) {
      setError(err.response?.data?.error || "Prediction failed.");
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      {/* Form 1: Predict from USGS API */}
      <div className="p-4 border rounded-xl shadow space-y-4 bg-gray-50">
        <h2 className="text-xl font-semibold">🌍 Predict Using USGS Latest Data</h2>
        <button
          onClick={handleUSGSPredict}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Fetch & Predict from USGS
        </button>
      </div>

      {/* Form 2: User Input or Random */}
      <div className="p-4 border rounded-xl shadow space-y-4 bg-gray-50">
        <h2 className="text-xl font-semibold">📝 Manual or Random Data Prediction</h2>

        <textarea
          rows={12}
          value={jsonInput}
          onChange={(e) => setJsonInput(e.target.value)}
          className="w-full p-2 border rounded font-mono text-sm"
        />

        <div className="flex flex-wrap gap-4">
          <button
            onClick={handleManualPredict}
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          >
            Predict from Input
          </button>

          <button
            onClick={handleRandomFetch}
            className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
          >
            Fetch Random Sequence
          </button>
        </div>
      </div>

      {/* Output */}
      {(summary || error) && (
        <div className="p-4 border rounded-xl shadow bg-white mt-4">
          <h3 className="text-lg font-semibold mb-2">🧠 Prediction Summary</h3>
          {error ? (
            <p className="text-red-600">{error}</p>
          ) : (
            <>
              <pre className="whitespace-pre-wrap mb-2">{summary}</pre>
              <details className="text-sm text-gray-700">
                <summary className="cursor-pointer font-medium">View Raw Prediction JSON</summary>
                <pre className="mt-2">{JSON.stringify(prediction, null, 2)}</pre>
              </details>
            </>
          )}
        </div>
      )}
    </div>
  );
}
