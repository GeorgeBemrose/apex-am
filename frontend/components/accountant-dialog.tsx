import React, { useState, useEffect, useCallback } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, TextField, Autocomplete, Button as MuiButton } from '@mui/material';
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
import { TrashIcon, PlusIcon } from '@heroicons/react/24/outline';
import { useAuth } from '../context/AuthContext';
import { accountantsAPI } from '../lib/api';
import { Accountant } from '../types';
import { CheckCircleIcon } from '@heroicons/react/24/solid';
import { Roles } from '../lib/roles';

interface AccountantSearchResult {
    id: string;
    first_name: string;
    last_name: string;
    email: string;
    user: {
        id: string;
        email: string;
        role: string;
    };
}

interface AccountantsDialogProps {
    open: boolean;
    onClose: () => void;
    businessName: string;
    accountants: Accountant[];
    businessId: string;
    onAccountantRemoved?: () => void; // Callback to refresh data
}

const AccountantsDialog: React.FC<AccountantsDialogProps> = ({ open, onClose, businessId, businessName, accountants, onAccountantRemoved }) => {
    const { user } = useAuth();
    const [availableAccountants, setAvailableAccountants] = useState<AccountantSearchResult[]>([]);
    const [selectedAccountant, setSelectedAccountant] = useState<AccountantSearchResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);
    const [isOperationInProgress, setIsOperationInProgress] = useState(false);
    const [allocatedAccountants, setAllocatedAccountants] = useState<Accountant[]>(accountants);
    
    // Show toast for 3 seconds
    useEffect(() => {
        if (toast) {
            const timer = setTimeout(() => setToast(null), 3000);
            return () => clearTimeout(timer);
        }
    }, [toast]);

    // Custom close handler that prevents closing during operations
    const handleClose = () => {
        if (!isOperationInProgress) {
            onClose();
        }
    };

    const fetchAvailableAccountants = useCallback(async () => {
        try {
            setLoading(true);
            const allAccountants = await accountantsAPI.getAll();
            // Filter out accountants that are already assigned to this business
            const assignedIds = accountants.map(acc => acc.id);
            const available = allAccountants.filter(acc => !assignedIds.includes(acc.id.toString()));
            // Convert Accountant to AccountantSearchResult format
            const availableFormatted = available.map(acc => ({
                id: acc.id,
                first_name: acc.first_name || '',
                last_name: acc.last_name || '',
                email: acc.user?.email || '',
                user: {
                    id: acc.user_id,
                    email: acc.user?.email || '',
                    role: acc.user?.role || ''
                }
            }));
            setAvailableAccountants(availableFormatted);
        } catch (error) {
            console.error('Failed to fetch available accountants:', error);
        } finally {
            setLoading(false);
        }
    }, [accountants]);

    // Add useEffect after function definition to avoid dependency issues
    useEffect(() => {
        if (open) {
            fetchAvailableAccountants();
        }
    }, [open, fetchAvailableAccountants]);

    const handleAddAccountant = async () => {
        if (!selectedAccountant) return;
        
        setIsOperationInProgress(true);
        try {
            const token = localStorage.getItem('access_token');
            const requestBody = { accountant_id: selectedAccountant.id };
            
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/businesses/${businessId}/assign-accountant`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody),
            });
            
            if (!response.ok) {
                throw new Error(`Failed to add accountant: ${response.statusText}`);
            }
            
            setSelectedAccountant(null);
            
            // Show success toast first
            setToast({ type: 'success', message: `Accountant ${selectedAccountant.first_name} ${selectedAccountant.last_name} added successfully!` });
            
            // Clear selection
            setSelectedAccountant(null);
            
            // Refresh the available accountants list
            await fetchAvailableAccountants();
            
            // Temporarily add to allocated list for immediate UI update
            const tempAccountant = {
                id: selectedAccountant.id,
                first_name: selectedAccountant.first_name,
                last_name: selectedAccountant.last_name,
                user: { email: selectedAccountant.email }
            };
            setAllocatedAccountants([...allocatedAccountants, tempAccountant as Accountant]);

        } catch (error) {
            console.error("Error adding accountant:", error);
            setToast({ type: 'error', message: `Failed to add accountant: ${error instanceof Error ? error.message : 'Unknown error'}` });
        } finally {
            setIsOperationInProgress(false);
        }
    };

    const handleDelete = async (accountantId: string, businessId: string) => {
        setIsOperationInProgress(true);
        try {
            const token = localStorage.getItem('access_token');
            
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/businesses/${businessId}/remove-accountant`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ accountant_id: accountantId }),
            });
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Failed to remove accountant: ${response.statusText}`);
            }
            
            // Show success toast first
            setToast({ type: 'success', message: `Accountant removed successfully!` });
            
            // Remove from allocated list immediately for instant UI feedback
            setAllocatedAccountants(allocatedAccountants.filter(acc => acc.id !== accountantId));
            
            // Refresh the available accountants list
            await fetchAvailableAccountants();
        } catch (error) {
            console.error("Error removing accountant:", error);
            setToast({ type: 'error', message: `Failed to remove accountant: ${error instanceof Error ? error.message : 'Unknown error'}` });
        } finally {
            setIsOperationInProgress(false);
        }
    };

    return (

        <Dialog open={open} onClose={handleClose} fullWidth={true} maxWidth="md">
            <DialogTitle>{businessName} - Accountants</DialogTitle>
            <DialogContent>
                {/* Toast Notification - Inside Dialog */}
                {toast && (
                    <div className={`mb-4 p-3 rounded-lg ${
                        toast.type === 'success' 
                            ? 'bg-green-100 border border-green-300 text-green-800' 
                            : 'bg-red-100 border border-red-300 text-red-800'
                    }`}>
                        <div className="flex items-center space-x-2">
                            {toast.type === 'success' ? (
                                <CheckCircleIcon className="h-5 w-5 text-green-600" />
                            ) : (
                                <div className="h-5 w-5 rounded-full border-2 border-red-600"></div>
                            )}
                            <span className="font-medium">{toast.message}</span>
                        </div>
                    </div>
                )}

                <div className='space-y-6'>
                    {/* Add Accountant Section */}
                    {(user?.role === Roles.ROOT_ADMIN || user?.role === Roles.SUPER_ACCOUNTANT) && (
                        <div className="bg-gray-50 p-4 rounded-lg">
                            <h3 className="text-lg font-medium text-gray-900 mb-3">Add Accountant</h3>
                            <div className="flex items-center space-x-3 w-full">
                                <Autocomplete
                                    options={availableAccountants}
                                    getOptionLabel={(option) => `${option.first_name} ${option.last_name} (${option.email})`}
                                    value={selectedAccountant}
                                    onChange={(_, newValue) => setSelectedAccountant(newValue)}
                                    loading={loading}
                                    fullWidth
                                    renderInput={(params) => (
                                        <TextField
                                            {...params}
                                            label="Search for an accountant"
                                            variant="outlined"
                                            size="small"
                                        />
                                    )}
                                    filterOptions={(options, { inputValue }) =>
                                        options.filter(option =>
                                            option.first_name.toLowerCase().includes(inputValue.toLowerCase()) ||
                                            option.last_name.toLowerCase().includes(inputValue.toLowerCase()) ||
                                            option.email.toLowerCase().includes(inputValue.toLowerCase())
                                        )
                                    }
                                />
                                <MuiButton
                                    variant="contained"
                                    onClick={handleAddAccountant}
                                    disabled={!selectedAccountant}
                                    startIcon={<PlusIcon className="h-4 w-4" />}
                                >
                                    Add
                                </MuiButton>
                            </div>
                        </div>
                    )}
                    
                    {/* Current Accountants Table */}
                    {allocatedAccountants && (
                        <div className='flex justify-center'>
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
                                {allocatedAccountants.map((accountant) => (
                                    <TableRow key={accountant.id}>
                                        <TableCell>{accountant.first_name}</TableCell>
                                        <TableCell>{accountant.last_name}</TableCell>
                                        <TableCell>{accountant?.user?.email}</TableCell>
                                        { user?.role === Roles.ROOT_ADMIN || user?.role === Roles.SUPER_ACCOUNTANT ? 
                                            <TableCell>
                                                <Button 
                                                    variant={"secondary"} 
                                                    onClick={() => handleDelete(accountant.id, businessId)}
                                                    className="text-red-600 hover:text-red-700 hover:bg-red-50"
                                                    title="Remove accountant from this business"
                                                >
                                                    <TrashIcon className="h-4 w-4" />
                                                </Button>
                                            </TableCell> 
                                            : null
                                        }
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </div>
                    )}
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