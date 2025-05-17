import { useState } from 'react';

const Navbar = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <nav style={{ backgroundColor: '#5e6172' }} className="py-4 px-6 shadow-md sticky top-0 z-50">
      <div className="container mx-auto flex justify-between items-center">
     
        <div className="text-xl font-bold" style={{ color: '#f4c543' }}>
          TerraAlert
        </div>

        <div className="hidden md:flex space-x-8">
          <a href="/" className="font-medium hover:opacity-80 transition-opacity" style={{ color: '#f1f1f1' }}>
            Home
          </a>
          <a href="/about" className="font-medium hover:opacity-80 transition-opacity" style={{ color: '#f4c543', borderBottom: '2px solid #f4c543' }}>
            About
          </a>
        </div>

        <div className="md:hidden">
          <button 
            onClick={toggleMenu}
            className="p-2 rounded focus:outline-none"
            style={{ color: '#f4c543' }}
          >
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              className="h-6 w-6" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              {menuOpen ? (
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M6 18L18 6M6 6l12 12" 
                />
              ) : (
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M4 6h16M4 12h16M4 18h16" 
                />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Navigation */}
      {menuOpen && (
        <div className="md:hidden pt-4 pb-2" style={{ backgroundColor: '#5e6172' }}>
          <div className="flex flex-col space-y-3 px-4">
            <a 
              href="/" 
              className="font-medium py-2 px-3 rounded hover:bg-opacity-10 hover:bg-white"
              style={{ color: '#f1f1f1' }}
            >
              Home
            </a>
            <a 
              href="/about" 
              className="font-medium py-2 px-3 rounded"
              style={{ backgroundColor: 'rgba(244, 197, 67, 0.2)', color: '#f4c543' }}
            >
              About
            </a>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar