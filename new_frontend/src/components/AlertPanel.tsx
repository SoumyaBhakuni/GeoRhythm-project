import React from 'react';
import { AlertTriangle, CheckCircle2, Info } from 'lucide-react';

interface Detection {
  id: number;
  timestamp: string;
  magnitude: number;
  confidence: number;
  location: string;
  risk: string;
}

interface AlertPanelProps {
  detections: Detection[];
}

const AlertPanel: React.FC<AlertPanelProps> = ({ detections }) => {
  // Get the highest risk detection
  const getHighestRiskDetection = () => {
    if (detections.length === 0) return null;
    
    // Sort by magnitude (higher = higher risk)
    return [...detections].sort((a, b) => b.magnitude - a.magnitude)[0];
  };
  
  const highestRiskDetection = getHighestRiskDetection();
  
  // Function to determine alert status
  const getAlertStatus = () => {
    if (!highestRiskDetection) return 'normal';
    
    if (highestRiskDetection.magnitude >= 5) return 'high';
    if (highestRiskDetection.magnitude >= 4) return 'moderate';
    return 'normal';
  };
  
  const alertStatus = getAlertStatus();
  
  // Alert panel styling based on status
  const getAlertStyles = () => {
    switch (alertStatus) {
      case 'high':
        return {
          bg: 'bg-red-50',
          border: 'border-red-200',
          icon: <AlertTriangle className="h-6 w-6 text-red-500" />,
          title: 'High Alert',
          message: 'Significant seismic activity detected. Monitor closely.'
        };
      case 'moderate':
        return {
          bg: 'bg-amber-50',
          border: 'border-amber-200',
          icon: <Info className="h-6 w-6 text-amber-500" />,
          title: 'Advisory Alert',
          message: 'Moderate seismic activity detected. Stay informed.'
        };
      default:
        return {
          bg: 'bg-green-50',
          border: 'border-green-200',
          icon: <CheckCircle2 className="h-6 w-6 text-green-500" />,
          title: 'Normal Status',
          message: 'No significant seismic activity detected.'
        };
    }
  };
  
  const alertStyles = getAlertStyles();
  
  return (
    <div className={`rounded-xl shadow-md p-6 ${alertStyles.bg} border ${alertStyles.border}`}>
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Status Alert</h2>
      
      <div className="flex items-start">
        <div className="mr-3 mt-0.5">
          {alertStyles.icon}
        </div>
        <div>
          <h3 className="font-semibold text-gray-800">{alertStyles.title}</h3>
          <p className="text-gray-600 text-sm mt-1">{alertStyles.message}</p>
          
          {highestRiskDetection && alertStatus !== 'normal' && (
            <div className="mt-4 p-3 bg-white rounded-lg border border-gray-200">
              <p className="text-sm font-medium text-gray-700 mb-1">Latest Detection:</p>
              <p className="text-sm text-gray-600">{highestRiskDetection.location}</p>
              <div className="mt-2 flex justify-between items-center">
                <span className="text-sm text-gray-500">
                  Magnitude: {highestRiskDetection.magnitude.toFixed(1)}
                </span>
                <span className="text-sm text-gray-500">
                  {new Date(highestRiskDetection.timestamp).toLocaleTimeString()}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AlertPanel;