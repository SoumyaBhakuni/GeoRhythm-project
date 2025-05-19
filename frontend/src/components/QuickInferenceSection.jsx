import React, { useState } from "react";
import { Button } from "./ui/button";

export default function QuickInferenceSection({
  setResult,
  setSummary,
  setPlotUrl,
  loading,
  setLoading,
  showError,
  showSuccess,
}) {
  const [timestamp, setTimestamp] = useState(0);

  const handleMongoFetch = async () => {
    try {
      setLoading(true);
      const res = await fetch("http://localhost:5000/predict-latest");
      const data = await res.json();
      setResult(data.result);
      setSummary(data.summary);
      setPlotUrl(data.plot_url);
      showSuccess("Prediction from MongoDB successful!");
    } catch (err) {
      showError("Error fetching from MongoDB");
    } finally {
      setLoading(false);
    }
  };

  const handleStaticGenerate = async () => {
    try {
      setLoading(true);
      const res = await fetch("http://localhost:5000/generate-sample-sequence");
      const data = await res.json();
      setResult(data.result);
      setSummary(data.summary);
      setPlotUrl(data.plot_url);
      showSuccess("Static sample prediction successful!");
    } catch (err) {
      showError("Error generating sample data");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex gap-2 items-end">
        <Button onClick={handleMongoFetch} disabled={loading}>Predict from MongoDB</Button>
        <Button onClick={handleStaticGenerate} disabled={loading}>Generate Random Static Data</Button>
      </div>
    </div>
  );
}