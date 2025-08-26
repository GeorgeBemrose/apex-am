from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  # "root_admin", "super_accountant", "accountant"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    businesses = relationship("Business", back_populates="owner")
    # Explicitly specify foreign_keys to avoid ambiguity
    managed_accountants = relationship(
        "Accountant", 
        back_populates="super_accountant",
        foreign_keys="Accountant.super_accountant_id"
    )

class Accountant(Base):
    __tablename__ = "accountants"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    super_accountant_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_super_accountant = Column(Boolean, default=False)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    super_accountant = relationship(
        "User", 
        foreign_keys=[super_accountant_id], 
        back_populates="managed_accountants"
    )
    businesses = relationship("Business", back_populates="accountant")

class Business(Base):
    __tablename__ = "businesses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    accountant_id = Column(Integer, ForeignKey("accountants.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="businesses")
    accountant = relationship("Accountant", back_populates="businesses")
    financial_metrics = relationship("BusinessFinancialMetrics", back_populates="business", uselist=False)
    metrics = relationship("BusinessMetrics", back_populates="business", uselist=False)

class BusinessFinancialMetrics(Base):
    __tablename__ = "business_financial_metrics"
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), unique=True)
    revenue = Column(Float)
    gross_profit = Column(Float)
    net_profit = Column(Float)
    total_costs = Column(Float)
    percentage_change_revenue = Column(Float)
    percentage_change_gross_profit = Column(Float)
    percentage_change_net_profit = Column(Float)
    percentage_change_total_costs = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    business = relationship("Business", back_populates="financial_metrics")

class BusinessMetrics(Base):
    __tablename__ = "business_metrics"
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), unique=True)
    documents_due = Column(Integer)
    outstanding_invoices = Column(Integer)
    pending_approvals = Column(Integer)
    accounting_year_end = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    business = relationship("Business", back_populates="metrics")