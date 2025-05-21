import React, { useState } from 'react';
import { ToggleLeft, ToggleRight, Settings, Sliders } from 'lucide-react';

interface DetectionControlsProps {
  status: string;
  onStatusChange: (status: string) => void;
}

const DetectionControls: React.FC<DetectionControlsProps> = ({ status, onStatusChange }) => {
  const [sensitivity, setSensitivity] = useState(75);
  const [threshold, setThreshold] = useState(60);
  
  // Toggle detector status
  const toggleStatus = () => {
    onStatusChange(status === 'active' ? 'inactive' : 'active');
  };
  
  return (
    <div className="space-y-6">
      {/* Status Toggle */}
      <div className="flex items-center justify-between">
        <div>
          <p className="font-medium text-gray-700">Detector Status</p>
          <p className="text-sm text-gray-500">Toggle AI wave detection</p>
        </div>
        <button onClick={toggleStatus} className="focus:outline-none">
          {status === 'active' ? (
            <ToggleRight className="h-8 w-8 text-blue-600" />
          ) : (
            <ToggleLeft className="h-8 w-8 text-gray-400" />
          )}
        </button>
      </div>
      
      {/* Divider */}
      <div className="border-t border-gray-200"></div>
      
      {/* Sensitivity Slider */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center">
            <Sliders className="h-4 w-4 text-gray-500 mr-2" />
            <p className="font-medium text-gray-700">Detection Sensitivity</p>
          </div>
          <span className="text-sm font-medium text-blue-600">{sensitivity}%</span>
        </div>
        <input
          type="range"
          min={0}
          max={100}
          value={sensitivity}
          onChange={(e) => setSensitivity(parseInt(e.target.value))}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>Low</span>
          <span>High</span>
        </div>
      </div>
      
      {/* Threshold Slider */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center">
            <Settings className="h-4 w-4 text-gray-500 mr-2" />
            <p className="font-medium text-gray-700">Alert Threshold</p>
          </div>
          <span className="text-sm font-medium text-blue-600">{threshold}%</span>
        </div>
        <input
          type="range"
          min={0}
          max={100}
          value={threshold}
          onChange={(e) => setThreshold(parseInt(e.target.value))}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>Low</span>
          <span>High</span>
        </div>
      </div>
      
      {/* Advanced Controls */}
      <button className="w-full flex items-center justify-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors">
        <Settings className="h-4 w-4 mr-2" />
        Advanced Settings
      </button>
    </div>
  );
};

export default DetectionControls;