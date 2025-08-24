import React from 'react';
import { Card, CardHeader, CardContent, CardFooter } from '@/components/ui/card';
import { DocumentIcon, CurrencyDollarIcon, CheckCircleIcon } from '@heroicons/react/24/outline';

const businesses = [
    { name: 'Los Pollos Hermanos', indicator: 'Revenue: $10,000', metrics: { documentsDue: 23, outstandingInvoices: 5, pendingApprovals: 2, accountingYearEnd: '23/09/2025' } },
    { name: 'Gray Matter Technologies', indicator: 'Revenue: $10,000', metrics: { documentsDue: 15, outstandingInvoices: 3, pendingApprovals: 1, accountingYearEnd: '23/03/2026' } },
    { name: 'Saul Goodman & Associates', indicator: 'Revenue: $15,000', metrics: { documentsDue: 30, outstandingInvoices: 8, pendingApprovals: 4, accountingYearEnd: '31/12/2025' } },
    { name: 'Business C', indicator: 'Revenue: $8,000', metrics: { documentsDue: 10, outstandingInvoices: 2, pendingApprovals: 0, accountingYearEnd: '01/04/2026' } },
];

const AccountantDashboard: React.FC = () => {
    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 p-10">
            {businesses.map((business, index) => (
                <Card key={index} className="shadow-lg">
                    <CardHeader>
                        <h2 className="text-lg font-bold">{business.name}</h2>
                    </CardHeader>
                    <CardContent>
                        <p>{business.indicator}</p>
                        <div className="mt-4 space-y-2">
                            
                            {/* Documents Due */}
                            <div className="flex items-center space-x-2">
                                <DocumentIcon className="h-5 w-5 text-blue-500" />
                                <span className="text-sm text-gray-700">
                                    {business.metrics.documentsDue} Documents Due
                                </span>
                            </div>
                            {/* Outstanding Invoices */}
                            <div className="flex items-center space-x-2">
                                <CurrencyDollarIcon className="h-5 w-5 text-green-500" />
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
                                    Account Year End: {business.metrics.accountingYearEnd}
                                </span>
                            </div>
                        </div>
                    </CardContent>
                    <CardFooter>
                        <button className="btn btn-primary">View Details</button>
                    </CardFooter>
                </Card>
            ))}
        </div>
    );
};

export default AccountantDashboard;