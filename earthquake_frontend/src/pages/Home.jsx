import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import Navbar from '../components/Navbar';
const Home = () => {
  const [earthquakes, setEarthquakes] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedQuake, setSelectedQuake] = useState(null);

  useEffect(() => {
  
    const mockEarthquakes = [
      {
        id: 1,
        magnitude: 5.8,
        location: "Near Tokyo, Japan",
        depth: 10.2,
        timestamp: new Date("2025-05-15T08:32:45").getTime(),
        coordinates: { lat: 35.6762, lng: 139.6503 }
      },
      {
        id: 2,
        magnitude: 4.2,
        location: "Off coast of California, USA",
        depth: 15.7,
        timestamp: new Date("2025-05-14T22:15:30").getTime(),
        coordinates: { lat: 37.7749, lng: -122.4194 }
      }
    ];
    
    setTimeout(() => {
      setEarthquakes(mockEarthquakes);
      setSelectedQuake(mockEarthquakes[0]);
      setIsLoading(false);
    }, 800);
  }, []);

  const handleQuakeSelect = (quake) => {
    setSelectedQuake(quake);
  };

  const scrollToMap = () => {
    const mapSection = document.getElementById('map-section');
    mapSection.scrollIntoView({ behavior: 'smooth' });
  };

  
  const Map = ({ earthquakes, selectedQuake, onSelectQuake }) => (
    <motion.div 
      className="bg-gradient-to-br from-[#5e6172] to-[#31924450] h-64 rounded-lg flex items-center justify-center overflow-hidden relative"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
    >
      {selectedQuake && (
        <motion.div 
          className="absolute inset-0 flex items-center justify-center"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.3, type: "spring", stiffness: 120 }}
        >
          <div className="relative">
            <div className="absolute -inset-1 rounded-full bg-[#f4c543] opacity-30 animate-ping"></div>
            <div className="absolute -inset-4 rounded-full bg-[#f4c543] opacity-20 animate-pulse"></div>
            <div className="bg-[#f4c543] h-4 w-4 rounded-full relative z-10"></div>
          </div>
        </motion.div>
      )}
      <div className="text-white text-center z-10">
        <p className="text-xl font-bold">Interactive Earthquake Map</p>
        <p className="text-sm opacity-80 mt-2">Showing {earthquakes.length} recent seismic events</p>
      </div>
      <div className="absolute inset-0 bg-[#31924450] opacity-10">
        <div className="grid grid-cols-8 grid-rows-8 h-full w-full">
          {Array(64).fill().map((_, i) => (
            <div key={i} className="border border-[#dee0dc] border-opacity-20"></div>
          ))}
        </div>
      </div>
    </motion.div>
  );

  const EarthquakeTable = ({ earthquakes, onSelectQuake }) => (
    <motion.div 
      className="mt-8 overflow-hidden shadow-lg ring-1 ring-[#5e6172]/20 rounded-lg"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
    >
      <table className="min-w-full divide-y divide-[#dee0dc]">
        <thead className="bg-[#f1f1f1]">
          <tr>
            <th className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-[#5e6172]">Magnitude</th>
            <th className="px-3 py-3.5 text-left text-sm font-semibold text-[#5e6172]">Location</th>
            <th className="px-3 py-3.5 text-left text-sm font-semibold text-[#5e6172]">Date</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-[#dee0dc] bg-white">
          {earthquakes.map((quake, index) => (
            <motion.tr 
              key={quake.id} 
              onClick={() => onSelectQuake(quake)}
              className="cursor-pointer hover:bg-[#f1f1f1] transition-colors duration-150"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
            >
              <td className="py-4 pl-4 pr-3 text-sm">
                <span className={`font-medium px-2 py-1 rounded-full text-white ${quake.magnitude >= 5 ? 'bg-[#5e6172]' : 'bg-[#f4c543]'}`}>
                  {quake.magnitude}
                </span>
              </td>
              <td className="px-3 py-4 text-sm text-[#5e6172]">{quake.location}</td>
              <td className="px-3 py-4 text-sm text-[#5e6172]">{new Date(quake.timestamp).toLocaleString()}</td>
            </motion.tr>
          ))}
        </tbody>
      </table>
    </motion.div>
  );

  return (
   
    <div className="bg-gradient-to-br from-[#f1f1f1] to-[#dee0dc]">
       <Navbar/>
      <div className="hero-section relative h-screen overflow-hidden bg-[#dee0dc]">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-[#dee0dc] to-[#31924450] z-10"></div>
          
        
          <div className="absolute inset-0 z-0">
            <motion.div 
              className="absolute w-96 h-96 rounded-full bg-[#f4c543] opacity-10"
              style={{ top: '10%', left: '5%' }}
              animate={{ 
                scale: [1, 1.2, 1],
                opacity: [0.1, 0.2, 0.1],
              }}
              transition={{ 
                repeat: Infinity,
                duration: 10,
                ease: "easeInOut" 
              }}
            />
            <motion.div 
              className="absolute w-64 h-64 rounded-full bg-[#31924450] opacity-10"
              style={{ bottom: '15%', right: '10%' }}
              animate={{ 
                scale: [1, 1.3, 1],
                opacity: [0.1, 0.15, 0.1],
              }}
              transition={{ 
                repeat: Infinity,
                duration: 8,
                ease: "easeInOut",
                delay: 1
              }}
            />
            <motion.div 
              className="absolute w-72 h-72 rounded-full bg-[#f4c543] opacity-10"
              style={{ top: '40%', right: '25%' }}
              animate={{ 
                scale: [1, 1.1, 1],
                opacity: [0.05, 0.1, 0.05],
              }}
              transition={{ 
                repeat: Infinity,
                duration: 12,
                ease: "easeInOut",
                delay: 2
              }}
            />
          </div>
        </div>

        <div className="container mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center">
          <motion.div 
            className="max-w-xl text-[#5e6172] z-20"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <motion.h1 
              className="text-4xl sm:text-5xl md:text-6xl font-bold leading-tight mb-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.3 }}
            >
              Predicting Earth's Movements
            </motion.h1>
            <motion.p 
              className="text-xl md:text-2xl mb-8 text-[#5e6172]"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.5 }}
            >
              Advanced AI-driven earthquake prediction technology to help communities prepare and stay safe.
            </motion.p>
            <motion.div 
              className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.7 }}
            >
              <motion.a 
                href="#" 
                className="bg-[#5e6172] hover:bg-[#5e6172]/90 text-white font-medium py-3 px-6 rounded-lg transition-colors duration-300 text-center shadow-lg hover:shadow-[#5e6172]/30"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Get Started
              </motion.a>
              <motion.div
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Link to="/about" className="bg-[#f4c543] hover:bg-[#f4c543]/90 text-[#5e6172] font-medium py-3 px-6 rounded-lg transition-colors duration-300 text-center shadow-lg">
                  Learn More
                </Link>
              </motion.div>
            </motion.div>
          </motion.div>
        </div>

        <motion.div 
          className="absolute bottom-10 left-1/2 transform -translate-x-1/2 text-[#5e6172] z-20"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ 
            duration: 0.5, 
            delay: 1.5,
            repeat: Infinity,
            repeatType: "reverse",
            repeatDelay: 0.5
          }}
        >
          <button 
            className="bg-[#f4c543]/20 p-3 rounded-full backdrop-blur-sm hover:bg-[#f4c543]/30 transition-colors duration-300 shadow-lg ring-1 ring-[#f4c543]/50"
            onClick={scrollToMap}
            aria-label="Scroll down"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
            </svg>
          </button>
        </motion.div>
      </div>

      {/* Recent Earthquakes Map Section */}
      <section id="map-section" className="py-20 bg-[#f1f1f1]">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            className="text-center mb-12"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            viewport={{ once: true, amount: 0.3 }}
          >
            <h2 className="text-3xl font-bold mb-4 text-[#5e6172]">Recent Earthquake Activity</h2>
            <div className="h-1 w-24 bg-[#f4c543] mx-auto mb-6 rounded-full"></div>
            <p className="text-lg text-[#5e6172] max-w-3xl mx-auto">
              Track the latest seismic events around the world with our interactive map. 
              Our AI model continuously analyzes this data to improve predictions.
            </p>
          </motion.div>

          {isLoading ? (
            <div className="flex justify-center items-center h-96">
              <div className="flex flex-col items-center">
                <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-[#5e6172]"></div>
                <p className="mt-4 text-[#5e6172]">Loading earthquake data...</p>
              </div>
            </div>
          ) : (
            <>
              <Map 
                earthquakes={earthquakes} 
                selectedQuake={selectedQuake}
                onSelectQuake={handleQuakeSelect}
              />
              
              <EarthquakeTable 
                earthquakes={earthquakes}
                onSelectQuake={handleQuakeSelect}
              />
            </>
          )}
          
          <motion.div 
            className="mt-8 text-center"
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            viewport={{ once: true }}
          >
            <motion.a 
              href="#" 
              className="inline-flex items-center text-[#5e6172] hover:text-[#5e6172]/80 font-medium"
              whileHover={{ x: 5 }}
              transition={{ type: "spring", stiffness: 400, damping: 10 }}
            >
              <span>View all earthquake data</span>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-2" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </motion.a>
          </motion.div>
        </div>
      </section>

      {/* Features Section with animation */}
      <section className="py-20 bg-gradient-to-b from-[#dee0dc] to-[#f1f1f1]">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            viewport={{ once: true, amount: 0.3 }}
          >
            <h2 className="text-3xl font-bold mb-4 text-[#5e6172]">Why TerraAlert?</h2>
            <div className="h-1 w-24 bg-[#f4c543] mx-auto mb-6 rounded-full"></div>
            <p className="text-lg text-[#5e6172] max-w-3xl mx-auto">
              Our advanced AI-powered system provides reliable earthquake predictions with unprecedented accuracy.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <motion.div 
              className="bg-white p-8 rounded-xl shadow-xl hover:shadow-2xl transition-shadow duration-300 border border-[#dee0dc]"
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              viewport={{ once: true, amount: 0.3 }}
            >
              <div className="text-[#5e6172] text-4xl mb-6 bg-[#f1f1f1] rounded-full w-16 h-16 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-3 text-[#5e6172]">AI-Powered Prediction</h3>
              <p className="text-[#5e6172]/80">
                Our machine learning algorithms analyze thousands of data points to predict seismic activity with remarkable accuracy.
              </p>
            </motion.div>
            
            <motion.div 
              className="bg-white p-8 rounded-xl shadow-xl hover:shadow-2xl transition-shadow duration-300 border border-[#dee0dc]"
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              viewport={{ once: true, amount: 0.3 }}
            >
              <div className="text-[#f4c543] text-4xl mb-6 bg-[#f1f1f1] rounded-full w-16 h-16 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-3 text-[#5e6172]">Real-Time Alerts</h3>
              <p className="text-[#5e6172]/80">
                Receive instant notifications when our system detects potential seismic activity in your area.
              </p>
            </motion.div>
            
            <motion.div 
              className="bg-white p-8 rounded-xl shadow-xl hover:shadow-2xl transition-shadow duration-300 border border-[#dee0dc]"
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.5 }}
              viewport={{ once: true, amount: 0.3 }}
            >
              <div className="text-[#31924450] text-4xl mb-6 bg-[#f1f1f1] rounded-full w-16 h-16 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-3 text-[#5e6172]">Community Safety</h3>
              <p className="text-[#5e6172]/80">
                We work with local governments and emergency services to ensure communities have time to prepare.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section with pulsing animation */}
      <section className="py-20 bg-gradient-to-r from-[#5e6172] to-[#31924450] text-white relative overflow-hidden">
        {/* Background Animation */}
        <div className="absolute inset-0 z-0">
          <motion.div 
            className="absolute top-0 left-0 w-72 h-72 bg-[#f4c543] opacity-5 rounded-full"
            animate={{ 
              x: [0, 50, 0],
              y: [0, 30, 0],
            }}
            transition={{ 
              repeat: Infinity,
              duration: 12,
              ease: "easeInOut" 
            }}
          />
          <motion.div 
            className="absolute bottom-0 right-0 w-96 h-96 bg-[#f4c543] opacity-5 rounded-full"
            animate={{ 
              x: [0, -50, 0],
              y: [0, -30, 0],
            }}
            transition={{ 
              repeat: Infinity,
              duration: 15,
              ease: "easeInOut" 
            }}
          />
        </div>

        <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          <motion.h2 
            className="text-4xl font-bold mb-4"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            viewport={{ once: true, amount: 0.3 }}
          >
            Stay Informed, Stay Safe
          </motion.h2>
          <motion.p 
            className="text-xl mb-8 max-w-xl mx-auto text-[#f1f1f1]"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.2 }}
            viewport={{ once: true, amount: 0.3 }}
          >
            Sign up for TerraAlert notifications to receive real-time updates about potential seismic activity in your area.
          </motion.p>
          <motion.form 
            className="max-w-md mx-auto flex flex-col sm:flex-row gap-4"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.4 }}
            viewport={{ once: true, amount: 0.3 }}
          >
            <input 
              type="email" 
              placeholder="Your email address" 
              className="flex-grow px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#f4c543] focus:ring-offset-2 focus:ring-offset-[#5e6172] text-[#5e6172] shadow-lg" 
              required 
              aria-label="Email address"
            />
            <motion.button 
              type="submit" 
              className="bg-[#f4c543] text-[#5e6172] font-medium px-6 py-3 rounded-lg hover:bg-[#f4c543]/90 transition-colors shadow-lg"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Subscribe
            </motion.button>
          </motion.form>
          <motion.p 
            className="mt-4 text-sm text-[#f1f1f1]"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 0.7, delay: 0.6 }}
            viewport={{ once: true }}
          >
            We'll never share your email with anyone else.
          </motion.p>
        </div>
      </section>
    </div>
  );
};

export default Home;