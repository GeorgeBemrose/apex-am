import React, { useState, useEffect } from 'react';
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "./ui/table";
import { accountantsAPI, Accountant } from '../lib/api';
import { Select, MenuItem } from '@mui/material';

const roleOptions = [
    { value: 'accountant', label: 'Accountant' },
    { value: 'super_accountant', label: 'Super Accountant' },
];

const ManageSuperDashboard = () => {
    const [accountants, setAccountants] = useState<Accountant[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetchAccountants();
    }, []);

    const fetchAccountants = async () => {
        try {
            setLoading(true);
            const data = await accountantsAPI.getAll();
            setAccountants(data);
            setError(null);
        } catch (err) {
            console.error('Failed to fetch accountants:', err);
            setError('Failed to load accountants');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = async (value: string, accountant: Accountant) => {
        try {
            if (value === 'super_accountant') {
                // Assign super accountant role
                await accountantsAPI.assignSuperAccountant(accountant.id, accountant.user_id);
            } else {
                // Remove super accountant role
                await accountantsAPI.removeSuperAccountant(accountant.id);
            }
            
            // Refresh the list
            await fetchAccountants();
        } catch (error) {
            console.error("Error updating accountant:", error);
            setError('Failed to update accountant role');
        }
    };

    if (loading) {
        return (
            <div className='flex justify-center w-full'>
                <div className='space-y-6 w-2/3'>
                    <div className="animate-pulse">
                        <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
                        <div className="space-y-3">
                            {[...Array(5)].map((_, i) => (
                                <div key={i} className="h-12 bg-gray-200 rounded"></div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className='flex justify-center w-full'>
                <div className='space-y-6 w-2/3'>
                    <div className="bg-red-50 border border-red-200 rounded-md p-4">
                        <p className="text-red-800">{error}</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className='flex justify-center w-full'>
            <div className='space-y-6 w-2/3'>
                <Table>
                    <TableCaption>A list of accountants.</TableCaption>
                    <TableHeader>
                        <TableRow>
                            <TableHead className="w-[100px]">First Name</TableHead>
                            <TableHead>Last Name</TableHead>
                            <TableHead>Email</TableHead>
                            <TableHead>Role</TableHead>
                            <TableHead className="text-right"></TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {accountants.map((accountant) => (
                            <TableRow key={accountant.id}>
                                <TableCell>{accountant.first_name || 'N/A'}</TableCell>
                                <TableCell>{accountant.last_name || 'N/A'}</TableCell>
                                <TableCell>{accountant.user?.email || 'N/A'}</TableCell>
                                <TableCell>
                                    {accountant.user?.role === "root_admin" ? 
                                    "Root Admin" 
                                    : 
                                    <Select
                                        value={accountant.user?.role || 'accountant'}
                                        onChange={(e) => handleChange(e.target.value, accountant)}
                                        className='text-xs'
                                    >
                                        {roleOptions.map((option) => (
                                            <MenuItem key={option.value} value={option.value}>
                                                {option.label}
                                            </MenuItem>
                                        ))}
                                    </Select>}
                                    
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>
        </div>
    );
};

export default ManageSuperDashboard;
