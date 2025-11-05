import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import openpyxl

def generate_health_excel():
    """Generate sample health department Excel file"""
    data = {
        'Date': pd.date_range('2025-10-01', periods=50),
        'District': np.random.choice(['Mumbai', 'Pune', 'Nagpur', 'Thane'], 50),
        'Hospital_Type': np.random.choice(['Government', 'Private', 'Tertiary'], 50),
        'Ambulance_Requests': np.random.randint(20, 100, 50),
        'Hospital_Beds_Available': np.random.randint(50, 300, 50),
        'Hospital_Beds_Occupied': np.random.randint(30, 280, 50),
        'OPD_Patients': np.random.randint(100, 500, 50),
        'Disease_Dengue_Cases': np.random.randint(0, 50, 50),
        'Disease_Malaria_Cases': np.random.randint(0, 30, 50),
        'Average_Response_Time_Min': np.random.randint(10, 60, 50),
        'Patient_Complaints': np.random.randint(0, 20, 50)
    }
    
    df = pd.DataFrame(data)
    
    # Save to Excel
    filename = '../data/raw/health_department_sample.xlsx'
    df.to_excel(filename, index=False, sheet_name='Health_Data')
    print(f"✅ Created: {filename}")
    print(f"   Records: {len(df)}")
    print(f"   Size: {df.memory_usage(deep=True).sum() / 1024:.2f} KB\n")
    
    return filename

def generate_infrastructure_excel():
    """Generate sample infrastructure department Excel file"""
    data = {
        'Date': pd.date_range('2025-10-01', periods=50),
        'District': np.random.choice(['Mumbai', 'Pune', 'Nagpur', 'Thane', 'Nashik'], 50),
        'Ward': [f'Ward_{i}' for i in np.random.randint(1, 25, 50)],
        'Water_Supply_Hours': np.random.randint(0, 24, 50),
        'Water_Tank_Level_Percent': np.random.randint(20, 100, 50),
        'Water_Tanker_Deployed': np.random.randint(0, 10, 50),
        'Road_Potholes_Reported': np.random.randint(0, 50, 50),
        'Road_Potholes_Repaired': np.random.randint(0, 40, 50),
        'Power_Outage_Hours': np.random.uniform(0, 12, 50),
        'Drainage_Blockages': np.random.randint(0, 20, 50),
        'Maintenance_Complaints': np.random.randint(0, 30, 50)
    }
    
    df = pd.DataFrame(data)
    
    # Save to Excel
    filename = '../data/raw/infrastructure_department_sample.xlsx'
    df.to_excel(filename, index=False, sheet_name='Infrastructure_Data')
    print(f"✅ Created: {filename}")
    print(f"   Records: {len(df)}")
    print(f"   Size: {df.memory_usage(deep=True).sum() / 1024:.2f} KB\n")
    
    return filename

def generate_public_safety_excel():
    """Generate sample public safety department Excel file"""
    data = {
        'Date': pd.date_range('2025-10-01', periods=50),
        'District': np.random.choice(['Mumbai', 'Pune', 'Nagpur'], 50),
        'Police_Station': [f'PS_{i}' for i in np.random.randint(1, 20, 50)],
        'Crime_Incidents': np.random.randint(0, 30, 50),
        'Traffic_Accidents': np.random.randint(0, 15, 50),
        'Accident_Casualties': np.random.randint(0, 10, 50),
        'Fire_Emergency_Calls': np.random.randint(0, 10, 50),
        'Emergency_Helpline_Calls': np.random.randint(50, 200, 50),
        'Average_Response_Time_Min': np.random.randint(5, 30, 50),
        'Cases_Resolved': np.random.randint(0, 30, 50),
        'Public_Complaints': np.random.randint(0, 20, 50)
    }
    
    df = pd.DataFrame(data)
    
    # Save to Excel
    filename = '../data/raw/public_safety_department_sample.xlsx'
    df.to_excel(filename, index=False, sheet_name='Safety_Data')
    print(f"✅ Created: {filename}")
    print(f"   Records: {len(df)}")
    print(f"   Size: {df.memory_usage(deep=True).sum() / 1024:.2f} KB\n")
    
    return filename

if __name__ == "__main__":
    print("\n" + "="*60)
    print("📊 GENERATING TEST EXCEL FILES")
    print("="*60 + "\n")
    
    files = [
        generate_health_excel(),
        generate_infrastructure_excel(),
        generate_public_safety_excel()
    ]
    
    print("="*60)
    print(f"✅ All 3 test Excel files generated!")
    print("="*60)
    print("\nFiles ready for Postman testing:")
    for f in files:
        print(f"  - {f}")
