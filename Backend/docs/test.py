import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# ============================================
# CONFIGURATION
# ============================================
NUM_RECORDS = 500  # Records per file
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 11, 5)

DISTRICTS = [
    'Mumbai', 'Pune', 'Nagpur', 'Thane', 'Nashik', PredictivMinds
    'Aurangabad', 'Kolhapur', 'Solapur', 'Amravati', 'Nanded'
]

# ============================================
# 1. HEALTH DEPARTMENT DATA
# ============================================


def generate_health_data(num_records=NUM_RECORDS):
    """Generate realistic health department data"""

    dates = pd.date_range(START_DATE, END_DATE, periods=num_records)

    data = {
        'Date': dates,
        'District': [random.choice(DISTRICTS) for _ in range(num_records)],
        'Hospital_Type': np.random.choice(['Government', 'Private', 'Tertiary', 'Primary'], num_records),

        # Ambulance services
        'Ambulance_Requests': np.random.randint(10, 150, num_records),
        'Ambulance_Deployed': np.random.randint(8, 145, num_records),
        'Ambulance_Response_Time_Minutes': np.random.uniform(5, 45, num_records).round(2),

        # Hospital beds
        'Hospital_Beds_Total': np.random.randint(50, 500, num_records),
        'Hospital_Beds_Occupied': np.random.randint(30, 480, num_records),
        'Hospital_Beds_Available': np.random.randint(5, 200, num_records),
        'ICU_Beds_Total': np.random.randint(10, 100, num_records),
        'ICU_Beds_Occupied': np.random.randint(5, 95, num_records),

        # OPD (Out-Patient Department)
        'OPD_Patients_General': np.random.randint(100, 800, num_records),
        'OPD_Patients_Pediatric': np.random.randint(50, 300, num_records),
        'OPD_Patients_Emergency': np.random.randint(20, 200, num_records),
        'OPD_Average_Wait_Time_Minutes': np.random.uniform(15, 120, num_records).round(2),

        # Disease cases
        'Disease_Dengue_Cases': np.random.randint(0, 50, num_records),
        'Disease_Malaria_Cases': np.random.randint(0, 30, num_records),
        'Disease_COVID_Cases': np.random.randint(0, 100, num_records),
        'Disease_Tuberculosis_Cases': np.random.randint(0, 20, num_records),

        # Medical staff
        'Doctors_On_Duty': np.random.randint(5, 50, num_records),
        'Nurses_On_Duty': np.random.randint(10, 100, num_records),
        'Paramedics_Available': np.random.randint(5, 30, num_records),

        # Service quality
        'Patient_Satisfaction_Score': np.random.uniform(3.0, 5.0, num_records).round(2),
        'Patient_Complaints': np.random.randint(0, 25, num_records),
        'Medical_Equipment_Functional': np.random.uniform(0.7, 1.0, num_records).round(2),

        # Additional metrics
        'Blood_Bank_Units_Available': np.random.randint(50, 500, num_records),
        'Oxygen_Cylinders_Available': np.random.randint(20, 200, num_records),
        'Ventilators_Available': np.random.randint(5, 50, num_records),
        'Ventilators_In_Use': np.random.randint(2, 45, num_records),
    }

    df = pd.DataFrame(data)

    # Add derived columns
    df['Hospital_Bed_Occupancy_Rate'] = (
        df['Hospital_Beds_Occupied'] / df['Hospital_Beds_Total']
    ).round(2)

    df['ICU_Occupancy_Rate'] = (
        df['ICU_Beds_Occupied'] / df['ICU_Beds_Total']
    ).round(2)

    df['Ambulance_Fulfillment_Rate'] = (
        df['Ambulance_Deployed'] / df['Ambulance_Requests']
    ).round(2)

    return df

# ============================================
# 2. INFRASTRUCTURE DEPARTMENT DATA
# ============================================


def generate_infrastructure_data(num_records=NUM_RECORDS):
    """Generate realistic infrastructure department data"""

    dates = pd.date_range(START_DATE, END_DATE, periods=num_records)

    data = {
        'Date': dates,
        'District': [random.choice(DISTRICTS) for _ in range(num_records)],
        'Ward': [f'Ward_{random.randint(1, 50)}' for _ in range(num_records)],

        # Water supply
        'Water_Supply_Hours_Per_Day': np.random.uniform(0, 24, num_records).round(2),
        'Water_Tank_Level_Percent': np.random.uniform(10, 100, num_records).round(2),
        'Water_Tank_Capacity_Liters': np.random.randint(10000, 500000, num_records),
        'Water_Tanker_Requests': np.random.randint(0, 50, num_records),
        'Water_Tanker_Deployed': np.random.randint(0, 45, num_records),
        'Water_Quality_Score': np.random.uniform(6.0, 9.5, num_records).round(2),
        'Water_Complaints': np.random.randint(0, 30, num_records),

        # Roads and infrastructure
        'Road_Potholes_Reported': np.random.randint(0, 100, num_records),
        'Road_Potholes_Repaired': np.random.randint(0, 95, num_records),
        'Road_Repair_Time_Days': np.random.uniform(1, 30, num_records).round(2),
        'Road_Length_KM': np.random.uniform(10, 500, num_records).round(2),
        'Road_Condition_Score': np.random.uniform(3.0, 9.0, num_records).round(2),

        # Power supply
        'Power_Supply_Hours_Per_Day': np.random.uniform(18, 24, num_records).round(2),
        'Power_Outage_Count': np.random.randint(0, 10, num_records),
        'Power_Outage_Duration_Minutes': np.random.uniform(0, 300, num_records).round(2),
        'Power_Complaints': np.random.randint(0, 20, num_records),

        # Drainage and sanitation
        'Drainage_Blockages_Reported': np.random.randint(0, 50, num_records),
        'Drainage_Blockages_Cleared': np.random.randint(0, 48, num_records),
        'Sanitation_Workers_Deployed': np.random.randint(5, 50, num_records),
        'Garbage_Collection_Trips': np.random.randint(5, 30, num_records),
        'Garbage_Processed_Tons': np.random.uniform(50, 500, num_records).round(2),

        # Street infrastructure
        'Street_Lights_Total': np.random.randint(100, 2000, num_records),
        'Street_Lights_Functional': np.random.randint(90, 1995, num_records),
        'Street_Lights_Complaints': np.random.randint(0, 30, num_records),

        # Maintenance
        'Maintenance_Requests': np.random.randint(10, 100, num_records),
        'Maintenance_Completed': np.random.randint(8, 95, num_records),
        'Maintenance_Budget_Used_Percent': np.random.uniform(40, 95, num_records).round(2),
        'Citizen_Complaints_Total': np.random.randint(5, 80, num_records),
    }

    df = pd.DataFrame(data)

    # Add derived columns
    df['Water_Fulfillment_Rate'] = (
        df['Water_Tanker_Deployed'] / (df['Water_Tanker_Requests'] + 1)
    ).clip(0, 1).round(2)

    df['Pothole_Repair_Rate'] = (
        df['Road_Potholes_Repaired'] / (df['Road_Potholes_Reported'] + 1)
    ).clip(0, 1).round(2)

    df['Street_Light_Functional_Rate'] = (
        df['Street_Lights_Functional'] / df['Street_Lights_Total']
    ).round(2)

    return df

# ============================================
# 3. PUBLIC SAFETY DEPARTMENT DATA
# ============================================


def generate_public_safety_data(num_records=NUM_RECORDS):
    """Generate realistic public safety department data"""

    dates = pd.date_range(START_DATE, END_DATE, periods=num_records)

    data = {
        'Date': dates,
        'District': [random.choice(DISTRICTS) for _ in range(num_records)],
        'Police_Station': [f'PS_{random.randint(1, 50)}' for _ in range(num_records)],

        # Crime incidents
        'Crime_Incidents_Total': np.random.randint(0, 50, num_records),
        'Crime_Theft': np.random.randint(0, 20, num_records),
        'Crime_Assault': np.random.randint(0, 10, num_records),
        'Crime_Robbery': np.random.randint(0, 8, num_records),
        'Crime_Cybercrime': np.random.randint(0, 15, num_records),
        'Crime_Cases_Resolved': np.random.randint(0, 45, num_records),
        'Crime_Resolution_Time_Days': np.random.uniform(1, 90, num_records).round(2),

        # Traffic and accidents
        'Traffic_Accidents': np.random.randint(0, 30, num_records),
        'Accident_Casualties_Minor': np.random.randint(0, 20, num_records),
        'Accident_Casualties_Major': np.random.randint(0, 10, num_records),
        'Accident_Fatalities': np.random.randint(0, 5, num_records),
        'Traffic_Violations': np.random.randint(10, 200, num_records),
        'Traffic_Fines_Collected_Rs': np.random.randint(5000, 100000, num_records),

        # Fire emergencies
        'Fire_Emergency_Calls': np.random.randint(0, 15, num_records),
        'Fire_Incidents': np.random.randint(0, 10, num_records),
        'Fire_Response_Time_Minutes': np.random.uniform(5, 25, num_records).round(2),
        'Fire_Property_Damage_Rs': np.random.randint(0, 5000000, num_records),
        'Fire_Lives_Saved': np.random.randint(0, 20, num_records),

        # Emergency helpline
        'Emergency_Helpline_Calls': np.random.randint(50, 500, num_records),
        'Emergency_Calls_Answered': np.random.randint(45, 495, num_records),
        'Emergency_Response_Time_Minutes': np.random.uniform(5, 30, num_records).round(2),
        'Emergency_False_Alarms': np.random.randint(0, 50, num_records),

        # Police resources
        'Police_Officers_On_Duty': np.random.randint(10, 100, num_records),
        'Police_Vehicles_Available': np.random.randint(5, 50, num_records),
        'Police_Vehicles_On_Patrol': np.random.randint(3, 45, num_records),

        # Public complaints
        'Public_Complaints': np.random.randint(0, 40, num_records),
        'Public_Complaints_Resolved': np.random.randint(0, 38, num_records),
        'Public_Satisfaction_Score': np.random.uniform(3.0, 5.0, num_records).round(2),

        # Law and order
        'Public_Gatherings': np.random.randint(0, 10, num_records),
        'Security_Personnel_Deployed': np.random.randint(0, 200, num_records),
        'Curfew_Violations': np.random.randint(0, 5, num_records),
    }

    df = pd.DataFrame(data)

    # Add derived columns
    df['Crime_Resolution_Rate'] = (
        df['Crime_Cases_Resolved'] / (df['Crime_Incidents_Total'] + 1)
    ).clip(0, 1).round(2)

    df['Emergency_Call_Answer_Rate'] = (
        df['Emergency_Calls_Answered'] / df['Emergency_Helpline_Calls']
    ).round(2)

    df['Complaint_Resolution_Rate'] = (
        df['Public_Complaints_Resolved'] / (df['Public_Complaints'] + 1)
    ).clip(0, 1).round(2)

    return df


# ============================================
# MAIN EXECUTION
# ============================================
if __name__ == "__main__":
    print("🚀 Generating Test Data for PredictivMinds...")
    print("=" * 60)

    # Generate data
    print("\n📊 Generating Health Department Data...")
    health_df = generate_health_data(NUM_RECORDS)

    print("📊 Generating Infrastructure Department Data...")
    infra_df = generate_infrastructure_data(NUM_RECORDS)

    print("📊 Generating Public Safety Department Data...")
    safety_df = generate_public_safety_data(NUM_RECORDS)

    # Save to Excel
    output_dir = "../data/raw/"

    print("\n💾 Saving to Excel files...")
    health_file = f"{output_dir}health_department_test_data.xlsx"
    infra_file = f"{output_dir}infrastructure_department_test_data.xlsx"
    safety_file = f"{output_dir}public_safety_department_test_data.xlsx"

    health_df.to_excel(health_file, index=False, sheet_name='Health_Data')
    infra_df.to_excel(infra_file, index=False,
                      sheet_name='Infrastructure_Data')
    safety_df.to_excel(safety_file, index=False, sheet_name='Safety_Data')

    print("\n" + "=" * 60)
    print("✅ SUCCESS! Test data generated")
    print("=" * 60)

    # Summary
    print(f"\n📁 HEALTH DATA:")
    print(f"   File: {health_file}")
    print(f"   Records: {len(health_df)}")
    print(f"   Columns: {len(health_df.columns)}")
    print(f"   Size: {health_df.memory_usage(deep=True).sum() / 1024:.2f} KB")

    print(f"\n📁 INFRASTRUCTURE DATA:")
    print(f"   File: {infra_file}")
    print(f"   Records: {len(infra_df)}")
    print(f"   Columns: {len(infra_df.columns)}")
    print(f"   Size: {infra_df.memory_usage(deep=True).sum() / 1024:.2f} KB")

    print(f"\n📁 PUBLIC SAFETY DATA:")
    print(f"   File: {safety_file}")
    print(f"   Records: {len(safety_df)}")
    print(f"   Columns: {len(safety_df.columns)}")
    print(f"   Size: {safety_df.memory_usage(deep=True).sum() / 1024:.2f} KB")

    print("\n🎯 Sample data preview (first 3 rows):")
    print("\nHealth Data:")
    print(health_df.head(3))
    print("\nInfrastructure Data:")
    print(infra_df.head(3))
    print("\nPublic Safety Data:")
    print(safety_df.head(3))

    print("\n" + "=" * 60)
    print("✅ Files ready for testing!")
    print("Upload these files to: https://api.predictivminds.shop")
    print("=" * 60)
