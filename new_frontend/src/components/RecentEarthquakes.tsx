import React, { useState } from 'react';
import { MapPin, Clock, ArrowDown, ArrowUp } from 'lucide-react';

// Sample earthquake data
const sampleEarthquakes = [
  {
    id: 1,
    location: 'San Francisco, CA',
    coordinates: '37.7749° N, 122.4194° W',
    magnitude: 4.2,
    depth: 10.5,
    time: '2025-03-15T08:27:43Z'
  },
  {
    id: 2,
    location: 'Tokyo, Japan',
    coordinates: '35.6762° N, 139.6503° E',
    magnitude: 5.1,
    depth: 35.2,
    time: '2025-03-15T07:14:12Z'
  },
  {
    id: 3,
    location: 'Los Angeles, CA',
    coordinates: '34.0522° N, 118.2437° W',
    magnitude: 3.7,
    depth: 8.3,
    time: '2025-03-14T22:30:45Z'
  },
  {
    id: 4,
    location: 'Mexico City, Mexico',
    coordinates: '19.4326° N, 99.1332° W',
    magnitude: 4.8,
    depth: 12.7,
    time: '2025-03-14T19:15:22Z'
  },
  {
    id: 5,
    location: 'Niigata, Japan',
    coordinates: '37.7749° N, 139.0° E',
    magnitude: 6.2,
    depth: 40.1,
    time: '2025-03-14T14:05:38Z'
  },
  {
    id: 6,
    location: 'Anchorage, Alaska',
    coordinates: '61.2181° N, 149.9003° W',
    magnitude: 4.5,
    depth: 15.3,
    time: '2025-03-14T10:42:17Z'
  }
];

// Sort options
type SortOption = 'time' | 'magnitude';
type SortDirection = 'asc' | 'desc';

const RecentEarthquakes: React.FC = () => {
  const [earthquakes, setEarthquakes] = useState(sampleEarthquakes);
  const [sortBy, setSortBy] = useState<SortOption>('time');
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc');

  // Get magnitude color class based on magnitude
  const getMagnitudeColorClass = (magnitude: number) => {
    if (magnitude >= 6) return 'bg-red-500';
    if (magnitude >= 5) return 'bg-orange-500';
    if (magnitude >= 4) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  // Sort earthquakes
  const handleSort = (field: SortOption) => {
    if (sortBy === field) {
      // Toggle direction if same field
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      // New field, default to descending
      setSortBy(field);
      setSortDirection('desc');
    }
  };

  // Apply sorting
  const sortedEarthquakes = [...earthquakes].sort((a, b) => {
    if (sortBy === 'time') {
      const timeA = new Date(a.time).getTime();
      const timeB = new Date(b.time).getTime();
      return sortDirection === 'asc' ? timeA - timeB : timeB - timeA;
    } else {
      return sortDirection === 'asc' 
        ? a.magnitude - b.magnitude 
        : b.magnitude - a.magnitude;
    }
  });

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      <div className="p-6 border-b border-gray-200">
        <div className="flex justify-between items-center">
          <h3 className="text-xl font-semibold text-gray-800">Recent Earthquakes</h3>
          <div className="flex space-x-4">
            <button 
              className={`flex items-center text-sm font-medium ${sortBy === 'time' ? 'text-blue-600' : 'text-gray-500'}`}
              onClick={() => handleSort('time')}
            >
              <Clock className="h-4 w-4 mr-1" />
              Time
              {sortBy === 'time' && (
                sortDirection === 'asc' ? 
                <ArrowUp className="h-3 w-3 ml-1" /> : 
                <ArrowDown className="h-3 w-3 ml-1" />
              )}
            </button>
            <button 
              className={`flex items-center text-sm font-medium ${sortBy === 'magnitude' ? 'text-blue-600' : 'text-gray-500'}`}
              onClick={() => handleSort('magnitude')}
            >
              Magnitude
              {sortBy === 'magnitude' && (
                sortDirection === 'asc' ? 
                <ArrowUp className="h-3 w-3 ml-1" /> : 
                <ArrowDown className="h-3 w-3 ml-1" />
              )}
            </button>
          </div>
        </div>
      </div>
      
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Location</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Magnitude</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Depth</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {sortedEarthquakes.map((earthquake) => (
              <tr key={earthquake.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  <div className="flex items-start">
                    <MapPin className="h-5 w-5 text-gray-400 mr-2 mt-0.5" />
                    <div>
                      <p className="font-medium">{earthquake.location}</p>
                      <p className="text-xs text-gray-500 mt-0.5">{earthquake.coordinates}</p>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className={`w-6 h-6 rounded-full flex items-center justify-center text-white text-xs font-bold ${getMagnitudeColorClass(earthquake.magnitude)}`}>
                      {earthquake.magnitude.toFixed(1)}
                    </div>
                    <div className="ml-2">
                      <div className="h-2 w-16 bg-gray-200 rounded-full overflow-hidden">
                        <div 
                          className={`h-full ${getMagnitudeColorClass(earthquake.magnitude)}`} 
                          style={{ width: `${Math.min(earthquake.magnitude / 10 * 100, 100)}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {earthquake.depth} km
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <div className="flex items-center">
                    <Clock className="h-4 w-4 text-gray-400 mr-1" />
                    {new Date(earthquake.time).toLocaleString()}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RecentEarthquakes;