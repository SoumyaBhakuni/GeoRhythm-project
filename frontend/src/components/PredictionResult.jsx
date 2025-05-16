import React from "react";
import { Card, CardContent } from "@/components/ui/card";

export default function PredictionResult({ summary, plotUrl, result }) {
  if (!result) return null;

  return (
    <>
      {summary && (
        <Card>
          <CardContent>
            <h2 className="text-xl font-semibold text-green-700 mb-2">🧠 Prediction Summary</h2>
            <p className="text-base text-gray-800">{summary}</p>
          </CardContent>
        </Card>
      )}
      {plotUrl && (
        <Card>
          <CardContent className="space-y-2">
            <h3 className="text-lg font-semibold">📊 Sequence Plot</h3>
            <img src={plotUrl} alt="Prediction Plot" className="w-full border rounded shadow" />
          </CardContent>
        </Card>
      )}
      {result && (
        <Card>
          <CardContent>
            <h2 className="text-xl font-semibold text-gray-700 mb-2">🧾 Raw Output</h2>
            <pre className="text-sm bg-gray-100 p-4 rounded whitespace-pre-wrap">
              {JSON.stringify(result, null, 2)}
            </pre>
          </CardContent>
        </Card>
      )}
    </>
  );
}
