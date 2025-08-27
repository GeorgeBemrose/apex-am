from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

# Junction table for many-to-many relationship between businesses and accountants
business_accountant = Table(
    'business_accountant',
    Base.metadata,
    Column('business_id', String, ForeignKey('businesses.id'), primary_key=True),
    Column('accountant_id', String, ForeignKey('accountants.id'), primary_key=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="accountant")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Accountant(Base):
    __tablename__ = "accountants"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    super_accountant_id = Column(String, ForeignKey("accountants.id"), nullable=True)
    is_super_accountant = Column(Boolean, default=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", primaryjoin="Accountant.user_id == User.id")
    super_accountant = relationship("Accountant", remote_side=[id], backref="subordinate_accountants")
    # Many-to-many relationship with businesses
    businesses = relationship("Business", secondary=business_accountant, back_populates="accountants")

class Business(Base):
    __tablename__ = "businesses"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    # Keep the primary accountant for backward compatibility
    accountant_id = Column(String, ForeignKey("accountants.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    owner = relationship("User", backref="owned_businesses")
    # Primary accountant (for backward compatibility)
    accountant = relationship("Accountant", foreign_keys=[accountant_id], backref="primary_managed_businesses")
    # Multiple accountants through junction table
    accountants = relationship("Accountant", secondary=business_accountant, back_populates="businesses")

class BusinessFinancialMetrics(Base):
    __tablename__ = "business_financial_metrics"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    revenue = Column(Integer, default=0)
    gross_profit = Column(Integer, default=0)
    net_profit = Column(Integer, default=0)
    total_costs = Column(Integer, default=0)
    percentage_change_revenue = Column(Integer, default=0)
    percentage_change_gross_profit = Column(Integer, default=0)
    percentage_change_net_profit = Column(Integer, default=0)
    percentage_change_total_costs = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    business = relationship("Business", backref="financial_metrics")

class BusinessMetrics(Base):
    __tablename__ = "business_metrics"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    documents_due = Column(Integer, default=0)
    outstanding_invoices = Column(Integer, default=0)
    pending_approvals = Column(Integer, default=0)
    accounting_year_end = Column(String, default="31/12/2024")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    business = relationship("Business", backref="metrics")