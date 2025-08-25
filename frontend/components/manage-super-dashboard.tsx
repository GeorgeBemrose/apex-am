import React from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const accountants = [
    { name: 'John Doe', role: 'Accountant' },
    { name: 'Jane Smith', role: 'Super Accountant' },
    { name: 'Alice Johnson', role: 'Accountant' },
    { name: 'Bob Brown', role: 'Super Accountant' },
];

const RootAdminDashboard = () => {
    return (
        <TableContainer component={Paper}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>Name</TableCell>
                        <TableCell>Role</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {accountants.map((accountant, index) => (
                        <TableRow key={index}>
                            <TableCell>{accountant.name}</TableCell>
                            <TableCell>{accountant.role}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};

export default RootAdminDashboard;
