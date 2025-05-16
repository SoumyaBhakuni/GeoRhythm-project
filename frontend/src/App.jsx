import './App.css';
import InferencePanel from './components/InferencePanel';
import { Toaster } from 'sonner';

function App() {
  return (
    <div className="min-h-screen bg-white text-black">
      <h1 className="text-2xl text-center mt-4 font-bold">Earthquake Prediction</h1>
      <InferencePanel />
      <Toaster position="top-right" richColors />
    </div>
  );
}

export default App;
