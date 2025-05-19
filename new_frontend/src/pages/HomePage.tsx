import React from 'react';
import { Link } from 'react-router-dom';
import { AlertTriangle, Activity, Search, Shield } from 'lucide-react';
import GoogleMapComponent from '../components/GoogleMapComponent';
import RecentEarthquakes from '../components/RecentEarthquakes';
import StatisticCard from '../components/StatisticCard';

const HomePage: React.FC = () => {
  return (
    <div className="pt-16">
      {/* Hero Section */}
      <section className="relative h-[90vh] flex items-center overflow-hidden">
        <div className="absolute inset-0 z-0">
          <img
            src="https://images.pexels.com/photos/1693095/pexels-photo-1693095.jpeg?auto=compress&cs=tinysrgb&w=1600"
            alt="Seismic waves background"
            className="w-full h-full object-cover object-center"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-blue-900/90 to-slate-900/70"></div>
        </div>
        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-3xl">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight">
                <span className="text-blue-400">AI Based </span>Seismic Wave Detection
            </h1>
            <p className="text-xl text-gray-200 mb-8 leading-relaxed">
              Monitor earthquakes in real-time with our cutting-edge AI technology. Get accurate predictions
              and analysis for better preparedness and response.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link
                to="/wave-detector"
                className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors duration-300 text-lg"
              >
                Open Wave Detector
              </Link>
              <a
                href="#map-section"
                className="px-8 py-3 bg-transparent border-2 border-white text-white hover:bg-white/10 rounded-lg font-medium transition-colors duration-300 text-lg"
              >
                View Earthquake Map
              </a>
            </div>
          </div>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-16 bg-gradient-to-t from-white to-transparent"></div>
      </section>

      {/* Key Statistics */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">
            Real-time Seismic Monitoring
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatisticCard
              icon={<Activity className="h-10 w-10 text-blue-600" />}
              title="Active Monitoring"
              value="24/7"
              description="Continuous seismic activity monitoring around the globe"
            />
            <StatisticCard
              icon={<AlertTriangle className="h-10 w-10 text-amber-600" />}
              title="Early Warnings"
              value="< 30 sec"
              description="Advanced warning system for potential seismic events"
            />
            <StatisticCard
              icon={<Search className="h-10 w-10 text-indigo-600" />}
              title="Detection Accuracy"
              value="99.7%"
              description="AI-powered precision in identifying seismic waves"
            />
            <StatisticCard
              icon={<Shield className="h-10 w-10 text-emerald-600" />}
              title="Global Coverage"
              value="180+"
              description="Countries with active monitoring stations"
            />
          </div>
        </div>
      </section>

      {/* Map Section */}
      <section id="map-section" className="py-16 bg-gray-100">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">Global Earthquake Map</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Visualize recent seismic activity around the world with our interactive map powered by real-time
              data from monitoring stations.
            </p>
          </div>
          <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            <div className="h-[600px]">
              <GoogleMapComponent />
            </div>
          </div>
        </div>
      </section>

      {/* Recent Earthquakes */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">Recent Seismic Activity</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Stay informed with the latest earthquake data from around the world, updated in real-time.
            </p>
          </div>
          <RecentEarthquakes />
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16 bg-gradient-to-r from-blue-900 to-indigo-900 text-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">How Our Technology Works</h2>
            <p className="text-blue-200 max-w-2xl mx-auto">
              Our AI-powered system uses advanced algorithms to detect, analyze, and predict seismic activity
              with unprecedented accuracy.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white/10 backdrop-blur-sm p-6 rounded-xl">
              <div className="bg-blue-600 w-12 h-12 rounded-full flex items-center justify-center mb-4">
                <span className="text-white font-bold text-xl">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-3">Data Collection</h3>
              <p className="text-blue-100">
                Our network of sensors continuously collects seismic data from around the world, feeding our
                system with real-time information.
              </p>
            </div>

            <div className="bg-white/10 backdrop-blur-sm p-6 rounded-xl">
              <div className="bg-blue-600 w-12 h-12 rounded-full flex items-center justify-center mb-4">
                <span className="text-white font-bold text-xl">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-3">AI Processing</h3>
              <p className="text-blue-100">
                Our advanced neural networks analyze the seismic waves, filtering noise and identifying
                patterns that indicate earthquake activity.
              </p>
            </div>

            <div className="bg-white/10 backdrop-blur-sm p-6 rounded-xl">
              <div className="bg-blue-600 w-12 h-12 rounded-full flex items-center justify-center mb-4">
                <span className="text-white font-bold text-xl">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-3">Real-time Alerts</h3>
              <p className="text-blue-100">
                Within seconds of detection, our system generates alerts with critical information about
                magnitude, location, and potential impact.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl font-bold text-gray-800 mb-6">Ready to Experience Advanced Seismic Detection?</h2>
            <p className="text-gray-600 mb-8 text-lg">
              Try our wave detector technology and see how AI can transform earthquake monitoring and early warning systems.
            </p>
            <Link
              to="/wave-detector"
              className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors duration-300 text-lg inline-block"
            >
              Open Wave Detector
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;