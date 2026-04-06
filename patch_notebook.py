import json
import os

notebook_path = "Zomato EDA.ipynb"

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        new_source = []
        for line in source:
            # 1. Fix data loading and column stripping
            if 'pd.read_csv(r"zomato_dataset.csv")' in line:
                new_source.append(line)
                new_source.append('df.columns = df.columns.str.strip()\n')
            
            # 2. Fix fillna for Dining_Rating
            elif 'df["Dining_Rating"].fillna("Not provided", inplace=True)' in line:
                new_source.append('df["Dining_Rating"] = df["Dining_Rating"].astype(object).fillna("Not provided")\n')
            
            # 3. Fix fillna for Delivery_Rating
            elif 'df["Delivery_Rating"].fillna("Not provided", inplace=True)' in line:
                new_source.append('df["Delivery_Rating"] = df["Delivery_Rating"].astype(object).fillna("Not provided")\n')
            
            # 4. Fix fillna for Best_Seller
            elif 'df["Best_Seller"].fillna("NA", inplace=True)' in line:
                new_source.append('df["Best_Seller"] = df["Best_Seller"].fillna("NA")\n')
            
            else:
                new_source.append(line)
        
        cell['source'] = new_source

# Write the patched notebook back
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook patched successfully!")
