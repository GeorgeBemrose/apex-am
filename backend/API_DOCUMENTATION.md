# Apex AM API Documentation

## Overview

The Apex AM API is a comprehensive RESTful API for managing accounting operations, user management, and business relationships. This API provides secure, role-based access control for accountants, businesses, and administrators.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.apex-am.com`

## Authentication

The API uses JWT (JSON Web Token) authentication. Most endpoints require a valid JWT token in the Authorization header.

### Getting a Token

#### OAuth2 Form Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=john.doe@example.com&password=securepassword123
```

#### JSON Login
```http
POST /auth/login-json
Content-Type: application/json

{
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

### Using the Token

Include the token in the Authorization header:
```http
Authorization: Bearer <your_jwt_token>
```

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/login` | OAuth2 form login | No |
| POST | `/auth/login-json` | JSON-based login | No |

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/users/` | List all users | Yes |
| GET | `/users/{user_id}` | Get user details | Yes |
| POST | `/users/` | Create new user | Yes |
| PUT | `/users/{user_id}` | Update user | Yes |
| DELETE | `/users/{user_id}` | Delete user | Yes |

### Accountants

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/accountants/` | List all accountants | Yes |
| GET | `/accountants/{accountant_id}` | Get accountant details | Yes |
| POST | `/accountants/` | Create new accountant | Yes |
| PUT | `/accountants/{accountant_id}` | Update accountant | Yes |
| DELETE | `/accountants/{accountant_id}` | Delete accountant | Yes |

### Businesses

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/businesses/` | List all businesses | Yes |
| GET | `/businesses/{business_id}` | Get business details | Yes |
| POST | `/businesses/` | Create new business | Yes |
| PUT | `/businesses/{business_id}` | Update business | Yes |
| DELETE | `/businesses/{business_id}` | Delete business | Yes |

### API Information

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | API root information | No |
| GET | `/health` | Health check | No |
| GET | `/api-info` | Detailed API information | No |
| GET | `/docs` | Swagger UI documentation | No |
| GET | `/redoc` | ReDoc documentation | No |
| GET | `/openapi.json` | OpenAPI schema | No |

## Data Models

### User

```json
{
  "id": "user_12345",
  "username": "john_doe",
  "email": "john.doe@example.com",
  "role": "accountant",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T14:45:00Z"
}
```

### Accountant

```json
{
  "id": "acc_12345",
  "first_name": "John",
  "last_name": "Doe",
  "is_super_accountant": false,
  "user_id": "user_12345",
  "super_accountant_id": "acc_67890",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T14:45:00Z",
  "user": {
    "id": "user_12345",
    "username": "john_doe",
    "email": "john.doe@example.com",
    "role": "accountant",
    "is_active": true
  }
}
```

### Business

```json
{
  "id": "business_12345",
  "name": "Acme Corporation",
  "description": "A leading technology company",
  "owner_id": "user_12345",
  "accountant_id": "acc_12345",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T14:45:00Z"
}
```

### Business Financial Metrics

```json
{
  "id": "metrics_12345",
  "revenue": 1000000,
  "gross_profit": 600000,
  "net_profit": 400000,
  "total_costs": 600000,
  "percentage_change_revenue": 15,
  "percentage_change_gross_profit": 12,
  "percentage_change_net_profit": 18,
  "percentage_change_total_costs": -5,
  "business_id": "business_12345"
}
```

## Error Handling

The API returns standard HTTP status codes and detailed error messages.

### Common Error Responses

#### 400 Bad Request
```json
{
  "detail": "Email and password are required",
  "error_code": 400,
  "timestamp": "2024-01-20T14:45:00Z",
  "path": "/auth/login-json"
}
```

#### 401 Unauthorized
```json
{
  "detail": "Incorrect email or password",
  "error_code": 401,
  "timestamp": "2024-01-20T14:45:00Z",
  "path": "/auth/login"
}
```

#### 404 Not Found
```json
{
  "detail": "User not found",
  "error_code": 404,
  "timestamp": "2024-01-20T14:45:00Z",
  "path": "/users/99999"
}
```

#### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "invalid email format",
      "type": "value_error.email"
    }
  ]
}
```

## Pagination

List endpoints support pagination with the following query parameters:

- `skip`: Number of items to skip (default: 0)
- `limit`: Maximum number of items to return (default: 100, max: 1000)

Example:
```http
GET /users/?skip=0&limit=10
```

## Filtering and Sorting

Some endpoints support filtering and sorting:

```http
GET /businesses/?is_active=true&sort_by=name&sort_order=asc
```

## Response Headers

All responses include standard headers:

- `Content-Type: application/json`
- `X-Request-ID`: Unique request identifier for tracking
- `X-RateLimit-Limit`: Rate limit for the endpoint
- `X-RateLimit-Remaining`: Remaining requests in the current period
- `X-RateLimit-Reset`: Time when the rate limit resets

## Testing

### Test Environment

Use the test environment for development and testing:

```bash
# Set environment variables
export ENVIRONMENT=test
export DATABASE_URL=sqlite:///./test.db

# Run tests
pytest
```

### Postman Collection

Import the provided Postman collection for testing:
- Collection: `development_utils/Apex_AM_API_Collection.postman_collection.json`
- Environment: `development_utils/Apex_AM_Environment.postman_environment.json`

## Support

- **Documentation**: `/docs` (Swagger UI)
- **API Schema**: `/openapi.json`
- **Issues**: GitHub Issues
- **Email**: dev@apex-am.com
- **Support Portal**: https://apex-am.com/support

## Changelog

### v1.0.0 (2024-01-20)
- Initial API release
- JWT authentication
- User management
- Accountant hierarchy
- Business management
- Financial metrics tracking

## License

This API is licensed under the MIT License. See the LICENSE file for details.
