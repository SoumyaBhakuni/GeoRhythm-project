import { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
const About = () => {
  const [isVisible, setIsVisible] = useState(false);
  
  useEffect(() => {
    setIsVisible(true);
  }, []);


  const ModelSteps = () => (
    <section className="py-16" style={{ backgroundColor: '#f1f1f1' }}>
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4" style={{ color: '#5e6172' }}>Our Advanced Prediction System</h2>
          <div className="h-1 w-16 mx-auto mb-6" style={{ backgroundColor: '#f4c543' }}></div>
          <p className="text-lg max-w-3xl mx-auto" style={{ color: '#5e6172' }}>
            Our innovative machine learning model integrates multiple data sources to provide accurate and timely seismic predictions.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="p-6 rounded-lg shadow-md text-center" style={{ backgroundColor: '#dee0dc' }}>
            <div className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold" style={{ backgroundColor: 'rgba(49, 146, 68, 0.3)', color: '#5e6172' }}>1</div>
            <h3 className="font-bold mb-2" style={{ color: '#5e6172' }}>Data Integration</h3>
            <p className="text-sm" style={{ color: '#5e6172' }}>Real-time collection of seismic, geological, and satellite data from global sources</p>
          </div>
          
          <div className="p-6 rounded-lg shadow-md text-center" style={{ backgroundColor: '#dee0dc' }}>
            <div className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold" style={{ backgroundColor: 'rgba(49, 146, 68, 0.3)', color: '#5e6172' }}>2</div>
            <h3 className="font-bold mb-2" style={{ color: '#5e6172' }}>Pattern Recognition</h3>
            <p className="text-sm" style={{ color: '#5e6172' }}>Analyzing historical patterns using our proprietary deep learning algorithms</p>
          </div>
          
          <div className="p-6 rounded-lg shadow-md text-center" style={{ backgroundColor: '#dee0dc' }}>
            <div className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold" style={{ backgroundColor: 'rgba(49, 146, 68, 0.3)', color: '#5e6172' }}>3</div>
            <h3 className="font-bold mb-2" style={{ color: '#5e6172' }}>Risk Assessment</h3>
            <p className="text-sm" style={{ color: '#5e6172' }}>Generating probability maps with regional vulnerability analysis</p>
          </div>
          
          <div className="p-6 rounded-lg shadow-md text-center" style={{ backgroundColor: '#dee0dc' }}>
            <div className="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold" style={{ backgroundColor: 'rgba(49, 146, 68, 0.3)', color: '#5e6172' }}>4</div>
            <h3 className="font-bold mb-2" style={{ color: '#5e6172' }}>Emergency Response</h3>
            <p className="text-sm" style={{ color: '#5e6172' }}>Delivering critical information to communities and first responders</p>
          </div>
        </div>
      </div>
    </section>
  );
  
  
  return (
    <div>
         <Navbar />
      <div className="py-24 bg-gradient-to-r from-[#dee0dc] to-[#31924450]">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className={`text-center transition-all duration-1000 transform ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
            <h1 className="text-5xl font-bold mb-6 text-[#5e6172]">TerraAlert</h1>
            <div className="h-1 w-20 mx-auto mb-8" style={{ backgroundColor: '#f4c543' }}></div>
            <p className="text-xl max-w-3xl mx-auto text-[#5e6172] leading-relaxed mb-8">
              Pioneering the future of earthquake prediction technology with advanced AI algorithms and innovative risk assessment models.
            </p>
            <p className="text-lg max-w-2xl mx-auto text-[#5e6172] leading-relaxed mb-10">
              Our system processes seismic data to provide early warnings, potentially saving thousands of lives through proactive emergency response.
            </p>
            <div className="mt-10">
              <a 
                href="#mission" 
                className="inline-block font-bold py-3 px-6 rounded-lg transition-colors duration-300"
                style={{ backgroundColor: '#f4c543', color: '#5e6172' }}
                onMouseOver={e => e.currentTarget.style.backgroundColor = '#e0b43c'}
                onMouseOut={e => e.currentTarget.style.backgroundColor = '#f4c543'}
              >
                Discover Our Vision
              </a>
            </div>
          </div>
        </div>
      </div>
      
  
      <section id="mission" className="py-16" style={{ backgroundColor: '#fff' }}>
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col items-center">
            <div className="max-w-3xl text-center">
              <h2 className="text-3xl font-bold mb-6" style={{ color: '#5e6172' }}>Our Research Mission</h2>
              <div className="h-1 w-16 mx-auto mb-6" style={{ backgroundColor: '#f4c543' }}></div>
              <p className="mb-6 leading-relaxed" style={{ color: '#5e6172' }}>
                TerraAlert represents a breakthrough in seismic prediction technology, combining machine learning with advanced geological data analysis. Our research team has developed a comprehensive system that monitors tectonic movements to identify potential earthquake threats before they occur.
              </p>
              <p className="mb-6 leading-relaxed" style={{ color: '#5e6172' }}>
                By analyzing patterns in crustal deformation, electromagnetic signals, and historical seismic data, our platform can detect precursors to major earthquakes days or even weeks in advance. This critical time window allows communities to implement emergency protocols and potentially save thousands of lives.
              </p>
              <div className="border-l-4 p-4 italic" style={{ backgroundColor: '#dee0dc', borderColor: '#f4c543', color: '#5e6172' }}>
                "Our research indicates that predictive seismology is possible when combining multiple data streams with sophisticated AI analysis. This approach represents the future of disaster preparedness." — TerraAlert Research Team
              </div>
            </div>
          </div>
        </div>
      </section>
      
      
      <ModelSteps />
      
      
      <section className="py-16 text-white" style={{ background: 'linear-gradient(to right, #5e6172, rgba(49, 146, 68, 0.5))' }}>
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">Supporting Our Research</h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Help us advance earthquake prediction technology by participating in our pilot program. Together, we can build a safer future through innovation and collaborative research.
          </p>
          <a 
            href="#" 
            className="inline-block font-bold py-3 px-8 rounded-lg transition-colors duration-300 shadow-lg"
            style={{ backgroundColor: '#f4c543', color: '#5e6172' }}
            onMouseOver={e => e.currentTarget.style.backgroundColor = '#e0b43c'}
            onMouseOut={e => e.currentTarget.style.backgroundColor = '#f4c543'}
          >
            Learn More
          </a>
        </div>
      </section>
    </div>
  );
};

export default About;