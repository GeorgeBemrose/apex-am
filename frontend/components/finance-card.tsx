import React from 'react';
import { CurrencyDollarIcon } from '@heroicons/react/24/outline';

interface FinanceCardProps {
    metric: number;
    percentageChange: number;
    title: string;
}

const FinanceCard: React.FC<FinanceCardProps> = ({ metric, percentageChange, title }) => {
    // Runtime safety check - handle cases where values might be undefined despite interface
    if (metric === undefined || percentageChange === undefined || 
        typeof metric !== 'number' || typeof percentageChange !== 'number') {
        return (
            <div className="flex items-center space-x-2">
                <CurrencyDollarIcon className="h-5 w-5 text-gray-400" />
                <span className="text-sm text-gray-500">{title}</span>
                <span className="text-sm font-bold text-gray-400">--</span>
            </div>
        );
    }
    
    // For Total Costs, an increase (positive change) is bad, so we invert the logic
    const isPositive = title === 'Total Costs' ? percentageChange < 0 : percentageChange > 0;
    const colorClass = isPositive ? 'text-green-500' : 'text-red-500';
    
    return (
        <div className="flex items-center space-x-2">
            <CurrencyDollarIcon className={`h-5 w-5 ${colorClass}`} />
            <span className="text-sm">{title}</span>
            <span className={`text-sm font-bold ${colorClass}`}>
                ${metric.toLocaleString()} ({percentageChange}%)
            </span>
        </div>
    );
};

export default FinanceCard;
