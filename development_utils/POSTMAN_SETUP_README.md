# Apex AM API - Postman Collection Setup Guide

This guide will help you set up Postman to test all the APIs in the Apex AM backend system.

## Files Included

1. **`Apex_AM_API_Collection.postman_collection.json`** - Complete API collection with all endpoints
2. **`Apex_AM_Environment.postman_environment.json`** - Environment variables for testing
3. **`POSTMAN_SETUP_README.md`** - This setup guide

## Prerequisites

- [Postman](https://www.postman.com/downloads/) installed on your machine
- Apex AM backend running locally on `http://localhost:8000`
- Valid admin credentials for authentication

## Setup Instructions

### Step 1: Import the Collection

1. Open Postman
2. Click **Import** button (top left)
3. Drag and drop `Apex_AM_API_Collection.postman_collection.json` or click to browse and select it
4. The collection will appear in your Collections panel

### Step 2: Import the Environment

1. In Postman, click **Import** again
2. Drag and drop `Apex_AM_Environment.postman_environment.json` or click to browse and select it
3. The environment will appear in your Environments panel

### Step 3: Select the Environment

1. In the top-right corner of Postman, click the environment dropdown
2. Select **"Apex AM Environment"**
3. This will activate all the environment variables

### Step 4: Configure Environment Variables

1. Click the **Environment** dropdown again and select **"Manage Environments"**
2. Click on **"Apex AM Environment"** to edit it
3. Update the following variables:

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `base_url` | Your backend server URL | `http://localhost:8000` |
| `admin_email` | Admin user email | `admin@example.com` |
| `admin_password` | Admin user password | `password` |

4. Click **Save** to apply changes

## API Testing Workflow

### 1. Authentication (Required First Step)

**Start with one of these endpoints to get an access token:**

- **Login with Form Data**: `POST /auth/login`
  - Uses form-encoded data with email as username
  - Content-Type: `application/x-www-form-urlencoded`

- **Login with JSON**: `POST /auth/login-json`
  - Uses JSON payload with email and password
  - Content-Type: `application/json`

**Important**: The access token is automatically saved to the `access_token` environment variable when you successfully login.

### 2. Testing Protected Endpoints

After authentication, you can test all other endpoints. The collection includes:

#### Users Management
- Create, read, update, delete users
- Assign roles to users
- Get user businesses

#### Businesses Management
- Create, read, update, delete businesses
- Assign/remove accountants from businesses

#### Accountants Management
- Create, read, update, delete accountants
- Assign/remove super accountants

### 3. Using Dynamic Variables

The collection uses these environment variables that you can update as needed:

| Variable | Usage |
|----------|-------|
| `{{user_id}}` | ID of a user for testing |
| `{{business_id}}` | ID of a business for testing |
| `{{accountant_id}}` | ID of an accountant for testing |
| `{{super_accountant_id}}` | ID of a super accountant for testing |

## API Endpoints Overview

### Authentication
- `POST /auth/login` - Login with form data
- `POST /auth/login-json` - Login with JSON

### Health & Info
- `GET /` - Root endpoint with API info
- `GET /health` - Health check

### Users
- `POST /users/` - Create user (Root Admin only)
- `GET /users/` - Get users list (Super Accountant/Root Admin only)
- `GET /users/me` - Get current user info
- `GET /users/{user_id}` - Get specific user
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user (Root Admin only)
- `POST /users/{user_id}/assign-role` - Assign role to user
- `GET /users/{user_id}/businesses` - Get user's businesses

### Businesses
- `GET /businesses/` - Get businesses list
- `GET /businesses/{business_id}` - Get specific business
- `POST /businesses/` - Create business (Root Admin/Super Accountant only)
- `PUT /businesses/{business_id}` - Update business
- `DELETE /businesses/{business_id}` - Delete business
- `POST /businesses/{business_id}/assign-accountant` - Assign accountant
- `POST /businesses/{business_id}/remove-accountant` - Remove accountant

### Accountants
- `GET /accountants/` - Get accountants list
- `GET /accountants/{accountant_id}` - Get specific accountant
- `POST /accountants/` - Create accountant (Super Accountant/Root Admin only)
- `PUT /accountants/{accountant_id}` - Update accountant
- `DELETE /accountants/{accountant_id}` - Delete accountant
- `POST /accountants/{accountant_id}/assign-super` - Assign super accountant
- `POST /accountants/{accountant_id}/remove-super` - Remove super accountant

## Testing Tips

### 1. Start with Health Check
Test `GET /health` first to ensure your backend is running.

### 2. Authentication Flow
1. Use the login endpoint to get an access token
2. The token is automatically saved to environment variables
3. All subsequent requests will use this token

### 3. Role-Based Access
- **Root Admin**: Can access all endpoints
- **Super Accountant**: Can manage accountants and businesses
- **Accountant**: Limited access to own data

### 4. Error Handling
- Check response status codes
- Review error messages in response body
- Ensure proper authentication headers

### 5. Data Validation
- Use the example request bodies as templates
- Modify data according to your testing needs
- Check required fields in the schemas

## Troubleshooting

### Common Issues

1. **401 Unauthorized**
   - Check if your access token is valid
   - Re-authenticate if needed
   - Verify token format: `Bearer <token>`

2. **403 Forbidden**
   - Check user role permissions
   - Ensure you have the required access level

3. **404 Not Found**
   - Verify the endpoint URL
   - Check if the resource ID exists
   - Ensure proper path parameters

4. **500 Internal Server Error**
   - Check backend logs
   - Verify database connection
   - Check request payload format

### Environment Variables Not Working
- Ensure the environment is selected
- Check variable names match exactly (case-sensitive)
- Verify variables are saved

## Security Notes

- Never commit real passwords to version control
- Use environment variables for sensitive data
- Regularly rotate access tokens
- Test with non-production data

## Support

If you encounter issues:
1. Check the backend logs for detailed error messages
2. Verify all environment variables are set correctly
3. Ensure the backend is running and accessible
4. Check API documentation at `http://localhost:8000/docs`

## Next Steps

After setting up Postman:
1. Test authentication endpoints
2. Create test users and businesses
3. Test role-based access control
4. Validate all CRUD operations
5. Test error scenarios and edge cases

Happy testing! 🚀
