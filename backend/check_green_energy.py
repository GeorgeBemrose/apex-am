#!/usr/bin/env python3

from app.database import engine
from app.models import BusinessFinancialMetrics, Business
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

try:
    # Find Green Energy Co
    business = session.query(Business).filter(Business.name == 'Green Energy Co').first()
    
    if business:
        print(f"Found business: {business.name}")
        print(f"Business ID: {business.id}")
        
        # Get financial metrics
        metrics = session.query(BusinessFinancialMetrics).filter(
            BusinessFinancialMetrics.business_id == business.id
        ).first()
        
        if metrics:
            print(f"Total Costs: ${metrics.total_costs:,}")
            print(f"Total Costs Change: {metrics.percentage_change_total_costs}%")
            print(f"Revenue: ${metrics.revenue:,}")
            print(f"Revenue Change: {metrics.percentage_change_revenue}%")
        else:
            print("No financial metrics found")
    else:
        print("Green Energy Co not found")
        
        # List all businesses
        businesses = session.query(Business).all()
        print(f"\nAll businesses ({len(businesses)}):")
        for b in businesses:
            print(f"- {b.name}")
            
except Exception as e:
    print(f"Error: {e}")
finally:
    session.close()
