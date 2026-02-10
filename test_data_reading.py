import pandas as pd
import numpy as np

# Test if data is being read correctly
print("Testing CSV data reading...")
print("=" * 60)

# Test file paths
test_files = [
    ("Option1_NetProduction", "1.1RMV.csv", "USA", 2020),
    ("Option1_NetProduction", "1.2RMR.csv", "China", 2025),
    ("Option2_TotalProduction", "11.1RMV.csv", "Germany", 2030),
    ("Option2_TotalProduction", "12.1ERV.csv", "Japan", 2015),
]

for folder, filename, country, year in test_files:
    filepath = f"data/{folder}/{filename}"
    
    try:
        df = pd.read_csv(filepath, index_col=0)
        year_str = str(year)
        
        if country in df.index and year_str in df.columns:
            value = df.loc[country, year_str]
            print(f"✅ {filename}: {country} {year} = {value:,.2f} MTCO2")
        else:
            print(f"❌ {filename}: {country} or {year} not found")
            print(f"   Available countries: {list(df.index)[:3]}...")
            print(f"   Available years: {list(df.columns)[:5]}...")
            
    except Exception as e:
        print(f"❌ Error reading {filename}: {e}")

print("\n" + "=" * 60)
print("Testing data trends by year...")

# Test trend for one country
folder = "Option1_NetProduction"
filename = "1.1RMV.csv"
country = "USA"

try:
    df = pd.read_csv(f"data/{folder}/{filename}", index_col=0)
    if country in df.index:
        print(f"\n📈 Yearly trend for {country} in {filename}:")
        years = [2011, 2015, 2020, 2025, 2030, 2035, 2040]
        for year in years:
            year_str = str(year)
            if year_str in df.columns:
                value = df.loc[country, year_str]
                print(f"   {year}: {value:,.2f} MTCO2")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
print("✅ Test complete!")