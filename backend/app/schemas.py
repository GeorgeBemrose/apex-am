from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Base schemas
class UserBase(BaseModel):
    username: str = Field(..., description="Unique username for the user", example="john_doe")
    email: str = Field(..., description="User's email address", example="john.doe@example.com")
    role: str = Field(..., description="User's role in the system", example="accountant")
    is_active: bool = Field(True, description="Whether the user account is active")

class UserCreate(UserBase):
    password: str = Field(..., description="User's password (will be hashed)", example="securepassword123", min_length=8)

class User(UserBase):
    id: str = Field(..., description="Unique identifier for the user", example="user_12345")
    created_at: Optional[datetime] = Field(None, description="Timestamp when user was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when user was last updated")

    class Config:
        schema_extra = {
            "example": {
                "id": "user_12345",
                "username": "john_doe",
                "email": "john.doe@example.com",
                "role": "accountant",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-20T14:45:00Z"
            }
        }

class AccountantBase(BaseModel):
    first_name: Optional[str] = Field(None, description="Accountant's first name", example="John")
    last_name: Optional[str] = Field(None, description="Accountant's last name", example="Doe")
    is_super_accountant: bool = Field(False, description="Whether this accountant has super privileges")

class AccountantCreate(AccountantBase):
    user_id: str = Field(..., description="ID of the associated user account", example="user_12345")
    super_accountant_id: Optional[str] = Field(None, description="ID of the supervising accountant", example="acc_67890")

class Accountant(AccountantBase):
    id: str = Field(..., description="Unique identifier for the accountant", example="acc_12345")
    user_id: str = Field(..., description="ID of the associated user account", example="user_12345")
    super_accountant_id: Optional[str] = Field(None, description="ID of the supervising accountant", example="acc_67890")
    created_at: Optional[datetime] = Field(None, description="Timestamp when accountant profile was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when accountant profile was last updated")
    user: Optional[User] = Field(None, description="Associated user account information")

    class Config:
        schema_extra = {
            "example": {
                "id": "acc_12345",
                "first_name": "John",
                "last_name": "Doe",
                "is_super_accountant": False,
                "user_id": "user_12345",
                "super_accountant_id": "acc_67890",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-20T14:45:00Z",
                "user": {
                    "id": "user_12345",
                    "username": "john_doe",
                    "email": "john.doe@example.com",
                    "role": "accountant",
                    "is_active": True
                }
            }
        }

class BusinessBase(BaseModel):
    name: str = Field(..., description="Business name", example="Acme Corporation")
    description: Optional[str] = Field(None, description="Business description", example="A leading technology company")
    owner_id: str = Field(..., description="ID of the business owner", example="user_12345")
    accountant_id: Optional[str] = Field(None, description="ID of the assigned accountant", example="acc_12345")
    is_active: bool = Field(True, description="Whether the business is active")

class BusinessCreate(BusinessBase):
    pass

class Business(BusinessBase):
    id: str = Field(..., description="Unique identifier for the business", example="business_12345")
    created_at: Optional[datetime] = Field(None, description="Timestamp when business was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when business was last updated")
    owner: Optional[User] = Field(None, description="Business owner information")
    accountant: Optional[Accountant] = Field(None, description="Assigned accountant information")
    accountants: Optional[List[Accountant]] = Field(None, description="List of all accountants associated with this business")

    class Config:
        schema_extra = {
            "example": {
                "id": "business_12345",
                "name": "Acme Corporation",
                "description": "A leading technology company",
                "owner_id": "user_12345",
                "accountant_id": "acc_12345",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-20T14:45:00Z"
            }
        }

class BusinessFinancialMetricsBase(BaseModel):
    revenue: int = Field(0, description="Total revenue in cents", example=1000000, ge=0)
    gross_profit: int = Field(0, description="Gross profit in cents", example=600000, ge=0)
    net_profit: int = Field(0, description="Net profit in cents", example=400000, ge=0)
    total_costs: int = Field(0, description="Total costs in cents", example=600000, ge=0)
    percentage_change_revenue: int = Field(0, description="Percentage change in revenue from previous period", example=15)
    percentage_change_gross_profit: int = Field(0, description="Percentage change in gross profit from previous period", example=12)
    percentage_change_net_profit: int = Field(0, description="Percentage change in net profit from previous period", example=18)
    percentage_change_total_costs: int = Field(0, description="Percentage change in total costs from previous period", example=-5)

class BusinessFinancialMetricsCreate(BusinessFinancialMetricsBase):
    business_id: str = Field(..., description="ID of the business these metrics belong to", example="business_12345")

class BusinessFinancialMetrics(BusinessFinancialMetricsBase):
    id: str = Field(..., description="Unique identifier for the financial metrics", example="metrics_12345")
    business_id: str = Field(..., description="ID of the business these metrics belong to", example="business_12345")
    created_at: Optional[datetime] = Field(None, description="Timestamp when metrics were created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when metrics were last updated")

    class Config:
        schema_extra = {
            "example": {
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
        }

class BusinessMetricsBase(BaseModel):
    documents_due: int = Field(0, description="Number of documents due", example=5, ge=0)
    outstanding_invoices: int = Field(0, description="Number of outstanding invoices", example=12, ge=0)
    pending_approvals: int = Field(0, description="Number of pending approvals", example=3, ge=0)
    accounting_year_end: str = Field("31/12/2024", description="Accounting year end date", example="31/12/2024")

class BusinessMetricsCreate(BusinessMetricsBase):
    business_id: str = Field(..., description="ID of the business these metrics belong to", example="business_12345")

class BusinessMetrics(BusinessMetricsBase):
    id: str = Field(..., description="Unique identifier for the business metrics", example="metrics_12345")
    business_id: str = Field(..., description="ID of the business these metrics belong to", example="business_12345")
    created_at: Optional[datetime] = Field(None, description="Timestamp when metrics were created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when metrics were last updated")

# Authentication schemas
class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token", example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(..., description="Type of token", example="bearer")

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huLmRvZUBleGFtcGxlLmNvbSIsImV4cCI6MTcwNTc2NzIwMH0.signature",
                "token_type": "bearer"
            }
        }

class TokenData(BaseModel):
    username: str = Field(..., description="Username from token", example="john_doe")

# Login schema
class LoginRequest(BaseModel):
    email: str = Field(..., description="User's email address", example="john.doe@example.com")
    password: str = Field(..., description="User's password", example="securepassword123", min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "securepassword123"
            }
        }

# Business management schemas
class AssignAccountantRequest(BaseModel):
    accountant_id: str = Field(..., description="ID of the accountant to assign", example="acc_12345")

# Role assignment schema
class RoleAssignment(BaseModel):
    new_role: str = Field(..., description="New role to assign to the user", example="super_accountant")
    super_accountant_id: Optional[str] = Field(None, description="ID of the supervising accountant", example="acc_67890")
