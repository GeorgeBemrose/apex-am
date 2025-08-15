export function authorize(user, requiredPermission) {
    if (!user.permissions.includes(requiredPermission)) {
        throw new Error('Access denied');
    }
}