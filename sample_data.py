import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create sample sales data
np.random.seed(42)

# Generate sample data
products = ['Widget A', 'Widget B', 'Widget C', 'Gadget X', 'Gadget Y']
sales_reps = ['John Smith', 'Jane Doe', 'Mike Johnson', 'Sarah Wilson', 'Tom Brown']
regions = ['North', 'South', 'East', 'West']

# Create 100 rows of sample data
data = []
start_date = datetime(2024, 1, 1)

for i in range(100):
    data.append({
        'Date': start_date + timedelta(days=np.random.randint(0, 365)),
        'Product': np.random.choice(products),
        'Sales_Rep': np.random.choice(sales_reps),
        'Region': np.random.choice(regions),
        'Units_Sold': np.random.randint(1, 50),
        'Unit_Price': np.random.uniform(10, 100),
        'Revenue': 0,  # Will calculate
        'Commission_Rate': np.random.choice([0.03, 0.05, 0.08]),
        'Commission': 0  # Will calculate
    })

# Convert to DataFrame
df = pd.DataFrame(data)

# Calculate derived fields
df['Revenue'] = df['Units_Sold'] * df['Unit_Price']
df['Commission'] = df['Revenue'] * df['Commission_Rate']

# Round numeric columns
df['Unit_Price'] = df['Unit_Price'].round(2)
df['Revenue'] = df['Revenue'].round(2)
df['Commission'] = df['Commission'].round(2)

# Save to Excel
df.to_excel('sample_sales_data.xlsx', index=False)
print("Sample Excel file created: sample_sales_data.xlsx")
print(f"Data shape: {df.shape}")
print("\nFirst 5 rows:")
print(df.head())