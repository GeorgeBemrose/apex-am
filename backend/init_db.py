#!/usr/bin/env python3
"""
Database initialization script for Apex AM API.
This script creates the database tables and populates them with real test data from frontend.
"""

import sys
import os
import json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal
from app.models import Base, User, Accountant, Business, BusinessFinancialMetrics, BusinessMetrics
from app.auth import get_password_hash
from sample_data.businesses import businesses_data
from sample_data.accountants import accountants_data

def create_sample_data():
    """Create sample data for the application"""
    return businesses_data, accountants_data

def parse_date(date_str):
    """Parse date string in format 'DD/MM/YYYY' to Date object."""
    try:
        return datetime.strptime(date_str, '%d/%m/%Y').date()
    except:
        return datetime.now().date()

def init_db():
    """Initialize the database with tables and real test data."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    print("Creating sample data...")
    businesses_data, accountants_data = create_sample_data()
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Database already contains data. Skipping initialization.")
            return
        
        # Create users with the correct structure
        users = {}
        accountants = {}
        
        # Create root admin
        root_admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("password"),
            role="root_admin",
            is_active=True
        )
        db.add(root_admin)
        db.flush()
        users["root_admin"] = root_admin
        
        # Create super accountant
        super_accountant = User(
            username="super",
            email="super@example.com",
            hashed_password=get_password_hash("password"),
            role="super_accountant",
            is_active=True
        )
        db.add(super_accountant)
        db.flush()
        users["super_accountant"] = super_accountant
        
        # Use the accountants data directly since it's already in the correct format
        regular_accountants = accountants_data
        
        # Create all regular accountant users
        for acc_data in regular_accountants:
            user = User(
                username=acc_data["username"],
                email=acc_data["email"],
                hashed_password=get_password_hash("password"),
                role=acc_data["role"],
                is_active=True
            )
            db.add(user)
            db.flush()
            users[acc_data["username"]] = user
        
        # Create accountant records
        # Root admin doesn't need an accountant record
        
        # Super accountant record
        super_acc_record = Accountant(
            user_id=super_accountant.id,
            first_name="Super",
            last_name="Accountant",
            is_super_accountant=True
        )
        db.add(super_acc_record)
        db.flush()
        accountants["super"] = super_acc_record
        
        # Regular accountant records - assign some to super accountant, some independent
        regular_acc_records = []
        for i, acc_data in enumerate(regular_accountants):
            # Alternate between assigning to super accountant and keeping independent
            super_accountant_id = super_accountant.id if i % 2 == 0 else None
            
            acc_record = Accountant(
                user_id=users[acc_data["username"]].id,
                first_name=acc_data["first_name"],
                last_name=acc_data["last_name"],
                is_super_accountant=False,
                super_accountant_id=super_accountant_id
            )
            db.add(acc_record)
            db.flush()
            regular_acc_records.append(acc_record)
            accountants[acc_data["username"]] = acc_record
        
        # Create businesses and distribute them among different accountants
        for i, business_data in enumerate(businesses_data):
            # Distribute businesses among different accountants
            assigned_accountant = regular_acc_records[i % len(regular_acc_records)]
            
            business = Business(
                name=business_data['name'],
                description=business_data.get('description', ''),
                owner_id=root_admin.id,  # Root admin owns all businesses
                accountant_id=assigned_accountant.id,  # Distribute among accountants
                is_active=True
            )
            db.add(business)
            db.flush()
            
            # Add the assigned accountant to the business's accountants list
            business.accountants.append(assigned_accountant)
            
            # Create financial metrics
            if 'financialMetrics' in business_data:
                fin_metrics = BusinessFinancialMetrics(
                    business_id=business.id,
                    revenue=business_data['financialMetrics'].get('revenue', 0),
                    gross_profit=business_data['financialMetrics'].get('grossProfit', 0),
                    net_profit=business_data['financialMetrics'].get('netProfit', 0),
                    total_costs=business_data['financialMetrics'].get('totalCosts', 0),
                    percentage_change_revenue=business_data['financialMetrics'].get('percentageChangeRevenue', 0),
                    percentage_change_gross_profit=business_data['financialMetrics'].get('percentageChangeGrossProfit', 0),
                    percentage_change_net_profit=business_data['financialMetrics'].get('percentageChangeNetProfit', 0),
                    percentage_change_total_costs=business_data['financialMetrics'].get('percentageChangeTotalCosts', 0)
                )
                db.add(fin_metrics)
            
            # Create business metrics
            if 'metrics' in business_data:
                metrics = BusinessMetrics(
                    business_id=business.id,
                    documents_due=business_data['metrics'].get('documentsDue', 0),
                    outstanding_invoices=business_data['metrics'].get('outstandingInvoices', 0),
                    pending_approvals=business_data['metrics'].get('pendingApprovals', 0),
                    accounting_year_end=parse_date(business_data['metrics'].get('accountingYearEnd', '31/12/2024'))
                )
                db.add(metrics)
        
        # Commit all changes
        db.commit()
        print("Database initialized successfully!")
        print(f"Created {len(users)} users:")
        for role, user in users.items():
            print(f"  - {role}: {user.email} (role: {user.role})")
        print(f"Created {len(accountants)} accountant records")
        print(f"Created {len(businesses_data)} businesses")
        
    except Exception as e:
        db.rollback()
        print(f"Error initializing database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def reset_db():
    """Reset the database by dropping all tables and recreating them."""
    print("Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("Recreating database tables...")
    Base.metadata.create_all(bind=engine)
    
    print("Database reset complete.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize Apex AM API database")
    parser.add_argument(
        "--reset", 
        action="store_true", 
        help="Reset database (drop all tables and recreate)"
    )
    
    args = parser.parse_args()
    
    if args.reset:
        reset_db()
    
    init_db()
