import React, { useState } from 'react';
import { Container, Typography, Button, Select, MenuItem, FormControl, InputLabel } from '@mui/material';

const SuperAccountantDashboard = () => { // BEGIN:
    const [selectedAccountant, setSelectedAccountant] = useState<string>('');
    const [selectedBusiness, setSelectedBusiness] = useState<string>('');

    const accountants = ['Accountant 1', 'Accountant 2', 'Accountant 3'];
    const businesses = ['Business A', 'Business B', 'Business C'];

    const handleAssign = () => {
        // Logic to assign accountant to business
        console.log(`Assigned ${selectedAccountant} to ${selectedBusiness}`);
    };

    return (
        <Container>
            <Typography variant="h4" gutterBottom>
                Assign Accountants to Businesses
            </Typography>
            <FormControl fullWidth margin="normal">
                <InputLabel id="accountant-select-label">Select Accountant</InputLabel>
                <Select
                    labelId="accountant-select-label"
                    value={selectedAccountant}
                    onChange={(e) => setSelectedAccountant(e.target.value)}
                >
                    {accountants.map((accountant) => (
                        <MenuItem key={accountant} value={accountant}>
                            {accountant}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
            <FormControl fullWidth margin="normal">
                <InputLabel id="business-select-label">Select Business</InputLabel>
                <Select
                    labelId="business-select-label"
                    value={selectedBusiness}
                    onChange={(e) => setSelectedBusiness(e.target.value)}
                >
                    {businesses.map((business) => (
                        <MenuItem key={business} value={business}>
                            {business}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
            <Button variant="contained" color="primary" onClick={handleAssign}>
                Assign Accountant
            </Button>
        </Container>
    );
}; // END:

export default SuperAccountantDashboard;
