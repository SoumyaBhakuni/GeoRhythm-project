import { useState } from "react";
import axios from "axios";

const API_BASE = "http://localhost:5000";

type PredictionResponse = {
  natural_language_summary: string;
  prediction: Record<string, any>;
};

type SequenceResponse = {
  sequence: any[];
};

export default function InferencePanel() {
  const [jsonInput, setJsonInput] = useState<string>("[]");
  const [summary, setSummary] = useState<string>("");
  const [prediction, setPrediction] = useState<Record<string, any> | null>(null);
  const [error, setError] = useState<string>("");

  const handleUSGSPredict = async () => {
    setError("");
    setSummary("");
    setPrediction(null);
    try {
      const res = await axios.get<PredictionResponse>(`${API_BASE}/predict-latest-usgs`);
      setSummary(res.data.natural_language_summary);
      setPrediction(res.data.prediction);
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to fetch prediction.");
    }
  };

  const handleRandomFetch = async () => {
    setError("");
    try {
      const res = await axios.get<SequenceResponse>(`${API_BASE}/fetch-random-sequence`);
      setJsonInput(JSON.stringify(res.data.sequence, null, 2));
    } catch (err) {
      setError("Failed to fetch random data.");
    }
  };

  const handleManualPredict = async () => {
    setError("");
    setSummary("");
    setPrediction(null);
    try {
      const input = JSON.parse(jsonInput);
      const res = await axios.post<PredictionResponse>(`${API_BASE}/predict`, input);
      setSummary(res.data.natural_language_summary);
      setPrediction(res.data.prediction);
    } catch (err: any) {
      setError(err.response?.data?.error || "Prediction failed.");
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-6 py-12 space-y-10 font-sans bg-gradient-to-br from-gray-50 via-white to-blue-50 min-h-screen">
      {/* Header */}
      <h1 className="text-4xl font-extrabold text-center text-blue-800 tracking-tight">AI Inference Dashboard </h1>

      {/* USGS Prediction Section */}
      <div className="p-8 rounded-3xl bg-white/70 backdrop-blur shadow-xl border border-blue-200">
        <h2 className="text-2xl font-bold text-blue-700 mb-4">🌍 Predict Using USGS Latest Data</h2>
        <button
          onClick={handleUSGSPredict}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-semibold transition-all duration-300 shadow-md hover:shadow-lg"
        >
          Fetch & Predict from USGS
        </button>
      </div>

      {/* Manual or Random Input Section */}
      <div className="p-8 rounded-3xl bg-white/70 backdrop-blur shadow-xl border border-green-200">
        <h2 className="text-2xl font-bold text-green-700 mb-4">📝 Manual or Random Data Prediction</h2>

        <textarea
          rows={10}
          value={jsonInput}
          onChange={(e) => setJsonInput(e.target.value)}
          className="w-full p-4 border border-gray-300 rounded-xl font-mono text-sm focus:outline-none focus:ring-4 focus:ring-green-400 focus:border-transparent resize-none shadow-inner bg-gray-50"
        />

        <div className="flex flex-wrap gap-4 mt-6">
          <button
            onClick={handleManualPredict}
            className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-xl font-semibold transition-all duration-300 shadow-md hover:shadow-lg"
          >
            Predict from Input
          </button>

          <button
            onClick={handleRandomFetch}
            className="px-6 py-3 bg-gray-700 hover:bg-gray-800 text-white rounded-xl font-semibold transition-all duration-300 shadow-md hover:shadow-lg"
          >
            Fetch Random Sequence
          </button>
        </div>
      </div>

      {/* Output Section */}
      {(summary || error) && (
        <div className="p-8 rounded-3xl bg-white/80 backdrop-blur-lg shadow-xl border border-gray-200 mt-4">
          <h3 className="text-xl font-bold text-gray-800 mb-4">🧠 Prediction Summary</h3>

          {error ? (
            <p className="text-red-600 font-semibold">{error}</p>
          ) : (
            <>
              <pre className="bg-white border border-gray-300 p-4 rounded-lg whitespace-pre-wrap text-gray-800 text-sm mb-4 shadow-inner overflow-x-auto">
                {summary}
              </pre>

              <details className="text-sm text-gray-700 cursor-pointer">
                <summary className="font-semibold underline">🔍 View Raw Prediction JSON</summary>
                <pre className="bg-white border border-gray-200 mt-2 p-4 rounded-lg overflow-x-auto text-xs shadow-inner">
                  {JSON.stringify(prediction, null, 2)}
                </pre>
              </details>
            </>
          )}
        </div>
      )}
    </div>
  );
}
