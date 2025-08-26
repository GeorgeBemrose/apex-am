import React from 'react';
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import accountants from '@/test/testData/accountants.json';
import { Accountant } from '@/types/accountant';
import { Select, MenuItem } from '@mui/material';

const roleOptions = [
    { value: 'accountant', label: 'Accountant' },
    { value: 'super_accountant', label: 'Super Accountant' },
];


const RootAdminDashboard = () => {

    const handleChange = async (value: string, accountant: Accountant) => {
        try {
            // Placeholder for API call to update the accountant
            console.log(`Updating accountant with ID: ${accountant.id} to role: ${value}`);
            // await api.delete(`/accountants/${accountantId}`); // Uncomment when API is available
        } catch (error) {
            console.error("Error updating accountant:", error);
        }
    };

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
                                <TableCell>{accountant.firstName}</TableCell>
                                <TableCell>{accountant.lastName}</TableCell>
                                <TableCell>{accountant.email}</TableCell>
                                <TableCell>
                                    {accountant.role === "root_admin" ? 
                                    "Root Admin" 
                                    : 
                                    <Select
                                        value={accountant.role}
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

export default RootAdminDashboard;
