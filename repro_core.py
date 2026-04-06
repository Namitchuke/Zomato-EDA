import pandas as pd
import numpy as np

def test_notebook_logic():
    try:
        print("--- Testing Data Loading ---")
        df = pd.read_csv("zomato_dataset.csv")
        print("Columns in CSV:", df.columns.tolist())
        
        print("\n--- Testing NA Filling ---")
        # Notebook code:
        # df["Dining_Rating"].fillna("Not provided", inplace=True)
        # df["Delivery_Rating"].fillna("Not provided", inplace=True)
        # df["Best_Seller"].fillna("NA", inplace=True)
        
        # In modern pandas, inplace might be tricky or the user might have a column name mismatch
        target_cols = ["Dining_Rating", "Delivery_Rating", "Best_Seller"]
        for col in target_cols:
            if col in df.columns:
                df[col] = df[col].fillna("Not provided" if "Rating" in col else "NA")
                print(f"Filled {col}")
            else:
                print(f"Column {col} NOT FOUND!")

        print("\n--- Testing Groupby ---")
        # res_count=df.groupby(['City'])['Restaurant_Name'].nunique().to_frame().reset_index().sort_values(by='Restaurant_Name', ascending=False)
        if 'City' in df.columns and 'Restaurant_Name' in df.columns:
            res_count = df.groupby(['City'])['Restaurant_Name'].nunique()
            print("Groupby City successful.")
        else:
            print("City or Restaurant_Name column NOT FOUND!")

        print("\n--- Checking for Cuisine column issue ---")
        if 'Cuisine ' in df.columns:
            print("Found 'Cuisine ' with trailing space.")
        elif 'Cuisine' in df.columns:
            print("Found 'Cuisine' without trailing space.")
        else:
            print("Cuisine column NOT FOUND at all!")

        print("\nBasic tests completed.")
        
    except Exception as e:
        print(f"\nCaught unexpected error: {e}")

if __name__ == "__main__":
    test_notebook_logic()
