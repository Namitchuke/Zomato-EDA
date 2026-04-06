import pandas as pd
import numpy as np

def verify_patched_logic():
    try:
        print("--- Verifying Patched Logic ---")
        df = pd.read_csv("zomato_dataset.csv")
        
        # New code added by patch:
        df.columns = df.columns.str.strip()
        print("Cleaned columns:", df.columns.tolist())
        
        if "Cuisine" in df.columns and " Cuisine " not in df.columns:
            print("SUCCESS: Cuisine column space issue resolved.")
        
        # New fillna logic:
        df["Dining_Rating"] = df["Dining_Rating"].astype(object).fillna("Not provided")
        df["Delivery_Rating"] = df["Delivery_Rating"].astype(object).fillna("Not provided")
        df["Best_Seller"] = df["Best_Seller"].fillna("NA")
        
        print("\nChecks:")
        print(f"Dining_Rating null count: {df['Dining_Rating'].isnull().sum()}")
        print(f"Sample values in Dining_Rating: {df['Dining_Rating'].unique()[:5]}")
        
        print("\nChecking if groupby still works...")
        res_count = df.groupby(['City'])['Restaurant_Name'].nunique()
        print("Groupby City successful.")
        
        print("\nVERIFICATION SUCCESSFUL: No TypeErrors or ChainedAssignmentErrors!")

    except Exception as e:
        print(f"\nCaught unexpected error during verification: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_patched_logic()
