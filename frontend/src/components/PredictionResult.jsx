import React from "react";
import { Card, CardContent } from "@/components/ui/card";

export default function PredictionResult({ summary, plotUrl, result, plotUrls }) {
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

      {plotUrls && plotUrls.length > 0 && (
        <Card>
          <CardContent className="space-y-2">
            <h3 className="text-lg font-semibold">📊 Inference Plots</h3>
            {plotUrls.map((url, idx) => (
              <img
                key={idx}
                src={`http://localhost:5000${url}`}
                alt={`Plot ${idx + 1}`}
                className="w-full border rounded shadow"
              />
            ))}
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
