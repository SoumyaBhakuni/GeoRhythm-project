import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  ChartData
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const IntensityChart: React.FC = () => {
  // Generate some random data for the chart
  const generateData = () => {
    const baseValue = 5;
    const spikes = [12, 18, 25]; // Positions of "earthquake" spikes
    
    return Array(30).fill(0).map((_, i) => {
      // Random normal activity (small variations)
      let value = baseValue + (Math.random() * 2 - 1);
      
      // Add earthquake spikes
      if (spikes.includes(i)) {
        // Magnitude varies between 5-8
        const magnitude = 5 + Math.random() * 3;
        value = baseValue + magnitude;
      }
      
      return value;
    });
  };
  
  const generateTimeLabels = () => {
    const now = new Date();
    return Array(30).fill(0).map((_, i) => {
      const time = new Date(now.getTime() - (29 - i) * 60000);
      return time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    });
  };
  
  const data: ChartData<'line'> = {
    labels: generateTimeLabels(),
    datasets: [
      {
        label: 'Seismic Intensity',
        data: generateData(),
        borderColor: '#3B82F6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.3,
        fill: true,
        pointBackgroundColor: (context) => {
          const value = context.dataset.data[context.dataIndex] as number;
          if (value > 10) return '#DC2626'; // Red for high intensity
          if (value > 7) return '#F97316'; // Orange for medium
          return '#3B82F6'; // Default blue
        },
        pointRadius: (context) => {
          const value = context.dataset.data[context.dataIndex] as number;
          if (value > 10) return 6;
          if (value > 7) return 4;
          return 3;
        },
        pointHoverRadius: 8,
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        titleColor: '#1F2937',
        bodyColor: '#1F2937',
        borderColor: '#E5E7EB',
        borderWidth: 1,
        padding: 10,
        cornerRadius: 6,
        displayColors: false,
        callbacks: {
          label: function(context: any) {
            const value = context.parsed.y;
            let label = `Intensity: ${value.toFixed(1)}`;
            
            // Add classification based on value
            if (value > 10) {
              label += ' (Strong)';
            } else if (value > 7) {
              label += ' (Moderate)';
            } else {
              label += ' (Weak)';
            }
            
            return label;
          }
        }
      }
    },
    scales: {
      x: {
        grid: {
          display: false
        },
        ticks: {
          maxRotation: 0,
          autoSkip: true,
          maxTicksLimit: 6
        }
      },
      y: {
        min: 0,
        max: 15,
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        },
        ticks: {
          stepSize: 3
        }
      }
    },
    interaction: {
      mode: 'index',
      intersect: false,
    },
  };

  return <Line data={data} options={options} />;
};

export default IntensityChart;