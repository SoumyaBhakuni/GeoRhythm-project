import React from 'react';
import { MapContainer, TileLayer,  Popup, CircleMarker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

// Sample earthquake data (can still be fetched from an API)
const sampleEarthquakes = [
  {
    id: 1,
    location: { lat: 37.7749, lng: -122.4194 },
    magnitude: 4.2,
    place: 'San Francisco, CA',
    time: '2025-03-15T08:27:43Z',
    depth: 10.5
  },
  {
    id: 2,
    location: { lat: 35.6762, lng: 139.6503 },
    magnitude: 5.1,
    place: 'Tokyo, Japan',
    time: '2025-03-15T07:14:12Z',
    depth: 35.2
  },
  {
    id: 3,
    location: { lat: 34.0522, lng: -118.2437 },
    magnitude: 3.7,
    place: 'Los Angeles, CA',
    time: '2025-03-14T22:30:45Z',
    depth: 8.3
  },
  {
    id: 4,
    location: { lat: 19.4326, lng: -99.1332 },
    magnitude: 4.8,
    place: 'Mexico City, Mexico',
    time: '2025-03-14T19:15:22Z',
    depth: 12.7
  },
  {
    id: 5,
    location: { lat: 37.7749, lng: 139.0 },
    magnitude: 6.2,
    place: 'Niigata, Japan',
    time: '2025-03-14T14:05:38Z',
    depth: 40.1
  }
];

const center = [25, 0];

const getMarkerColor = (magnitude: number) => {
  if (magnitude >= 6) return '#DC2626';
  if (magnitude >= 5) return '#F97316';
  if (magnitude >= 4) return '#FBBF24';
  if (magnitude >= 3) return '#FCD34D';
  return '#4ADE80';
};

const getMarkerSize = (magnitude: number) => {
  return Math.max(magnitude * 4, 8); // Scale as needed
};

const LeafletMapComponent: React.FC = () => {
  return (
    <div className="h-screen w-full">
      <MapContainer center={center} zoom={2} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {sampleEarthquakes.map((eq) => (
          <CircleMarker
            key={eq.id}
            center={eq.location}
            radius={getMarkerSize(eq.magnitude)}
            pathOptions={{ color: getMarkerColor(eq.magnitude), fillOpacity: 0.6 }}
            eventHandlers={{
              click: () => {
                console.log('Clicked:', eq.place);
              }
            }}
          >
            <Popup>
              <div>
                <strong>{eq.place}</strong>
                <br />
                Magnitude: {eq.magnitude}
                <br />
                Depth: {eq.depth} km
                <br />
                Time: {new Date(eq.time).toLocaleString()}
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
};

export default LeafletMapComponent;
