# Apex AM - Accounting Management System

A comprehensive accounting management system with role-based access control for accountants, businesses, and administrators. Built with FastAPI backend and Next.js frontend, containerized with Docker for easy deployment.

## 🚀 Quick Start

### Option 1: Docker (Recommended)

The easiest way to get started is using Docker:

```bash
# Start development environment
make dev-build

# Access the application:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs

# Stop services
make dev-down
```

### Option 2: Manual Setup

#### Frontend Development

1. Navigate to the frontend directory:
```bash
cd frontend
npm install
npm run dev
```

2. Create environment variables for local development:
```bash
# Create .env.local file
cat > .env.local << EOF
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_TIMEOUT=10000
EOF
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

#### Backend Setup

1. Create a Python virtual environment:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies and run:
```bash
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔐 Demo Accounts

| Role | Email | Password |
|------|-------|----------|
| Root Admin | admin@example.com | password |
| Super Accountant | super@example.com | password |
| Accountant | accountant@example.com | password |

## 🏗️ Project Structure

```
apex-am/
├── backend/           # FastAPI backend application
│   ├── app/          # Main application code
│   ├── tests/        # Test suite
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/          # Next.js frontend application
│   ├── app/          # Next.js app directory
│   ├── components/   # React components
│   ├── lib/          # Utility libraries
│   ├── types/        # TypeScript type definitions
│   └── Dockerfile
├── development_utils/ # Postman collections and utilities
├── docker-compose.yml # Docker configuration
├── Makefile          # Docker and development commands
└── README.md         # This file
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite
- **Frontend**: Next.js 15, TypeScript, Tailwind CSS
- **Database**: SQLite (development), PostgreSQL ready (production)
- **Authentication**: JWT-based auth system
- **Containerization**: Docker & Docker Compose

## 🐳 Docker Commands

```bash
# Development
make dev-build          # Build and start development environment
make dev-logs           # View development logs
make dev-down           # Stop development environment

# General
make build              # Build all Docker images
make clean              # Stop and remove all containers
make logs               # View all service logs
make test               # Run tests in development container
make shell              # Open shell in backend container
make status             # View service status
make restart            # Restart services
make stats              # View resource usage
```

## 🔌 API Endpoints

### Authentication
- `POST /auth/login` - OAuth2 form login
- `POST /auth/login-json` - JSON-based login

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

### Businesses
- `POST /businesses/` - Create business
- `GET /businesses/` - List businesses (role-based access)
- `GET /businesses/my-businesses` - Get own businesses
- `GET /businesses/{business_id}` - Get specific business
- `PUT /businesses/{business_id}` - Update business
- `DELETE /businesses/{business_id}` - Delete business

### API Documentation
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation
- `GET /openapi.json` - OpenAPI schema

## 🔐 Role-Based Access Control

### Root Admin
- **Full system access** to all endpoints and data
- **User Management**: Create, read, update, delete any user
- **Role Assignment**: Can assign any role to any user
- **Accountant Management**: Full CRUD operations on all accountants
- **Business Management**: Access to all businesses and financial data

### Super Accountant
- **User Management**: View and update users (cannot create/delete)
- **Accountant Supervision**: Manage accountants under their supervision
- **Business Access**: View and manage businesses of supervised accountants
- **Financial Data**: Access to business metrics and financial insights

### Accountant
- **Business Management**: Only their own assigned businesses
- **Client Data**: Access to client financial information
- **Limited User Access**: View-only access to user information

## 🧪 Testing

### Backend Testing

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run specific test file
docker compose exec backend pytest tests/test_auth.py

# Open shell for manual testing
make shell
```

### Frontend Testing

```bash
cd frontend
npm run lint          # Run ESLint
npm run build         # Build for production
```

## 🔧 Configuration

### Environment Variables

#### Backend
```bash
# Database
DATABASE_URL=sqlite:///./apex_am.db

# Security
SECRET_KEY=dev-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS="http://localhost:3000,http://frontend:3000"

# Environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
```

#### Frontend
```bash
# API configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000  # For local development
NEXT_PUBLIC_API_TIMEOUT=10000

# Environment
NODE_ENV=development
NEXT_TELEMETRY_DISABLED=1
```

**Note**: Create a `.env.local` file in the `frontend/` directory for local development:
```bash
cd frontend
# Create .env.local manually with the values above
cat > .env.local << EOF
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_TIMEOUT=10000
EOF
```

### Environment Variables: Docker vs Local

**Docker Environment**: Most environment variables are configured in `docker-compose.yml` and are automatically available to containers.

**Local Development**: You'll need to create `.env.local` files for environment-specific configuration.

### Docker Configuration

The application uses multi-stage Docker builds:
- **Backend**: Python 3.11 with FastAPI and Uvicorn
- **Frontend**: Node.js 18 with Next.js standalone output
- **Database**: SQLite for development (easily configurable for PostgreSQL/MySQL)

## 📚 API Testing with Postman

Import the Postman collection from `development_utils/`:
1. **`Apex_AM_API_Collection.postman_collection.json`** - Complete API collection
2. **`Apex_AM_Environment.postman_environment.json`** - Environment variables

### Testing Workflow
1. **Authentication**: Use `/auth/login-json` to get access token
2. **Protected Endpoints**: Token automatically included in requests
3. **Role Testing**: Test different user roles and permissions

## 🗄️ Database Schema

### Users Table
- `id`: Primary key (UUID)
- `email`: Unique email address
- `hashed_password`: Securely hashed password using bcrypt
- `role`: User role (root_admin, super_accountant, accountant)
- `is_active`: Account status
- `created_at`, `updated_at`: Timestamps

### Accountants Table
- `id`: Primary key (UUID)
- `user_id`: Reference to User table
- `first_name`, `last_name`: Accountant's name
- `super_accountant_id`: Reference to supervising super accountant
- `is_super_accountant`: Boolean flag for role distinction
- `created_at`, `updated_at`: Timestamps

### Businesses Table
- `id`: Primary key (UUID)
- `name`: Business name
- `description`: Business description
- `owner_id`: Reference to User table (business owner)
- `accountant_id`: Reference to Accountant table (assigned accountant)
- `is_active`: Business status
- `created_at`, `updated_at`: Timestamps

## 🚀 Development Workflow

### Hot Reloading
- **Backend**: Uvicorn with `--reload` flag for automatic restart
- **Frontend**: Next.js development server with hot reloading (`npm run dev`)
- **Docker**: Volume mounts for immediate code changes
- **Development Mode**: Uses `Dockerfile.dev` for optimal development experience

### Code Quality
```bash
# Backend
docker compose exec backend black .          # Format Python code
docker compose exec backend flake8 .         # Lint Python code

# Frontend
cd frontend
npm run lint                                # Run ESLint
npm run build                               # Build for production
```

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Check what's using the port
lsof -i :3000
lsof -i :8000

# Stop conflicting services or change ports in docker-compose.yml
```

#### Frontend Build Issues
```bash
# Rebuild frontend container
docker compose build --no-cache frontend

# Check frontend logs
docker compose logs frontend
```

#### CORS Issues
- Ensure `CORS_ORIGINS` includes your frontend URL
- Check that frontend uses correct backend URL (`http://backend:8000` in Docker)

#### Database Issues
```bash
# Check backend logs
docker compose logs backend

# Rebuild containers
make clean
make dev-build
```

### Debug Commands
```bash
# Enter running container
make shell

# View container details
docker inspect apex_am_backend

# Check container resource usage
docker stats apex_am_backend apex_am_frontend
```

## 🚀 Production Deployment

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

## 🔮 Future Enhancements

### Multi-Firm Support
- **Tenant Isolation**: Implement multi-tenancy with separate schemas
- **Shared Services**: Common authentication across firms
- **Data Partitioning**: Route requests to appropriate firm's data

### Performance Optimization
- **Database Scaling**: Connection pooling, read replicas, caching
- **Application Scaling**: Horizontal scaling, async processing
- **CDN Integration**: Static asset delivery optimization

### Security Enhancements
- **Multi-Factor Authentication (MFA)**: TOTP, SMS, or hardware tokens
- **OAuth2 Integration**: Support for Google, Microsoft, or custom providers
- **Field-Level Encryption**: Sensitive data encryption at rest

## 📋 Contributing

1. Follow the existing code style
2. Add tests for new functionality
3. Update documentation for API changes
4. Ensure all tests pass before submitting
5. Test Docker builds and deployments

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Postman Learning Center](https://learning.postman.com/)

## 📄 License

This project is licensed under the MIT License.

---

**Happy coding! 🚀**
