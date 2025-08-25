import React from 'react';
import { CurrencyDollarIcon } from '@heroicons/react/24/outline';

interface FinanceCardProps {
    metric: number;
    percentageChange: number;
    title: string;
}

const FinanceCard: React.FC<FinanceCardProps> = ({ metric, percentageChange, title }) => {
    return (
        <div className="flex items-center space-x-2">
            <CurrencyDollarIcon className={`h-5 w-5 ${percentageChange > 0 ? 'text-green-500' : 'text-red-500'}`} />
            <span className={`text-sm`}>
                {title}
            </span>
            <span className={`text-sm font-bold ${percentageChange > 0 ? 'text-green-500' : 'text-red-500'}`}>
                ${metric.toLocaleString()} ({percentageChange * 100}%)
            </span>
        </div>
    );
};

export default FinanceCard;
