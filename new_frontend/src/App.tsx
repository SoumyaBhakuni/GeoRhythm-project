import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import WaveDetectorPage from './pages/WaveDetectorPage';
import InferencePanel from './pages/InferencePanel';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="wave-detector" element={<WaveDetectorPage />} />
        <Route path="inference-panel" element={<InferencePanel/>} />
        
      </Route>
    </Routes>
  );
}

export default App;