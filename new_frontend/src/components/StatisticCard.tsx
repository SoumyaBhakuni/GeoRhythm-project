import React from 'react';

interface StatisticCardProps {
  icon: React.ReactNode;
  title: string;
  value: string;
  description: string;
}

const StatisticCard: React.FC<StatisticCardProps> = ({ icon, title, value, description }) => {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 transition-transform hover:scale-[1.02]">
      <div className="flex items-center mb-4">
        {icon}
        <h3 className="text-lg font-semibold text-gray-800 ml-3">{title}</h3>
      </div>
      <p className="text-3xl font-bold text-gray-900 mb-2">{value}</p>
      <p className="text-gray-600">{description}</p>
    </div>
  );
};

export default StatisticCard;