import React from "react";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";

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
    let parsedInput;
    try {
      parsedInput = JSON.parse(manualInput);
      if (!Array.isArray(parsedInput)) throw new Error("Input must be a JSON array.");
    } catch (parseError) {
      showError("Invalid JSON format: Please enter a valid JSON array.");
      return;
    }

    try {
      setLoading(true);
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(parsedInput), // send raw array as body
      });

      if (!response.ok) {
        const err = await response.json();
        showError(err.error || "Server returned an error.");
        setLoading(false);
        return;
      }

      const data = await response.json();

      setResult(data.prediction);
      setSummary(data.natural_language_summary);
      setPlotUrl(data.plot_url);
      showSuccess("Manual input prediction successful!");
    } catch (err) {
      showError("Server error while predicting.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
    
      <Textarea
        id="input-sequence"
        value={manualInput}
        onChange={(e) => setManualInput(e.target.value)}
        rows={8}
        spellCheck={false}
      />
      <Button onClick={handleSubmit} disabled={loading}>
        {loading ? "Predicting..." : "Run Prediction"}
      </Button>
    </div>
  );
}
