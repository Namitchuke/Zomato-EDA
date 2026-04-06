import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

print("Imports successful!")

try:
    print("Trying to load 'zomato_dataset.csv'...")
    df = pd.read_csv(r"zomato_dataset.csv")
    print("CSV loaded successfully!")
    print("\nHead of data:")
    print(df.head())
    
    print("\nColumns:")
    print(df.columns)
    
    print("\nInfo:")
    print(df.info())
    
    print("\nBASIC CODE RAN SUCCESSFULLY!")
except Exception as e:
    print(f"\nError running basic code: {e}")
