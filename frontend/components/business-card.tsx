import React, { useState } from 'react';
import { 
    DocumentIcon, 
    CheckCircleIcon, 
    DocumentCurrencyDollarIcon,
    BuildingOfficeIcon,
    CalendarIcon
} from '@heroicons/react/24/outline';
import { Card, CardHeader, CardContent, CardTitle } from './ui/card';
import FinanceCard from './finance-card';
import { Business } from '../types';
import { useAuth } from '../context/AuthContext';
import { Button } from './ui/button';
import AccountantsDialog from './accountant-dialog';
import { Roles } from '../lib/roles';

interface BusinessCardProps {
    business: Business;
    onRefresh?: () => void; // Callback to refresh data
}

const BusinessCard: React.FC<BusinessCardProps> = ({ business, onRefresh }) => {
    const { user } = useAuth();
    const [openDialog, setOpenDialog] = useState(false);

    const handleClickOpen = () => {
        setOpenDialog(true);
    };

    const handleClose = () => {
        setOpenDialog(false);
    };

    const handleAccountantRemoved = () => {
        // Just refresh the data, don't close the dialog
        if (onRefresh) {
            onRefresh();
        }
    };

    // Get the first metrics and financial_metrics objects since they're now arrays
    const metrics = business.metrics?.[0];
    const financialMetrics = business.financial_metrics?.[0];

    // Format date for better display
    const formatDate = (dateString: string) => {
        if (!dateString) return 'N/A';
        return new Date(dateString).toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric', 
            year: 'numeric' 
        });
    };

    return (
        <Card className="shadow-lg hover:shadow-xl transition-all duration-200 border-0 bg-gradient-to-br from-white to-gray-50">
            {/* Header with Status */}
            <CardHeader>
                <div className="flex items-start justify-between">
                    <div className="flex-1">
                        <CardTitle className="text-lg font-bold text-gray-900 flex items-center gap-2">
                            <BuildingOfficeIcon className="h-5 w-5 text-blue-600" />
                            {business.name}
                        </CardTitle>
                        {business.description && (
                            <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                                {business.description}
                            </p>
                        )}
                    </div>
                    {/* Status Badge */}
                    <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                        business.is_active 
                            ? 'bg-green-100 text-green-800 border border-green-200'
                            : 'bg-red-100 text-red-800 border border-red-200'
                    }`}>
                        {business.is_active ? 'Active' : 'Inactive'}
                    </div>
                </div>
            </CardHeader>

            <CardContent className="pt-0">
                {/* Key Metrics Section */}
                <div className="mb-4">
                    <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                        <DocumentIcon className="h-4 w-4 text-blue-500" />
                        Key Metrics
                    </h4>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-3">
                        <div className="flex items-center space-x-2 p-2 sm:p-2 bg-blue-50 rounded-lg">
                            <DocumentIcon className="h-4 w-4 text-blue-500" />
                            <div className="min-w-0 flex-1">
                                <div className="text-xs text-gray-500">Documents Due</div>
                                <div className="text-sm font-semibold text-gray-900">
                                    {metrics?.documents_due || 0}
                                </div>
                            </div>
                        </div>
                        <div className="flex items-center space-x-2 p-2 sm:p-2 bg-orange-50 rounded-lg">
                            <DocumentCurrencyDollarIcon className="h-4 w-4 text-orange-500" />
                            <div className="min-w-0 flex-1">
                                <div className="text-xs text-gray-500">Outstanding</div>
                                <div className="text-sm font-semibold text-gray-900">
                                    {metrics?.outstanding_invoices || 0}
                                </div>
                            </div>
                        </div>
                        <div className="flex items-center space-x-2 p-2 sm:p-2 bg-purple-50 rounded-lg">
                            <CheckCircleIcon className="h-4 w-4 text-purple-500" />
                            <div className="min-w-0 flex-1">
                                <div className="text-xs text-gray-500">Pending</div>
                                <div className="text-sm font-semibold text-gray-900">
                                    {metrics?.pending_approvals || 0}
                                </div>
                            </div>
                        </div>
                        <div className="flex items-center space-x-2 p-2 sm:p-2 bg-indigo-50 rounded-lg">
                            <CalendarIcon className="h-4 w-4 text-indigo-500" />
                            <div className="min-w-0 flex-1">
                                <div className="text-xs text-gray-500">Year End</div>
                                <div className="text-sm font-semibold text-gray-900">
                                    {metrics?.accounting_year_end ? formatDate(metrics.accounting_year_end) : 'N/A'}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Financial Metrics Section */}
                {financialMetrics && (
                    <div className="mb-4">
                        <h4 className="text-sm font-semibold text-gray-700 mb-2 sm:mb-3 flex items-center gap-2">
                            <DocumentCurrencyDollarIcon className="h-4 w-4 text-green-500" />
                            Financial Performance
                        </h4>
                        <div className="space-y-2">
                            <FinanceCard metric={financialMetrics.revenue} percentageChange={financialMetrics.percentage_change_revenue} title="Revenue" />
                            <FinanceCard metric={financialMetrics.gross_profit} percentageChange={financialMetrics.percentage_change_gross_profit} title="Gross Profit" />
                            <FinanceCard metric={financialMetrics.net_profit} percentageChange={financialMetrics.percentage_change_net_profit} title="Net Profit" />
                            <FinanceCard metric={financialMetrics.total_costs} percentageChange={financialMetrics.percentage_change_total_costs} title="Total Costs" />
                        </div>
                    </div>
                )}



                {/* Action Button */}
                <div className="flex justify-center">
                    <Button 
                        variant='secondary' 
                        onClick={handleClickOpen}
                        className="w-full bg-white hover:bg-gray-50 text-gray-700 border border-gray-300 hover:border-gray-400 shadow-sm hover:shadow-md transition-all duration-200 text-sm sm:text-base py-2 sm:py-2.5"
                    >
                        {user?.role === Roles.ROOT_ADMIN || user?.role === Roles.SUPER_ACCOUNTANT ? 
                            "View & Manage Accountants" : 
                            "View Accountants"
                        }
                    </Button>
                </div>

                <AccountantsDialog 
                    open={openDialog} 
                    onClose={handleClose} 
                    businessName={business.name} 
                    businessId={business.id} 
                    accountants={business.accountants || []} 
                    onAccountantRemoved={handleAccountantRemoved} 
                />
            </CardContent>
        </Card>
    );
};

export default BusinessCard;
