import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

try:
    print("Loading data...")
    df = pd.read_csv("zomato_dataset.csv")
    print("Data loaded successfully.")
    
    print("\nColumns found:")
    print(df.columns.tolist())
    
    print("\nInitial Info:")
    df.info()
    
    # Simulating the notebook's basic operations
    print("\nFilling NAs...")
    # These were in the notebook
    df["Dining_Rating"].fillna("Not provided", inplace=True)
    df["Delivery_Rating"].fillna("Not provided", inplace=True)
    df["Best_Seller"].fillna("NA", inplace=True)
    print("NAs filled.")
    
    # Check for the Cuisine column space issue
    if 'Cuisine ' in df.columns:
        print("\nFixing space in 'Cuisine ' column name...")
        df.rename(columns={'Cuisine ': 'Cuisine'}, inplace=True)
    
    print("\nSimulating a groupby operation...")
    res_count = df.groupby(['City'])['Restaurant_Name'].nunique().to_frame().reset_index().sort_values(by='Restaurant_Name', ascending=False)
    print("Groupby successful.")
    
    print("\nAll basic steps executed without crashing.")

except Exception as e:
    print(f"\nERROR ENCOUNTERED: {e}")
    import traceback
    traceback.print_exc()
