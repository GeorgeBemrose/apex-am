export const Roles = {
    ROOT_ADMIN: 'root_admin',
    SUPER_ACCOUNTANT: 'super_accountant',
    ACCOUNTANT: 'accountant',
};

export const Permissions = {
    FULL_ACCESS: 'full_access',
    MANAGE_ACCOUNTANTS: 'manage_accountants',
    MANAGE_BUSINESSES: 'manage_businesses',
};

export const RolePermissions = {
    [Roles.ROOT_ADMIN]: [Permissions.FULL_ACCESS],
    [Roles.SUPER_ACCOUNTANT]: [Permissions.MANAGE_ACCOUNTANTS, Permissions.MANAGE_BUSINESSES],
    [Roles.ACCOUNTANT]: [Permissions.MANAGE_BUSINESSES],
};
