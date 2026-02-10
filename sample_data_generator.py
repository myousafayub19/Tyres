import pandas as pd
import numpy as np
import os

# Create directories
os.makedirs('data/Option1_NetProduction', exist_ok=True)
os.makedirs('data/Option2_TotalProduction', exist_ok=True)

# List of countries with realistic variations
countries = {
    'USA': {'factor': 1.2, 'trend': -0.01},
    'China': {'factor': 1.5, 'trend': -0.005},
    'Germany': {'factor': 0.9, 'trend': -0.015},
    'Japan': {'factor': 0.8, 'trend': -0.01},
    'India': {'factor': 1.1, 'trend': 0.005},
    'Brazil': {'factor': 0.7, 'trend': -0.008},
    'France': {'factor': 0.85, 'trend': -0.012},
    'UK': {'factor': 0.88, 'trend': -0.01},
    'Italy': {'factor': 0.82, 'trend': -0.009},
    'Canada': {'factor': 1.0, 'trend': -0.007},
}

# Years 2011-2040
years = list(range(2011, 2041))

# Define realistic base values for each file type
file_configs = {
    # Option 1: Net Production
    'Option1_NetProduction': {
        '1.1RMV': {'base': 2000, 'variation': 0.3, 'trend_factor': -0.015},  # Virgin raw material
        '1.2RMR': {'base': 1200, 'variation': 0.25, 'trend_factor': -0.02},  # Recycled raw material
        '1.3RMS': {'base': 800, 'variation': 0.2, 'trend_factor': -0.025},   # Sustainable sourcing
        
        '2.1ERV': {'base': 1500, 'variation': 0.25, 'trend_factor': -0.02},  # Renewable energy virgin
        '2.2ERR': {'base': 1000, 'variation': 0.2, 'trend_factor': -0.025},  # Renewable energy recycled
        '2.3ENV': {'base': 2500, 'variation': 0.3, 'trend_factor': -0.01},   # Non-renewable energy virgin
        '2.4ENR': {'base': 1800, 'variation': 0.25, 'trend_factor': -0.015}, # Non-renewable energy recycled
        
        '3.1WSA': {'base': 600, 'variation': 0.2, 'trend_factor': -0.03},    # Waste absolute
        '3.2WSM': {'base': 900, 'variation': 0.25, 'trend_factor': -0.02},   # Waste medium
        '3.3WSH': {'base': 1200, 'variation': 0.3, 'trend_factor': -0.01},   # Waste high
        
        '3.4WWA': {'base': 400, 'variation': 0.15, 'trend_factor': -0.025},  # Water absolute
        '3.5WWM': {'base': 600, 'variation': 0.2, 'trend_factor': -0.02},    # Water medium
        '3.6WWH': {'base': 800, 'variation': 0.25, 'trend_factor': -0.015},  # Water high
        
        '4.1LEV': {'base': 1200, 'variation': 0.25, 'trend_factor': -0.01},  # Logistics virgin
        '4.2LER': {'base': 800, 'variation': 0.2, 'trend_factor': -0.015},   # Logistics recycled
        
        '5.1UEA': {'base': 1800, 'variation': 0.3, 'trend_factor': -0.015},  # Usage absolute
        '5.2UEM': {'base': 2200, 'variation': 0.35, 'trend_factor': -0.01},  # Usage medium
        '5.3UEH': {'base': 2600, 'variation': 0.4, 'trend_factor': -0.005},  # Usage high
        
        '6.1ELU': {'base': 500, 'variation': 0.2, 'trend_factor': -0.02},    # End life retreading
        '6.2ELR': {'base': 300, 'variation': 0.15, 'trend_factor': -0.025},  # End life recycling
        '6.3ELG': {'base': 700, 'variation': 0.25, 'trend_factor': -0.01},   # End life pyro/gas
        '6.4ELC': {'base': 900, 'variation': 0.3, 'trend_factor': -0.008},   # End life combustion
        '6.5ELE': {'base': 1200, 'variation': 0.35, 'trend_factor': -0.005}, # End life landfill
    },
    
    # Option 2: Total Production (higher values)
    'Option2_TotalProduction': {
        '11.1RMV': {'base': 3000, 'variation': 0.35, 'trend_factor': -0.01},
        '11.2RMR': {'base': 1800, 'variation': 0.3, 'trend_factor': -0.015},
        '11.3RMS': {'base': 1200, 'variation': 0.25, 'trend_factor': -0.02},
        
        '12.1ERV': {'base': 2200, 'variation': 0.3, 'trend_factor': -0.015},
        '12.2ERR': {'base': 1500, 'variation': 0.25, 'trend_factor': -0.02},
        '12.3ENV': {'base': 3500, 'variation': 0.35, 'trend_factor': -0.008},
        '12.4ENR': {'base': 2500, 'variation': 0.3, 'trend_factor': -0.01},
        
        '13.1WSA': {'base': 900, 'variation': 0.25, 'trend_factor': -0.025},
        '13.2WSM': {'base': 1300, 'variation': 0.3, 'trend_factor': -0.015},
        '13.3WSH': {'base': 1700, 'variation': 0.35, 'trend_factor': -0.008},
        
        '13.4WWA': {'base': 600, 'variation': 0.2, 'trend_factor': -0.02},
        '13.5WWM': {'base': 900, 'variation': 0.25, 'trend_factor': -0.015},
        '13.6WWH': {'base': 1200, 'variation': 0.3, 'trend_factor': -0.01},
        
        '14.1LEV': {'base': 1800, 'variation': 0.3, 'trend_factor': -0.008},
        '14.2LER': {'base': 1200, 'variation': 0.25, 'trend_factor': -0.01},
        
        '15.1UEA': {'base': 2500, 'variation': 0.35, 'trend_factor': -0.01},
        '15.2UEM': {'base': 3000, 'variation': 0.4, 'trend_factor': -0.007},
        '15.3UEH': {'base': 3500, 'variation': 0.45, 'trend_factor': -0.004},
        
        '16.1ELU': {'base': 700, 'variation': 0.25, 'trend_factor': -0.015},
        '16.2ELR': {'base': 500, 'variation': 0.2, 'trend_factor': -0.02},
        '16.3ELG': {'base': 1000, 'variation': 0.3, 'trend_factor': -0.008},
        '16.4ELC': {'base': 1300, 'variation': 0.35, 'trend_factor': -0.006},
        '16.5ELE': {'base': 1700, 'variation': 0.4, 'trend_factor': -0.004},
    }
}

def generate_realistic_data(countries_dict, years_list, config):
    """Generate realistic data with country-specific trends"""
    data_dict = {}
    
    for filename, params in config.items():
        df = pd.DataFrame(index=list(countries_dict.keys()), columns=years_list)
        
        for country, country_info in countries_dict.items():
            # Base value for this country
            base_value = params['base'] * country_info['factor']
            
            # Generate data for each year with trend
            for i, year in enumerate(years_list):
                # Time trend
                trend_effect = 1 + (params['trend_factor'] + country_info['trend']) * i
                
                # Random variation
                random_variation = 1 + np.random.uniform(-params['variation'], params['variation'])
                
                # Calculate final value
                value = base_value * trend_effect * random_variation
                
                # Ensure positive values
                value = max(value, 10)
                
                df.loc[country, year] = round(value, 2)
        
        data_dict[filename] = df
    
    return data_dict

print("Generating realistic sample data...")
print("=" * 60)

# Generate data for both options
for option, config in file_configs.items():
    print(f"\nCreating {option} files:")
    data = generate_realistic_data(countries, years, config)
    
    for filename, df in data.items():
        filepath = f"data/{option}/{filename}.csv"
        df.to_csv(filepath)
        print(f"  ✓ {filename}.csv - Range: {df.min().min():.0f} to {df.max().max():.0f}")

print("\n" + "=" * 60)
print("✅ Sample data generation complete!")
print(f"Created {len(file_configs['Option1_NetProduction'])} files for Option 1")
print(f"Created {len(file_configs['Option2_TotalProduction'])} files for Option 2")

# Create a test CSV to verify
test_file = "data/Option1_NetProduction/1.1RMV.csv"
df_test = pd.read_csv(test_file, index_col=0)
print("\n📊 Sample data verification:")
print(f"File: {test_file}")
print(f"Shape: {df_test.shape}")
print(f"Sample values for USA:")
print(df_test.loc['USA', ['2011', '2020', '2030', '2040']])
print("\n✅ Data is ready! Run: streamlit run app_final.py")