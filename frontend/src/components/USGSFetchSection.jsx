import React, { useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";

export default function USGSFetchSection({
  setResult,
  setSummary,
  setPlotUrl,
  loading,
  setLoading,
  showError,
  showSuccess,
}) {
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");

  const handleFetch = async () => {
    if (!startTime || !endTime) {
      showError("Please provide both start and end timestamps.");
      return;
    }
    try {
      setLoading(true);
      const response = await fetch("http://localhost:5000/predict-usgs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          source: "usgs",
          start_time: startTime,
          end_time: endTime,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        showError(errorData.error || "Error fetching data from USGS or during prediction.");
        setLoading(false);
        return;
      }

      const data = await response.json();
      setResult(data.prediction);
      setSummary(data.natural_language_summary);
      setPlotUrl(data.plot_urls || []);  // handles array of plots

      showSuccess("USGS-based prediction successful!");
    } catch (err) {
      showError("Error fetching data from USGS or during prediction.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <Label>Start Timestamp</Label>
        <Input type="datetime-local" value={startTime} onChange={(e) => setStartTime(e.target.value)} />
      </div>
      <div className="space-y-2">
        <Label>End Timestamp</Label>
        <Input type="datetime-local" value={endTime} onChange={(e) => setEndTime(e.target.value)} />
      </div>
      <Button onClick={handleFetch} disabled={loading}>
        {loading ? "Fetching & Predicting..." : "Fetch USGS Data & Predict"}
      </Button>
    </div>
  );
}
