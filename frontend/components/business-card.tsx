import React, { useState } from 'react';
import { DocumentIcon, CheckCircleIcon, DocumentCurrencyDollarIcon } from '@heroicons/react/24/outline';
import { Card, CardHeader, CardContent, CardTitle } from './ui/card';
import FinanceCard from './finance-card';
import { Business, Accountant } from '../types';
import { useAuth } from '../context/AuthContext';
import { Button } from './ui/button';
import AccountantsDialog from './accountant-dialog';
import { Roles } from '../lib/roles';

interface BusinessCardProps {
    index: number;
    business: Business;
    onRefresh?: () => void; // Callback to refresh data
}

const BusinessCard: React.FC<BusinessCardProps> = ({ index, business, onRefresh }) => {
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

    return (
        <Card key={index} className="shadow-lg">
            <CardHeader>
                <CardTitle className="text-lg font-bold">{business.name}</CardTitle>
            </CardHeader>
            <CardContent>
                <div className='grid grid-cols-1 md:grid-cols-2 gap-4 mb-4'>
                    <div className="space-y-2">
                        {/* Documents Due */}
                        <div className="flex items-center space-x-2">
                            <DocumentIcon className="h-5 w-5 text-blue-500" />
                            <span className="text-sm text-gray-700">
                                {metrics?.documents_due} Documents Due
                            </span>
                        </div>
                        {/* Outstanding Invoices */}
                        <div className="flex items-center space-x-2">
                            <DocumentCurrencyDollarIcon className="h-5 w-5 text-green-500" />
                            <span className="text-sm text-gray-700">
                                {metrics?.outstanding_invoices} Outstanding Invoices
                            </span>
                        </div>
                        {/* Pending Approvals */}
                        <div className="flex items-center space-x-2">
                            <CheckCircleIcon className="h-5 w-5 text-yellow-500" />
                            <span className="text-sm text-gray-700">
                                {metrics?.pending_approvals} Pending Approvals
                            </span>
                        </div>
                        {/* Year End Date */}
                        <div className="flex items-center space-x-2">
                            <CheckCircleIcon className="h-5 w-5 text-yellow-500" />
                            <span className="text-sm text-gray-700">
                                Accounting YE: {metrics?.accounting_year_end}
                            </span>
                        </div>
                    </div>
                    {financialMetrics && (
                        <div className="space-y-2">
                            <FinanceCard metric={financialMetrics.revenue} percentageChange={financialMetrics.percentage_change_revenue} title="MTD Revenue" />
                            <FinanceCard metric={financialMetrics.gross_profit} percentageChange={financialMetrics.percentage_change_gross_profit} title="Gross Profit" />
                            <FinanceCard metric={financialMetrics.net_profit} percentageChange={financialMetrics.percentage_change_net_profit} title="Net Profit" />
                            <FinanceCard metric={financialMetrics.total_costs} percentageChange={financialMetrics.percentage_change_total_costs} title="Total Costs" />
                        </div>)}
                </div>

                <div className="flex justify-center">
                    <Button variant='secondary' onClick={handleClickOpen}>
                        View {user?.role === Roles.ROOT_ADMIN || user?.role === Roles.SUPER_ACCOUNTANT ? "& Manage" : ""} Accountants
                    </Button>
                </div>

                <AccountantsDialog open={openDialog} onClose={handleClose} businessName={business.name} businessId={business.id} accountants={business.accountants || []} onAccountantRemoved={handleAccountantRemoved} />
            </CardContent>
        </Card>
    );
};

export default BusinessCard;
