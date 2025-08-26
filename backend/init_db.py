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

def load_frontend_test_data():
    """Load test data from frontend test files."""
    frontend_test_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'test', 'testData')
    
    # Load businesses data
    businesses_file = os.path.join(frontend_test_dir, 'businesses.json')
    with open(businesses_file, 'r') as f:
        businesses_data = json.load(f)
    
    # Load accountants data
    accountants_file = os.path.join(frontend_test_dir, 'accountants.json')
    with open(accountants_file, 'r') as f:
        accountants_data = json.load(f)
    
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
    
    print("Loading frontend test data...")
    try:
        businesses_data, accountants_data = load_frontend_test_data()
    except FileNotFoundError as e:
        print(f"Error: Could not find frontend test data files: {e}")
        print("Make sure you're running this from the backend directory and frontend test data exists.")
        return
    
    print("Creating sample data...")
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Database already contains data. Skipping initialization.")
            return
        
        # Create users based on frontend accountant data
        users = {}
        accountants = {}
        
        for acc_data in accountants_data:
            # Create user
            user = User(
                username=acc_data['email'].split('@')[0],
                email=acc_data['email'],
                hashed_password=get_password_hash("password"),
                role=acc_data['role'],
                is_active=True
            )
            db.add(user)
            db.flush()  # Get the ID without committing
            
            # Create accountant record
            accountant = Accountant(
                user_id=user.id,
                first_name=acc_data['firstName'],
                last_name=acc_data['lastName'],
                is_super_accountant=(acc_data['role'] == 'super_accountant')
            )
            db.add(accountant)
            db.flush()
            
            users[acc_data['id']] = user
            accountants[acc_data['id']] = accountant
        
        # Set up super accountant relationships
        # Find the super accountant
        super_accountant = None
        for acc_id, acc in accountants.items():
            if acc.is_super_accountant:
                super_accountant = acc
                break
        
        # Assign regular accountants to super accountant
        if super_accountant:
            for acc_id, acc in accountants.items():
                if not acc.is_super_accountant:
                    acc.super_accountant_id = super_accountant.user_id
        
        # Create businesses from frontend data
        for business_data in businesses_data:
            # Find the first accountant assigned to this business
            assigned_accountant = None
            if business_data['accountants']:
                first_acc_id = business_data['accountants'][0]['id']
                if first_acc_id in accountants:
                    assigned_accountant = accountants[first_acc_id]
            
            # Create business
            business = Business(
                name=business_data['name'],
                description=f"Business {business_data['id']} from frontend test data",
                owner_id=assigned_accountant.user_id if assigned_accountant else list(users.values())[0].id,
                accountant_id=assigned_accountant.id if assigned_accountant else None,
                is_active=True
            )
            db.add(business)
            db.flush()
            
            # Create financial metrics
            financial_metrics = BusinessFinancialMetrics(
                business_id=business.id,
                revenue=business_data['financialMetrics']['revenue'],
                gross_profit=business_data['financialMetrics']['grossProfit'],
                net_profit=business_data['financialMetrics']['netProfit'],
                total_costs=business_data['financialMetrics']['totalCosts'],
                percentage_change_revenue=business_data['financialMetrics']['percentageChangeRevenue'],
                percentage_change_gross_profit=business_data['financialMetrics']['percentageChangeGrossProfit'],
                percentage_change_net_profit=business_data['financialMetrics']['percentageChangeNetProfit'],
                percentage_change_total_costs=business_data['financialMetrics']['percentageChangeTotalCosts']
            )
            db.add(financial_metrics)
            
            # Create business metrics
            business_metrics = BusinessMetrics(
                business_id=business.id,
                documents_due=business_data['metrics']['documentsDue'],
                outstanding_invoices=business_data['metrics']['outstandingInvoices'],
                pending_approvals=business_data['metrics']['pendingApprovals'],
                accounting_year_end=parse_date(business_data['metrics']['accountingYearEnd'])
            )
            db.add(business_metrics)
        
        # Commit all changes
        db.commit()
        
        print("Sample data created successfully!")
        print("\nDefault users created (matching frontend):")
        print(f"Root Admin: email={users['1'].email}, password=password")
        print(f"Super Accountant: email={users['2'].email}, password=password")
        print(f"Accountant: email={users['3'].email}, password=password")
        print(f"\nCreated {len(businesses_data)} businesses with full financial data")
        print("All data matches your frontend test files exactly!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
        raise
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
