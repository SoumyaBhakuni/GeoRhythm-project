import React, { useState } from 'react';
import { 
  Activity, 
  
  Clock, 
  MapPin, 
   
  Waves, 
  Gauge, 
  RefreshCw,
  Upload
} from 'lucide-react';
import WaveVisualizer from '../components/WaveVisualizer';
import IntensityChart from '../components/IntensityChart';
import AlertPanel from '../components/AlertPanel';
import DetectionControls from '../components/DetectionControls';

// Sample data (in real app, this would come from your ML backend)
const sampleData = {
  confidence: 87,
  lastUpdated: new Date().toISOString(),
  status: 'monitoring',
  detections: [
    { 
      id: 1, 
      timestamp: '2025-03-15T08:27:43Z', 
      magnitude: 4.2, 
      confidence: 92,
      location: 'Pacific Ocean, 120km NE of Tokyo',
      depth: 35,
      intensity: 'moderate',
      risk: 'low'
    },
    { 
      id: 2, 
      timestamp: '2025-03-15T07:14:12Z', 
      magnitude: 2.8, 
      confidence: 89,
      location: 'Southern California, 25km E of Los Angeles',
      depth: 12,
      intensity: 'light',
      risk: 'very low'
    }
  ]
};

const WaveDetectorPage: React.FC = () => {
  const [data, setData] = useState(sampleData);
  const [isLoading, setIsLoading] = useState(false);
  const [detectorStatus, setDetectorStatus] = useState('active');
  
  // Function to simulate loading new data (in a real app, this would fetch from your API)
  const refreshData = () => {
    setIsLoading(true);
    setTimeout(() => {
      // Simulate updated data
      setData({
        ...data,
        confidence: Math.floor(Math.random() * 10) + 85,
        lastUpdated: new Date().toISOString()
      });
      setIsLoading(false);
    }, 1500);
  };

  // Function to handle file upload (for ML model input)
  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      // In a real app, you would process the file and send it to your ML backend
      console.log('File selected:', files[0].name);
      // Simulate processing
      setIsLoading(true);
      setTimeout(() => {
        setIsLoading(false);
        // Show a simulated detection based on the upload
        const newDetection = {
          id: Date.now(),
          timestamp: new Date().toISOString(),
          magnitude: 3.1 + Math.random() * 2,
          confidence: 85 + Math.floor(Math.random() * 10),
          location: 'Uploaded data sample',
          depth: 15 + Math.floor(Math.random() * 20),
          intensity: 'moderate',
          risk: 'low'
        };
        setData({
          ...data,
          detections: [newDetection, ...data.detections]
        });
      }, 2000);
    }
  };

  return (
    <div className="pt-16 bg-slate-100 min-h-screen">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">AI Seismic Wave Detector</h1>
          <p className="text-gray-600">
            Real-time monitoring and detection of seismic waves using advanced machine learning algorithms
          </p>
        </div>

        {/* Status and Controls Panel */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Status Card */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-800">System Status</h2>
              <div className="flex items-center">
                <span className={`h-3 w-3 rounded-full mr-2 ${detectorStatus === 'active' ? 'bg-green-500' : 'bg-red-500'}`}></span>
                <span className="text-sm font-medium capitalize">{detectorStatus}</span>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-blue-50 rounded-lg p-3">
                <div className="flex items-center text-blue-700 mb-1">
                  <Activity className="h-4 w-4 mr-1" />
                  <span className="text-xs font-medium">Confidence</span>
                </div>
                <p className="text-2xl font-bold text-blue-800">{data.confidence}%</p>
              </div>
              
              <div className="bg-gray-50 rounded-lg p-3">
                <div className="flex items-center text-gray-700 mb-1">
                  <Clock className="h-4 w-4 mr-1" />
                  <span className="text-xs font-medium">Last Update</span>
                </div>
                <p className="text-sm font-medium text-gray-800">
                  {new Date(data.lastUpdated).toLocaleTimeString()}
                </p>
              </div>
            </div>
            
            <button 
              onClick={refreshData}
              disabled={isLoading}
              className="mt-4 w-full flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-blue-300"
            >
              {isLoading ? (
                <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
              ) : (
                <RefreshCw className="h-4 w-4 mr-2" />
              )}
              Refresh Data
            </button>
          </div>
          
          {/* Wave Visualizer Preview */}
          <div className="bg-white rounded-xl shadow-md p-6 lg:col-span-2">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Live Waveform</h2>
            <div className="h-32">
              <WaveVisualizer isActive={detectorStatus === 'active'} />
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Controls and Upload */}
          <div className="space-y-6">
            {/* Detection Controls */}
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Detector Controls</h2>
              <DetectionControls 
                status={detectorStatus} 
                onStatusChange={setDetectorStatus}
              />
            </div>
            
            {/* Data Upload */}
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Upload Seismic Data</h2>
              <p className="text-sm text-gray-600 mb-4">
                Upload seismic waveform data for analysis by our AI detection algorithm
              </p>
              
              <label className="block">
                <span className="sr-only">Choose file</span>
                <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md cursor-pointer hover:border-blue-500 transition-colors">
                  <div className="space-y-1 text-center">
                    <Upload className="mx-auto h-12 w-12 text-gray-400" />
                    <div className="flex text-sm text-gray-600">
                      <label htmlFor="file-upload" className="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500">
                        <span>Upload a file</span>
                        <input 
                          id="file-upload" 
                          name="file-upload" 
                          type="file" 
                          className="sr-only"
                          onChange={handleFileUpload}
                          accept=".csv,.txt,.mseed"
                        />
                      </label>
                      <p className="pl-1">or drag and drop</p>
                    </div>
                    <p className="text-xs text-gray-500">
                      CSV, TXT or MSEED up to 10MB
                    </p>
                  </div>
                </div>
              </label>
            </div>
            
            {/* Alert Panel */}
            <AlertPanel detections={data.detections} />
          </div>
          
          {/* Right Columns - Main Visualizations and Data */}
          <div className="lg:col-span-2 space-y-6">
            {/* Main Wave Visualizer */}
            <div className="bg-white rounded-xl shadow-md p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-semibold text-gray-800">Detailed Waveform Analysis</h2>
                <div className="flex items-center text-sm text-gray-500">
                  <Clock className="h-4 w-4 mr-1" />
                  <span>Real-time</span>
                </div>
              </div>
              
              <div className="h-64">
                <WaveVisualizer isActive={detectorStatus === 'active'} detailed />
              </div>
              
              <div className="mt-4 grid grid-cols-3 gap-4">
                <div className="bg-gray-50 rounded-lg p-3">
                  <div className="flex items-center text-gray-700 mb-1">
                    <Waves className="h-4 w-4 mr-1" />
                    <span className="text-xs font-medium">P-Wave</span>
                  </div>
                  <p className="text-sm font-medium text-gray-800">Detected</p>
                </div>
                
                <div className="bg-gray-50 rounded-lg p-3">
                  <div className="flex items-center text-gray-700 mb-1">
                    <Waves className="h-4 w-4 mr-1" />
                    <span className="text-xs font-medium">S-Wave</span>
                  </div>
                  <p className="text-sm font-medium text-gray-800">Analyzing</p>
                </div>
                
                <div className="bg-gray-50 rounded-lg p-3">
                  <div className="flex items-center text-gray-700 mb-1">
                    <Gauge className="h-4 w-4 mr-1" />
                    <span className="text-xs font-medium">Amplitude</span>
                  </div>
                  <p className="text-sm font-medium text-gray-800">0.35 μm</p>
                </div>
              </div>
            </div>
            
            {/* Intensity Chart */}
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Seismic Intensity Analysis</h2>
              <div className="h-80">
                <IntensityChart />
              </div>
            </div>
            
            {/* Recent Detections Table */}
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Recent Detections</h2>
              
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Location</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Magnitude</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Depth</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Confidence</th>
                      <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Risk</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {data.detections.map((detection) => (
                      <tr key={detection.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {new Date(detection.timestamp).toLocaleString()}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <MapPin className="h-4 w-4 text-gray-400 mr-1" />
                            <span className="text-sm text-gray-900">{detection.location}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            detection.magnitude > 4 ? 'bg-red-100 text-red-800' : 
                            detection.magnitude > 3 ? 'bg-yellow-100 text-yellow-800' : 
                            'bg-green-100 text-green-800'
                          }`}>
                            {detection.magnitude.toFixed(1)}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {detection.depth} km
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {detection.confidence}%
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            detection.risk === 'high' ? 'bg-red-100 text-red-800' : 
                            detection.risk === 'moderate' ? 'bg-yellow-100 text-yellow-800' : 
                            'bg-green-100 text-green-800'
                          }`}>
                            {detection.risk}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WaveDetectorPage;