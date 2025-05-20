import React, { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/Tabs";
import ManualInputSection from "./ManualInputSection";
import QuickInferenceSection from "./QuickInferenceSection";
import USGSFetchSection from "./USGSFetchSection";
import PredictionResult from "./PredictionResult";

export default function InferencePanel() {
  const [activeTab, setActiveTab] = useState("manual");
  const [result, setResult] = useState(null);
  const [summary, setSummary] = useState("");
  const [plotUrl, setPlotUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [manualInput, setManualInput] = useState(`[
  { "magnitude": 5.2, "latitude": 34.1, "longitude": -117.2, "depth": 10.0 },
  { "magnitude": 4.8, "latitude": 33.9, "longitude": -116.5, "depth": 8.0 },
  { "magnitude": 5.0, "latitude": 34.0, "longitude": -117.0, "depth": 9.5 }
]`);

  const showError = (msg) => alert(msg);
  const showSuccess = (msg) => console.log(msg);

  const handleTabChange = (value) => {
    setActiveTab(value);
    // Reset outputs on tab change
    setResult(null);
    setSummary("");
    setPlotUrl("");
    setLoading(false);
  };

  return (
    <Tabs value={activeTab} onValueChange={handleTabChange} className="space-y-6">
      <TabsList>
        <TabsTrigger value="manual">📝 Manual Entry</TabsTrigger>
        <TabsTrigger value="quick">⚡ Quick Predict</TabsTrigger>
        <TabsTrigger value="usgs">🌍 USGS Fetch</TabsTrigger>
      </TabsList>

      <TabsContent value="manual">
        <ManualInputSection
          manualInput={manualInput}
          setManualInput={setManualInput}
          setResult={setResult}
          setSummary={setSummary}
          setPlotUrl={setPlotUrl}
          loading={loading}
          setLoading={setLoading}
          showError={showError}
          showSuccess={showSuccess}
        />
        <PredictionResult result={result} summary={summary} plotUrl={plotUrl} />
      </TabsContent>

      <TabsContent value="quick">
        <QuickInferenceSection
          setResult={setResult}
          setSummary={setSummary}
          setPlotUrl={setPlotUrl}
          loading={loading}
          setLoading={setLoading}
          showError={showError}
          showSuccess={showSuccess}
        />
        <PredictionResult result={result} summary={summary} plotUrl={plotUrl} />
      </TabsContent>

      <TabsContent value="usgs">
        <USGSFetchSection
          setResult={setResult}
          setSummary={setSummary}
          setPlotUrl={setPlotUrl}
          loading={loading}
          setLoading={setLoading}
          showError={showError}
          showSuccess={showSuccess}
        />
        <PredictionResult result={result} summary={summary} plotUrl={plotUrl} />
      </TabsContent>
    </Tabs>
  );
}
