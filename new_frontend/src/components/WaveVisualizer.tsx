import React, { useEffect, useRef } from 'react';

interface WaveVisualizerProps {
  isActive: boolean;
  detailed?: boolean;
}

const WaveVisualizer: React.FC<WaveVisualizerProps> = ({ isActive, detailed = false }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationFrameRef = useRef<number>(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas dimensions
    const resizeCanvas = () => {
      const parent = canvas.parentElement;
      if (parent) {
        canvas.width = parent.clientWidth;
        canvas.height = parent.clientHeight;
      }
    };

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Wave parameters
    let offset = 0;
    const waveCount = detailed ? 3 : 1;
    const waves = Array(waveCount).fill(0).map((_, i) => ({
      amplitude: detailed ? (i === 0 ? 15 : i === 1 ? 10 : 5) : 15,
      frequency: detailed ? (i === 0 ? 0.02 : i === 1 ? 0.04 : 0.01) : 0.02,
      speed: detailed ? (i === 0 ? 0.1 : i === 1 ? 0.05 : 0.15) : 0.1,
      color: detailed ? 
        (i === 0 ? '#1E40AF' : i === 1 ? '#3B82F6' : '#93C5FD') : 
        '#3B82F6',
      offset: 0
    }));

    // Draw wave function
    const drawWave = () => {
      if (!ctx || !canvas) return;
      
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Draw baseline
      const baseline = canvas.height / 2;
      ctx.strokeStyle = '#E5E7EB';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(0, baseline);
      ctx.lineTo(canvas.width, baseline);
      ctx.stroke();
      
      if (!isActive) {
        // Draw flat line with small noise if inactive
        ctx.strokeStyle = '#94A3B8';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(0, baseline);
        
        for (let x = 0; x < canvas.width; x += 5) {
          const y = baseline + (Math.random() * 2 - 1);
          ctx.lineTo(x, y);
        }
        
        ctx.stroke();
        return;
      }
      
      // Draw each wave
      waves.forEach(wave => {
        const { amplitude, frequency, color, offset } = wave;
        
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.beginPath();
        
        for (let x = 0; x <= canvas.width; x++) {
          // Main sine wave with some randomness for realism
          const noise = detailed ? Math.random() * 2 - 1 : 0;
          const y = baseline + 
                   Math.sin((x * frequency) + offset) * amplitude + 
                   noise;
          
          if (x === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }
        
        ctx.stroke();
      });
      
      // Animate waves
      waves.forEach(wave => {
        wave.offset += wave.speed;
      });
      
      animationFrameRef.current = requestAnimationFrame(drawWave);
    };

    // Start animation
    drawWave();

    // Cleanup
    return () => {
      window.removeEventListener('resize', resizeCanvas);
      cancelAnimationFrame(animationFrameRef.current);
    };
  }, [isActive, detailed]);

  return (
    <div className="w-full h-full relative">
      <canvas 
        ref={canvasRef}
        className="w-full h-full"
      />
      {!isActive && (
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-gray-500 text-sm">Detector inactive</span>
        </div>
      )}
    </div>
  );
};

export default WaveVisualizer;