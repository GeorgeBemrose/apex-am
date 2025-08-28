import React from 'react';
import { CurrencyDollarIcon, ArrowUpIcon, ArrowDownIcon } from '@heroicons/react/24/outline';

interface FinanceCardProps {
    metric: number;
    percentageChange: number;
    title: string;
}

const FinanceCard: React.FC<FinanceCardProps> = ({ metric, percentageChange, title }) => {    
    // For Total Costs, an increase (positive change) is bad, so we invert the logic
    const isPositive = title === 'Total Costs' ? percentageChange < 0 : percentageChange > 0;
    const colorClass = isPositive ? 'text-green-600' : 'text-red-600';
    const bgColorClass = isPositive ? 'bg-green-50' : 'bg-red-50';
    const borderColorClass = isPositive ? 'border-green-200' : 'border-red-200';
    
    return (
        <div className={`flex flex-col sm:flex-row sm:items-center sm:justify-between p-2 sm:p-2 rounded-lg border ${bgColorClass} ${borderColorClass} space-y-1 sm:space-y-0`}>
            <div className="flex items-center space-x-2">
                <CurrencyDollarIcon className="h-4 w-4 text-gray-500" />
                <span className="text-sm font-medium text-gray-700">{title}</span>
            </div>
            <div className="flex items-center space-x-2">
                <span className="text-sm font-bold text-gray-900">
                    ${metric.toLocaleString()}
                </span>
                <div className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium ${bgColorClass} ${colorClass}`}>
                    {isPositive ? (
                        <ArrowUpIcon className="h-3 w-3" />
                    ) : (
                        <ArrowDownIcon className="h-3 w-3" />
                    )}
                    <span>{Math.abs(percentageChange)}%</span>
                </div>
            </div>
        </div>
    );
};

export default FinanceCard;
