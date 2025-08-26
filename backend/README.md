# Apex AM Backend API

A comprehensive FastAPI backend for an Accounting Management System with Role-Based Access Control (RBAC).

## Features

### 🔐 Authentication & Authorization
- **JWT-based authentication** with secure token management
- **Role-based access control** with three distinct roles:
  - **Root Admin**: Full system access
  - **Super Accountant**: Can manage accountants and their businesses
  - **Accountant**: Can only manage their own businesses

### 🏢 Business Management
- Complete CRUD operations for businesses
- Business assignment to accountants
- Role-based business access control

### 👥 User & Accountant Management
- User creation and role assignment
- Accountant management with super accountant oversight
- Hierarchical permission system

### 🗄️ Database
- SQLAlchemy ORM with SQLite (easily configurable for PostgreSQL/MySQL)
- Automatic database table creation
- Sample data initialization

### 📚 API Documentation
- **Swagger/OpenAPI** auto-generated documentation at `/docs`
- **ReDoc** alternative documentation at `/redoc`
- Comprehensive endpoint descriptions

### 🧪 Testing
- Unit tests for critical backend logic
- Test database isolation
- Authentication and authorization testing

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python init_db.py
```

This creates the database with sample data and default users (matching frontend):
- **Root Admin**: `admin@example.com` / `password`
- **Super Accountant**: `super@example.com` / `password`
- **Accountant**: `accountant@example.com` / `password`

### 3. Run the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 4. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/login` - Login with form data
- `POST /auth/login-json` - Login with JSON

### Users
- `POST /users/` - Create user (Root Admin only)
- `GET /users/` - List users (Super Accountant or Root Admin)
- `GET /users/me` - Get current user info
- `GET /users/{user_id}` - Get specific user
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user (Root Admin only)
- `POST /users/{user_id}/assign-role` - Assign role to user

### Accountants
- `POST /accountants/` - Create accountant (Root Admin only)
- `GET /accountants/` - List accountants
- `GET /accountants/my-accountants` - Get managed accountants
- `GET /accountants/{accountant_id}` - Get specific accountant
- `PUT /accountants/{accountant_id}` - Update accountant
- `DELETE /accountants/{accountant_id}` - Delete accountant
- `POST /accountants/{accountant_id}/assign-super` - Assign super accountant
- `POST /accountants/{accountant_id}/remove-super` - Remove super accountant

### Businesses
- `POST /businesses/` - Create business
- `GET /businesses/` - List businesses (role-based access)
- `GET /businesses/my-businesses` - Get own businesses
- `GET /businesses/{business_id}` - Get specific business
- `PUT /businesses/{business_id}` - Update business
- `DELETE /businesses/{business_id}` - Delete business
- `POST /businesses/{business_id}/assign-accountant` - Assign accountant
- `POST /businesses/{business_id}/remove-accountant` - Remove accountant

## Role-Based Access Control

### Root Admin
- Full access to all endpoints
- Can create, read, update, and delete any user, accountant, or business
- Can assign roles and manage the entire system

### Super Accountant
- Can view and manage users (except create/delete)
- Can manage accountants under their supervision
- Can view and manage businesses of their managed accountants
- Cannot access root admin functions

### Accountant
- Can only view and manage their own businesses
- Limited access to user management
- Cannot access other accountants' data

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `hashed_password`: Securely hashed password
- `role`: User role (root_admin, super_accountant, accountant)
- `is_active`: Account status
- `created_at`, `updated_at`: Timestamps

### Accountants Table
- `id`: Primary key
- `user_id`: Reference to User table
- `super_accountant_id`: Reference to supervising super accountant
- `is_super_accountant`: Boolean flag
- `created_at`, `updated_at`: Timestamps

### Businesses Table
- `id`: Primary key
- `name`: Business name
- `description`: Business description
- `owner_id`: Reference to User table (business owner)
- `accountant_id`: Reference to Accountant table (assigned accountant)
- `is_active`: Business status
- `created_at`, `updated_at`: Timestamps

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run specific test file
pytest app/tests/test_auth.py

# Run with coverage
pytest --cov=app

# Run with verbose output
pytest -v
```

## Configuration

The application uses environment variables for configuration. Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=sqlite:///./apex_am.db

# Security
SECRET_KEY=your-secure-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:3001"]

# Environment
ENVIRONMENT=development
DEBUG=true
```

## Production Deployment

### Security Considerations
1. **Change the SECRET_KEY** to a secure, random value
2. **Configure CORS_ORIGINS** to only allow your frontend domains
3. **Use a production database** (PostgreSQL/MySQL) instead of SQLite
4. **Enable HTTPS** in production
5. **Set DEBUG=false** in production

### Database Migration
For production databases, consider using Alembic for database migrations:

```bash
pip install alembic
alembic init alembic
# Configure alembic.ini and env.py
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Environment Variables
Set these in your production environment:
```bash
export DATABASE_URL="postgresql://user:password@localhost/apex_am"
export SECRET_KEY="your-production-secret-key"
export ENVIRONMENT="production"
export DEBUG="false"
```

## API Usage Examples

### Authentication
```bash
# Login to get access token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=password"
```

### Create Business (with authentication)
```bash
# First get token from login
TOKEN="your-access-token-here"

# Create business
curl -X POST "http://localhost:8000/businesses/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Business",
    "description": "A new business",
    "owner_id": 1
  }'
```

### Get Businesses
```bash
curl -X GET "http://localhost:8000/businesses/" \
  -H "Authorization: Bearer $TOKEN"
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure the database directory is writable
   - Check if SQLite is properly installed

2. **Import Errors**
   - Ensure you're in the correct directory
   - Check that all dependencies are installed

3. **Permission Errors**
   - Verify role-based access control is working
   - Check if the user has the required role

4. **Token Expiration**
   - Tokens expire after 30 minutes by default
   - Re-authenticate to get a new token

### Logs
Enable debug logging by setting `DEBUG=true` in your environment variables.

## Contributing

1. Follow the existing code style
2. Add tests for new functionality
3. Update documentation for API changes
4. Ensure all tests pass before submitting

## License

This project is licensed under the MIT License.
