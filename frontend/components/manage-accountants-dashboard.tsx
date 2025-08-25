import React, { useState } from 'react';
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"

const SuperAccountantDashboard = () => {
    const [selectedAccountant, setSelectedAccountant] = useState<string>('');
    const [selectedBusiness, setSelectedBusiness] = useState<string>('');

    const accountants = ['Accountant 1', 'Accountant 2', 'Accountant 3'];
    const businesses = ['Business A', 'Business B', 'Business C'];

    const handleAssign = () => {
        // Logic to assign accountant to business
        console.log(`Assigned ${selectedAccountant} to ${selectedBusiness}`);
    };

    return (
        <div className='flex justify-center'>
            <div className='space-y-6 w-2/3'>
                <Table>
                    <TableCaption>A list of your recent invoices.</TableCaption>
                    <TableHeader>
                        <TableRow>
                            <TableHead className="w-[100px]">Invoice</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead>Method</TableHead>
                            <TableHead className="text-right">Amount</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        <TableRow>
                            <TableCell className="font-medium">INV001</TableCell>
                            <TableCell>Paid</TableCell>
                            <TableCell>Credit Card</TableCell>
                            <TableCell className="text-right">$250.00</TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
            </div>
        </div>
    );
};

export default SuperAccountantDashboard;
