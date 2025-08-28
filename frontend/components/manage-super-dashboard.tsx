import React, { useState, useEffect } from 'react';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "./ui/table";
import { accountantsAPI, usersAPI } from '../lib/api';
import { Select, MenuItem, Chip, Tooltip, Alert, Snackbar } from '@mui/material';
import { Roles } from '../lib/roles';
import { 
    UserGroupIcon, 
    ShieldCheckIcon, 
    UserIcon, 
    ExclamationTriangleIcon,
    CheckCircleIcon,
    XCircleIcon
} from '@heroicons/react/24/outline';
import { CheckCircleIcon as CheckCircleSolid } from '@heroicons/react/24/solid';

const roleOptions = [
    { value: Roles.ACCOUNTANT, label: 'Accountant', color: 'default' },
    { value: Roles.SUPER_ACCOUNTANT, label: 'Super Accountant', color: 'primary' },
];

// Extended interface to handle both accountants and users
interface UserWithRole {
    id: string;
    first_name?: string;
    last_name?: string;
    email: string;
    role: string;
    is_accountant: boolean;
    accountant_id?: string;
}

const ManageSuperDashboard = () => {
    const [users, setUsers] = useState<UserWithRole[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [successMessage, setSuccessMessage] = useState<string | null>(null);
    const [updatingId, setUpdatingId] = useState<string | null>(null);
    
    // Pagination state
    const [currentPage, setCurrentPage] = useState(1);
    const [usersPerPage] = useState(10);
    
    // Search state
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        try {
            setLoading(true);
            
            // Fetch both users and accountants
            const [allUsers, allAccountants] = await Promise.all([
                usersAPI.getAll(),
                accountantsAPI.getAll()
            ]);

            // Create a map of accountant user IDs for quick lookup
            const accountantUserIds = new Set(allAccountants.map(acc => acc.user_id));

            // Combine users and accountants data
            const combinedUsers: UserWithRole[] = allUsers.map(user => {
                const accountant = allAccountants.find(acc => acc.user_id === user.id);
                return {
                    id: user.id,
                    first_name: user.first_name || accountant?.first_name,
                    last_name: user.last_name || accountant?.last_name,
                    email: user.email,
                    role: user.role,
                    is_accountant: accountantUserIds.has(user.id),
                    accountant_id: accountant?.id
                };
            });

            setUsers(combinedUsers);
            setError(null);
        } catch (err) {
            console.error('Failed to fetch users:', err);
            setError('Failed to load users');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = async (value: string, user: UserWithRole) => {
        try {
            setUpdatingId(user.id);
            
            if (value === Roles.SUPER_ACCOUNTANT) {
                // Assign super accountant role to the user
                await usersAPI.assignRole(user.id, { 
                    new_role: Roles.SUPER_ACCOUNTANT 
                });
                setSuccessMessage(`${user.first_name} ${user.last_name} promoted to Super Accountant`);
            } else {
                // Remove super accountant role (set back to accountant)
                await usersAPI.assignRole(user.id, { 
                    new_role: Roles.ACCOUNTANT 
                });
                setSuccessMessage(`${user.first_name} ${user.last_name} role changed to Accountant`);
            }
            
            // Refresh the list
            await fetchUsers();
            // Reset to first page after role change
            setCurrentPage(1);
        } catch (error) {
            console.error("Error updating user role:", error);
            setError('Failed to update user role');
        } finally {
            setUpdatingId(null);
        }
    };

    const getRoleChip = (role: string) => {
        if (role === Roles.ROOT_ADMIN) {
            return (
                <Chip
                    icon={<ShieldCheckIcon className="h-4 w-4" />}
                    label="Root Admin"
                    color="error"
                    size="small"
                    variant="outlined"
                />
            );
        } else if (role === Roles.SUPER_ACCOUNTANT) {
            return (
                <Chip
                    icon={<UserGroupIcon className="h-4 w-4" />}
                    label="Super Accountant"
                    color="primary"
                    size="small"
                />
            );
        } else {
            return (
                <Chip
                    icon={<UserIcon className="h-4 w-4" />}
                    label="Accountant"
                    color="default"
                    size="small"
                    variant="outlined"
                />
            );
        }
    };

    const getStatusIcon = (user: UserWithRole) => {
        if (user.role === Roles.ROOT_ADMIN) {
            return <ShieldCheckIcon className="h-5 w-5 text-red-600" />;
        } else if (user.role === Roles.SUPER_ACCOUNTANT) {
            return <UserGroupIcon className="h-5 w-5 text-blue-600" />;
        } else {
            return <UserIcon className="h-5 w-5 text-gray-600" />;
        }
    };

    // Search and filtering logic
    const filteredUsers = users.filter(user => 
        user.first_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.last_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        user.role.toLowerCase().includes(searchTerm.toLowerCase())
    );

    // Pagination logic
    const indexOfLastUser = currentPage * usersPerPage;
    const indexOfFirstUser = indexOfLastUser - usersPerPage;
    const currentUsers = filteredUsers.slice(indexOfFirstUser, indexOfLastUser);
    const totalPages = Math.ceil(filteredUsers.length / usersPerPage);

    const handlePageChange = (page: number) => {
        setCurrentPage(page);
    };

    const goToFirstPage = () => setCurrentPage(1);
    const goToLastPage = () => setCurrentPage(totalPages);
    const goToPreviousPage = () => setCurrentPage(prev => Math.max(prev - 1, 1));
    const goToNextPage = () => setCurrentPage(prev => Math.min(prev + 1, totalPages));

    if (loading) {
        return (
            <div className='flex justify-center w-full p-6'>
                <div className='space-y-6 w-full max-w-6xl'>
                    <div className="animate-pulse">
                        <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
                        <div className="space-y-3">
                            {[...Array(5)].map((_, i) => (
                                <div key={i} className="h-16 bg-gray-200 rounded"></div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className='flex justify-center w-full p-6'>
                <div className='space-y-6 w-full max-w-6xl'>
                    <Alert severity="error" icon={<ExclamationTriangleIcon className="h-5 w-5" />}>
                        {error}
                    </Alert>
                </div>
            </div>
        );
    }

    return (
        <div className='flex justify-center w-full p-6'>
            <div className='space-y-6 w-full max-w-6xl'>
                {/* Header Section */}
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-3">
                                <UserGroupIcon className="h-8 w-8 text-blue-600" />
                                Manage User Roles
                            </h1>
                            <p className="text-gray-600 mt-2">
                                Promote users to Super Accountant status or manage their roles
                            </p>
                        </div>
                        <div className="text-right">
                            <div className="text-3xl font-bold text-blue-600">
                                {users.length}
                            </div>
                            <div className="text-sm text-gray-500">Total Users</div>
                        </div>
                    </div>
                </div>

                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <div className="flex items-center">
                            <div className="p-2 bg-blue-100 rounded-lg">
                                <UserIcon className="h-6 w-6 text-blue-600" />
                            </div>
                            <div className="ml-4">
                                <p className="text-sm font-medium text-gray-600">Regular Accountants</p>
                                <p className="text-2xl font-bold text-gray-900">
                                    {users.filter(user => user.role === Roles.ACCOUNTANT).length}
                                </p>
                            </div>
                        </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <div className="flex items-center">
                            <div className="p-2 bg-purple-100 rounded-lg">
                                <UserGroupIcon className="h-6 w-6 text-purple-600" />
                            </div>
                            <div className="ml-4">
                                <p className="text-sm font-medium text-gray-600">Super Accountants</p>
                                <p className="text-2xl font-bold text-gray-900">
                                    {users.filter(user => user.role === Roles.SUPER_ACCOUNTANT).length}
                                </p>
                            </div>
                        </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <div className="flex items-center">
                            <div className="p-2 bg-red-100 rounded-lg">
                                <ShieldCheckIcon className="h-6 w-6 text-red-600" />
                            </div>
                            <div className="ml-4">
                                <p className="text-sm font-medium text-gray-600">Root Admins</p>
                                <p className="text-2xl font-bold text-gray-900">
                                    {users.filter(user => user.role === Roles.ROOT_ADMIN).length}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Main Table */}
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                    <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
                        <div className="flex items-center justify-between">
                            <div>
                                <h2 className="text-lg font-semibold text-gray-900">User Role Management</h2>
                                <p className="text-sm text-gray-600 mt-1">
                                    Click on the role dropdown to change a user&apos;s status
                                </p>
                            </div>
                            <div className="flex items-center space-x-4">
                                <div className="relative">
                                    <input
                                        type="text"
                                        placeholder="Search users..."
                                        value={searchTerm}
                                        onChange={(e) => {
                                            setSearchTerm(e.target.value);
                                            setCurrentPage(1); // Reset to first page when searching
                                        }}
                                        className="w-64 px-4 py-2 border border-gray-300 rounded-md bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                                    />
                                    {searchTerm && (
                                        <button
                                            onClick={() => {
                                                setSearchTerm('');
                                                setCurrentPage(1);
                                            }}
                                            className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                                            title="Clear search"
                                        >
                                            ✕
                                        </button>
                                    )}
                                </div>
                                <div className="text-sm text-gray-600">
                                    {filteredUsers.length} of {users.length} users
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <Table>
                        <TableHeader>
                            <TableRow className="bg-gray-50">
                                <TableHead className="font-semibold text-gray-700">User</TableHead>
                                <TableHead className="font-semibold text-gray-700">Contact</TableHead>
                                <TableHead className="font-semibold text-gray-700">Current Role</TableHead>
                                <TableHead className="font-semibold text-gray-700 text-center">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {currentUsers.map((user) => (
                                <TableRow key={user.id} className="hover:bg-gray-50 transition-colors">
                                    <TableCell>
                                        <div className="flex items-center space-x-3">
                                            <div className="flex-shrink-0">
                                                {getStatusIcon(user)}
                                            </div>
                                            <div>
                                                <div className="font-medium text-gray-900">
                                                    {user.first_name} {user.last_name}
                                                </div>
                                                <div className="text-sm text-gray-500">
                                                    ID: {user.id.slice(0, 8)}...
                                                    {user.is_accountant && (
                                                        <span className="ml-2 text-blue-600">• Accountant</span>
                                                    )}
                                                </div>
                                            </div>
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <div className="text-sm">
                                            <div className="text-gray-900">{user.email}</div>
                                            <div className="text-gray-500">
                                                {user.role === Roles.ROOT_ADMIN ? 'System Administrator' : 
                                                 user.role === Roles.SUPER_ACCOUNTANT ? 'Team Lead' : 'Team Member'}
                                            </div>
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        {user.role === Roles.ROOT_ADMIN ? 
                                            getRoleChip(Roles.ROOT_ADMIN)
                                        : 
                                            <Select
                                                value={user.role || Roles.ACCOUNTANT}
                                                onChange={(e) => handleChange(e.target.value, user)}
                                                size="small"
                                                disabled={updatingId === user.id}
                                                sx={{
                                                    '& .MuiSelect-select': {
                                                        padding: '4px 8px',
                                                        fontSize: '0.875rem'
                                                    }
                                                }}
                                            >
                                                {roleOptions.map((option) => (
                                                    <MenuItem key={option.value} value={option.value}>
                                                        {option.label}
                                                    </MenuItem>
                                                ))}
                                            </Select>}
                                    </TableCell>
                                    <TableCell className="text-center">
                                        {updatingId === user.id ? (
                                            <div className="flex items-center justify-center">
                                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                                                <span className="ml-2 text-sm text-gray-500">Updating...</span>
                                            </div>
                                        ) : (
                                            <div className="flex items-center justify-center space-x-2">
                                                {user.role === Roles.SUPER_ACCOUNTANT && (
                                                    <Tooltip title="Super Accountant - Can manage other accountants">
                                                        <CheckCircleSolid className="h-5 w-5 text-orange-500" />
                                                    </Tooltip>
                                                )}
                                                {user.role === Roles.ACCOUNTANT && (
                                                    <Tooltip title="Regular Accountant">
                                                        <UserIcon className="h-5 w-5 text-blue-500" />
                                                    </Tooltip>
                                                )}
                                                {user.role === Roles.ROOT_ADMIN && (
                                                    <Tooltip title="Root Administrator - Full system access">
                                                        <ShieldCheckIcon className="h-5 w-5 text-purple-500" />
                                                    </Tooltip>
                                                )}
                                            </div>
                                        )}
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                    
                    {/* Pagination Controls */}
                    {totalPages > 1 && (
                        <div className="px-6 py-4 border-t border-gray-200 bg-gray-50">
                            <div className="flex items-center justify-between">
                                <div className="text-sm text-gray-700">
                                    Showing {indexOfFirstUser + 1} to {Math.min(indexOfLastUser, filteredUsers.length)} of {filteredUsers.length} users
                                </div>
                                <div className="flex items-center space-x-2">
                                    {/* First Page Button */}
                                    <button
                                        onClick={goToFirstPage}
                                        disabled={currentPage === 1}
                                        className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                                    >
                                        First
                                    </button>
                                    
                                    {/* Previous Page Button */}
                                    <button
                                        onClick={goToPreviousPage}
                                        disabled={currentPage === 1}
                                        className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                                    >
                                        Previous
                                    </button>
                                    
                                    {/* Page Numbers */}
                                    <div className="flex items-center space-x-1">
                                        {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                                            <button
                                                key={page}
                                                onClick={() => handlePageChange(page)}
                                                className={`px-3 py-2 text-sm font-medium rounded-md ${
                                                    currentPage === page
                                                        ? 'bg-gradient-to-r from-orange-500 to-purple-500 text-white'
                                                        : 'text-gray-500 bg-white border border-gray-300 hover:bg-gray-50'
                                                }`}
                                            >
                                                {page}
                                            </button>
                                        ))}
                                    </div>
                                    
                                    {/* Next Page Button */}
                                    <button
                                        onClick={goToNextPage}
                                        disabled={currentPage === totalPages}
                                        className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                                    >
                                        Next
                                    </button>
                                    
                                    {/* Last Page Button */}
                                    <button
                                        onClick={goToLastPage}
                                        disabled={currentPage === totalPages}
                                        className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                                    >
                                        Last
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                {/* Success/Error Messages */}
                <Snackbar
                    open={!!successMessage}
                    autoHideDuration={4000}
                    onClose={() => setSuccessMessage(null)}
                    anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
                >
                    <Alert 
                        onClose={() => setSuccessMessage(null)} 
                        severity="success" 
                        icon={<CheckCircleIcon className="h-5 w-5" />}
                        sx={{ width: '100%' }}
                    >
                        {successMessage}
                    </Alert>
                </Snackbar>

                <Snackbar
                    open={!!error}
                    autoHideDuration={6000}
                    onClose={() => setError(null)}
                    anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
                >
                    <Alert 
                        onClose={() => setError(null)} 
                        severity="error" 
                        icon={<XCircleIcon className="h-5 w-5" />}
                        sx={{ width: '100%' }}
                    >
                        {error}
                    </Alert>
                </Snackbar>
            </div>
        </div>
    );
};

export default ManageSuperDashboard;
