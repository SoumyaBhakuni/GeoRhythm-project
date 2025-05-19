import React from "react";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import Label from "./ui/label";
export default function ManualInputSection({
  manualInput,
  setManualInput,
  setResult,
  setSummary,
  setPlotUrl,
  loading,
  setLoading,
  showError,
  showSuccess,
}) {
  const handleSubmit = async () => {
    try {
      setLoading(true);
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source: "manual", sequence: JSON.parse(manualInput) }),
      });

      const data = await response.json();
      setResult(data.result);
      setSummary(data.summary);
      setPlotUrl(data.plot_url);
      showSuccess("Manual input prediction successful!");
    } catch (err) {
      showError("Invalid input format or server error.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <Label htmlFor="input-sequence">Enter Sequence Data (JSON format)</Label>
      <Textarea
        id="input-sequence"
        value={manualInput}
        onChange={(e) => setManualInput(e.target.value)}
        rows={8}
      />
      <Button onClick={handleSubmit} disabled={loading}>
        {loading ? "Predicting..." : "Run Prediction"}
      </Button>
    </div>
  );
}