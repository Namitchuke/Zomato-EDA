import json

notebook_path = "Zomato EDA.ipynb"

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Set notebook level metadata
if 'metadata' not in nb:
    nb['metadata'] = {}
nb['metadata']['trusted'] = True

# Set cell level metadata for every cell
for cell in nb['cells']:
    if 'metadata' not in cell:
        cell['metadata'] = {}
    cell['metadata']['trusted'] = True

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook metadata set to 'trusted': True for all cells.")
