import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Activity, Menu, X } from 'lucide-react';

const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const navbarClasses = `fixed w-full z-50 transition-all duration-300 ${
    isScrolled ? 'bg-white shadow-md py-2' : 'bg-transparent py-4'
  }`;

  const linkClasses = (path: string) => {
    return `transition-colors duration-200 ${
      location.pathname === path
        ? 'text-blue-700 font-semibold'
        : isScrolled
        ? 'text-gray-800 hover:text-blue-600'
        : 'text-gray-800 hover:text-blue-600'
    }`;
  };

  return (
    <nav className={navbarClasses}>
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center">
          <Link to="/" className="flex items-center space-x-2">
            <Activity className="h-8 w-8 text-blue-700" />
            <span className="text-xl font-bold text-gray-900">SeismicAI</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link to="/" className={linkClasses('/')}>
              Home
            </Link>
            <Link to="/wave-detector" className={linkClasses('/wave-detector')}>
              Wave Detector
            </Link>
            
          </div>

          {/* Mobile Navigation Toggle */}
          <div className="md:hidden flex items-center">
            <button
              onClick={toggleMenu}
              className="text-gray-800 focus:outline-none"
              aria-label="Toggle Menu"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation Menu */}
        {isOpen && (
          <div className="md:hidden pt-4 pb-2 animate-fadeIn">
            <div className="flex flex-col space-y-4">
              <Link
                to="/"
                className={`${linkClasses('/')} block px-2 py-2`}
                onClick={() => setIsOpen(false)}
              >
                Home
              </Link>
              <Link
                to="/wave-detector"
                className={`${linkClasses('/wave-detector')} block px-2 py-2`}
                onClick={() => setIsOpen(false)}
              >
                Wave Detector
              </Link>
              <button
                onClick={() => setIsOpen(false)}
                className="bg-blue-700 hover:bg-blue-800 text-white px-4 py-2 rounded-md transition-colors duration-200 w-full text-left"
              >
                Get Started
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;