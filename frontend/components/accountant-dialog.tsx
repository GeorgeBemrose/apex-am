import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';
import { Button } from './ui/button';
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "./ui/table"
import { TrashIcon } from '@heroicons/react/24/outline';
import { useAuth } from '../context/AuthContext';

interface Accountant {
    id: string;
    firstName: string;
    lastName: string;
    email: string;
}

interface AccountantsDialogProps {
    open: boolean;
    onClose: () => void;
    businessName: string;
    accountants: Accountant[];
    businessId: string;
}

const AccountantsDialog: React.FC<AccountantsDialogProps> = ({ open, onClose, businessId, businessName, accountants }) => {
const handleDelete = async (accountantId: string, businessId: string) => {
    try {
        // Placeholder for API call to delete the accountant
        console.log(`Deleting accountant with ID: ${accountantId} from business: ${businessId}`);
        // await api.delete(`/accountants/${accountantId}`); // Uncomment when API is available
    } catch (error) {
        console.error("Error deleting accountant:", error);
    }
};
    const {user} = useAuth();
    return (
        <Dialog open={open} onClose={onClose} fullWidth={true}>
            <DialogTitle>{businessName} - Accountants</DialogTitle>
            <DialogContent>
                <div className='flex justify-center'>
                    <div className='space-y-6'>

                        <Table>
                            <TableCaption>A list of accountants of {businessName}.</TableCaption>
                            <TableHeader>
                                <TableRow>
                                    <TableHead className="w-[100px]">First Name</TableHead>
                                    <TableHead>Last Name</TableHead>
                                    <TableHead>Email</TableHead>
                                    <TableHead className="text-right"></TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {accountants.map((accountant) => (
                                    <TableRow key={accountant.id}>
                                        <TableCell>{accountant.firstName}</TableCell>
                                        <TableCell>{accountant.lastName}</TableCell>
                                        <TableCell>{accountant.email}</TableCell>
                                        { user.role === "root_admin" || user.role === "super_accountant" ? 
                                            <TableCell>
                                                <Button 
                                                    variant={"secondary"} 
                                                    onClick={() => handleDelete(accountant.id, businessId)}
                                                >
                                                    <TrashIcon />
                                                </Button>
                                            </TableCell> 
                                            : null
                                        }
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </div>
                </div>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose} color="primary" variant={"secondary"}>
                    Close
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default AccountantsDialog;