import { Roles, RolePermissions } from './roles';

export const mockUsers = [
    { id: 1, name: 'Root Admin', email: 'admin@example.com', password: 'password', role: Roles.ROOT_ADMIN },
    { id: 2, name: 'Super Accountant', email: 'super@example.com', password: 'password', role: Roles.SUPER_ACCOUNTANT },
    { id: 3, name: 'Accountant', email: 'accountant@example.com', password: 'password', role: Roles.ACCOUNTANT },
];

export function authenticateUser(email, password) {
    const user = mockUsers.find((u) => u.email === email && u.password === password);
    if (!user) {
        return false;
    }
    return {
        ...user,
        permissions: RolePermissions[user.role],
    };
}