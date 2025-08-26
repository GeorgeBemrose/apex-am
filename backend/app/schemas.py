from marshmallow import Schema, fields
from typing import Optional, List
from datetime import datetime

# Base schemas
class UserBase(Schema):
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    role = fields.Str(required=True)

class UserCreate(Schema):
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    role = fields.Str(required=True)

class UserUpdate(Schema):
    username = fields.Str()
    email = fields.Str()
    role = fields.Str()
    is_active = fields.Bool()

class UserResponse(Schema):
    id = fields.Int(required=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    role = fields.Str(required=True)
    is_active = fields.Bool(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime()

# Accountant schemas
class AccountantBase(Schema):
    user_id = fields.Int(required=True)
    super_accountant_id = fields.Int()
    is_super_accountant = fields.Bool(default=False)
    first_name = fields.Str()
    last_name = fields.Str()

class AccountantCreate(Schema):
    user_id = fields.Int(required=True)
    super_accountant_id = fields.Int()
    is_super_accountant = fields.Bool(default=False)
    first_name = fields.Str()
    last_name = fields.Str()

class AccountantUpdate(Schema):
    super_accountant_id = fields.Int()
    is_super_accountant = fields.Bool()
    first_name = fields.Str()
    last_name = fields.Str()

class AccountantResponse(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    super_accountant_id = fields.Int()
    is_super_accountant = fields.Bool(required=True)
    first_name = fields.Str()
    last_name = fields.Str()
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime()
    user = fields.Nested(UserResponse, required=True)

# Financial Metrics schemas
class BusinessFinancialMetricsBase(Schema):
    revenue = fields.Float(required=True)
    gross_profit = fields.Float(required=True)
    net_profit = fields.Float(required=True)
    total_costs = fields.Float(required=True)
    percentage_change_revenue = fields.Float(required=True)
    percentage_change_gross_profit = fields.Float(required=True)
    percentage_change_net_profit = fields.Float(required=True)
    percentage_change_total_costs = fields.Float(required=True)

class BusinessFinancialMetricsResponse(BusinessFinancialMetricsBase):
    id = fields.Int(required=True)
    business_id = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime()

# Business Metrics schemas
class BusinessMetricsBase(Schema):
    documents_due = fields.Int(required=True)
    outstanding_invoices = fields.Int(required=True)
    pending_approvals = fields.Int(required=True)
    accounting_year_end = fields.Date(required=True)

class BusinessMetricsResponse(BusinessMetricsBase):
    id = fields.Int(required=True)
    business_id = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime()

# Business schemas
class BusinessBase(Schema):
    name = fields.Str(required=True)
    description = fields.Str()
    owner_id = fields.Int(required=True)
    accountant_id = fields.Int()

class BusinessCreate(Schema):
    name = fields.Str(required=True)
    description = fields.Str()
    owner_id = fields.Int(required=True)
    accountant_id = fields.Int()

class BusinessUpdate(Schema):
    name = fields.Str()
    description = fields.Str()
    accountant_id = fields.Int()
    is_active = fields.Bool()

class BusinessResponse(BusinessBase):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str()
    owner_id = fields.Int(required=True)
    accountant_id = fields.Int()
    is_active = fields.Bool(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime()
    owner = fields.Nested(UserResponse, required=True)
    accountant = fields.Nested(AccountantResponse)
    financial_metrics = fields.Nested(BusinessFinancialMetricsResponse)
    metrics = fields.Nested(BusinessMetricsResponse)

# Authentication schemas
class Token(Schema):
    access_token = fields.Str(required=True)
    token_type = fields.Str(required=True)

class TokenData(Schema):
    username = fields.Str()

# Login schema
class UserLogin(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

# Role assignment schema
class RoleAssignment(Schema):
    user_id = fields.Int(required=True)
    new_role = fields.Str(required=True)
    super_accountant_id = fields.Int()
