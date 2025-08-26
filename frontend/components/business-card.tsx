import React, { useState } from 'react';
import { DocumentIcon, CurrencyDollarIcon, CheckCircleIcon, DocumentCurrencyDollarIcon } from '@heroicons/react/24/outline';
import { Card, CardHeader, CardContent, CardFooter, CardTitle, CardDescription } from './ui/card';
import FinanceCard from './finance-card';
import { Business } from '../types/business';
import { useAuth } from '../context/AuthContext';
import Link from 'next/link';
import { Button } from './ui/button';
import AccountantsDialog from './accountant-dialog';

interface BusinessCardProps {
    index: number;
    business: Business
}

const BusinessCard: React.FC<BusinessCardProps> = ({ index, business }) => {
    const { user } = useAuth();
    const [openDialog, setOpenDialog] = useState(false);

    const handleClickOpen = () => {
        setOpenDialog(true);
    };

    const handleClose = () => {
        setOpenDialog(false);
    };

    return (
        <Card key={index} className="shadow-lg">
            <CardHeader>
                <CardTitle className="text-lg font-bold">{business.name}</CardTitle>
            </CardHeader>
            <CardContent className='grid grid-cols-1 sm:grid-cols-2'>
                <div className="space-y-2">
                    {/* Documents Due */}
                    <div className="flex items-center space-x-2">
                        <DocumentIcon className="h-5 w-5 text-blue-500" />
                        <span className="text-sm text-gray-700">
                            {business.metrics.documentsDue} Documents Due
                        </span>
                    </div>
                    {/* Outstanding Invoices */}
                    <div className="flex items-center space-x-2">
                        <DocumentCurrencyDollarIcon className="h-5 w-5 text-green-500" />
                        <span className="text-sm text-gray-700">
                            {business.metrics.outstandingInvoices} Outstanding Invoices
                        </span>
                    </div>
                    {/* Pending Approvals */}
                    <div className="flex items-center space-x-2">
                        <CheckCircleIcon className="h-5 w-5 text-yellow-500" />
                        <span className="text-sm text-gray-700">
                            {business.metrics.pendingApprovals} Pending Approvals
                        </span>
                    </div>
                    {/* Year End Date */}
                    <div className="flex items-center space-x-2">
                        <CheckCircleIcon className="h-5 w-5 text-yellow-500" />
                        <span className="text-sm text-gray-700">
                            Accounting YE: {business.metrics.accountingYearEnd}
                        </span>
                    </div>
                </div>
                <div className="space-y-2">
                    <FinanceCard metric={business.financialMetrics.revenue} percentageChange={business.financialMetrics.percentageChangeRevenue} title="MTD Revenue" />
                    <FinanceCard metric={business.financialMetrics.grossProfit} percentageChange={business.financialMetrics.percentageChangeGrossProfit} title="Gross Profit" />
                    <FinanceCard metric={business.financialMetrics.netProfit} percentageChange={business.financialMetrics.percentageChangeNetProfit} title="Net Profit" />
                    <FinanceCard metric={business.financialMetrics.totalCosts} percentageChange={business.financialMetrics.percentageChangeTotalCosts} title="Total Costs" />
                </div>

                <Button variant='secondary' className='mt-4 col-span-2 w-1/2 mx-auto' onClick={handleClickOpen}>
                    View { user.role === "root_admin" || user.role === "super_accountant" ? "& Edit" : ""} Accountants
                </Button>

                <AccountantsDialog open={openDialog} onClose={handleClose} businessName={business.name} businessId={business.id} accountants={business.accountants}/>
            </CardContent>
        </Card>
    );
};

export default BusinessCard;
