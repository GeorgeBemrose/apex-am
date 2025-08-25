import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button } from '@mui/material';

interface AccountantsDialogProps {
    open: boolean;
    onClose: () => void;
    name: string
}



const AccountantsDialog: React.FC<AccountantsDialogProps> = ({ open, onClose, name }) => {
    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>{name} - Accountants</DialogTitle>
            <DialogContent>
                <p>Details about accountants will go here.</p>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose} color="primary">
                    Close
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default AccountantsDialog;