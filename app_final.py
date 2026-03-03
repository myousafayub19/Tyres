import streamlit as st
import pandas as pd
import numpy as np
import os
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# Add matplotlib import
try:
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib_available = True
except ImportError:
    matplotlib_available = False

# Page configuration - MUST BE FIRST
st.set_page_config(
    page_title="Tyre Emissions Dashboard",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS with improved styling and icons
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1E3A8A;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3B82F6;
    }
    .sub-title {
        text-align: center;
        color: #6B7280;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .group-header {
        color: #1F2937;
        font-size: 1.3rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #E5E7EB;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .parameter-box {
        background: #FFFFFF;
        padding: 18px;
        border-radius: 12px;
        border: 2px solid #E5E7EB;
        margin: 12px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    .parameter-box:hover {
        border-color: #3B82F6;
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.1);
    }
    .required-box {
        border-left: 6px solid #EF4444;
        background: linear-gradient(90deg, #FEF2F2 0%, #FFFFFF 100%);
    }
    .recommended-box {
        border-left: 6px solid #10B981;
        background: linear-gradient(90deg, #F0FDF4 0%, #FFFFFF 100%);
    }
    .info-label {
        font-size: 0.8rem;
        color: #6B7280;
        font-weight: 500;
        margin-bottom: 5px;
        display: block;
    }
    .required-badge {
        background: #EF4444;
        color: white;
        font-size: 0.7rem;
        padding: 2px 8px;
        border-radius: 12px;
        margin-left: 8px;
    }
    .result-box {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 20px 0;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .sustainable {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        border: 3px solid #10b981;
    }
    .not-sustainable {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #991b1b;
        border: 3px solid #ef4444;
    }
    .instruction-box {
        background: #FEF3C7;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #F59E0B;
        margin: 20px 0;
        font-size: 1rem;
        box-shadow: 0 4px 6px rgba(245, 158, 11, 0.1);
    }
    .custom-value-box {
        background: #F0F9FF;
        padding: 20px;
        border-radius: 12px;
        border: 2px dashed #3B82F6;
        margin: 20px 0;
    }
    .metric-card {
        background: #F9FAFB;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin: 10px 0;
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .stButton>button {
        font-weight: bold;
        font-size: 1.1rem;
        padding: 12px 28px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(59, 130, 246, 0.2);
    }
    .section-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #3B82F6, transparent);
        margin: 30px 0;
        opacity: 0.5;
    }
    .icon {
        font-size: 1.2rem;
        vertical-align: middle;
        margin-right: 5px;
    }
    .tooltip-icon {
        cursor: help;
        color: #6B7280;
        margin-left: 5px;
        font-size: 0.9rem;
    }
    .moon-journey {
        background: linear-gradient(135deg, #0B0B2B 0%, #1B1B4B 50%, #2B2B6B 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 20px 0;
        text-align: center;
        border: 2px solid #4a4a8a;
        position: relative;
        overflow: hidden;
    }
    .moon-journey::before {
        content: "★";
        position: absolute;
        color: rgba(255, 255, 255, 0.3);
        font-size: 20px;
        top: 10%;
        left: 20%;
        animation: twinkle 3s infinite;
    }
    .moon-journey::after {
        content: "✦";
        position: absolute;
        color: rgba(255, 255, 255, 0.3);
        font-size: 15px;
        bottom: 15%;
        right: 25%;
        animation: twinkle 4s infinite;
    }
    @keyframes twinkle {
        0% { opacity: 0.3; }
        50% { opacity: 1; }
        100% { opacity: 0.3; }
    }
    .star {
        position: absolute;
        color: white;
        font-size: 12px;
        opacity: 0.5;
        animation: twinkle 2s infinite;
    }
    .star1 { top: 30%; left: 10%; animation-delay: 0s; }
    .star2 { top: 70%; left: 85%; animation-delay: 1s; }
    .star3 { top: 20%; left: 90%; animation-delay: 2s; }
    .star4 { top: 80%; left: 15%; animation-delay: 1.5s; }
    .star5 { top: 40%; left: 50%; animation-delay: 0.5s; }
    .car-icon {
        font-size: 3rem;
        animation: drive 3s infinite;
        position: relative;
        z-index: 2;
    }
    @keyframes drive {
        0% { transform: translateX(-20px); }
        50% { transform: translateX(20px); }
        100% { transform: translateX(-20px); }
    }
    .moon-icon {
        font-size: 3rem;
        color: #ffd700;
        position: relative;
        z-index: 2;
        animation: glow 3s infinite;
    }
    @keyframes glow {
        0% { filter: drop-shadow(0 0 5px #ffd700); }
        50% { filter: drop-shadow(0 0 15px #ffd700); }
        100% { filter: drop-shadow(0 0 5px #ffd700); }
    }
    .journey-stats {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ffd700;
        margin: 10px 0;
        position: relative;
        z-index: 2;
    }
    .journey-text {
        font-size: 1.1rem;
        color: #a0a0ff;
        margin: 5px 0;
        position: relative;
        z-index: 2;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-title">🌍 Zero Emissions Strategy Tool for Tyres (ZEST)</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Real-time emissions calculation with sustainability recommendations</p>', unsafe_allow_html=True)

# Data Loading Functions
@st.cache_data
def load_csv_file(file_path):
    """Load a single CSV file"""
    try:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, index_col=0)
            df.columns = df.columns.astype(str)
            df = df.apply(pd.to_numeric, errors='coerce')
            return df
        else:
            return None
    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return None

def get_file_path(option, filename):
    """Get the correct file path based on option"""
    if option == "Net Production":
        folder = "Option1_NetProduction"
    else:
        folder = "Option2_TotalProduction"
    return f"data/{folder}/{filename}.csv"

def get_value(df, country, year):
    """Get value from dataframe for specific country and year"""
    try:
        year_str = str(year)
        if df is not None and country in df.index and year_str in df.columns:
            value = df.loc[country, year_str]
            if pd.isna(value):
                return 0.0
            return float(value)
        else:
            return 0.0
    except:
        return 0.0

# Initialize session state
if 'calculate_btn' not in st.session_state:
    st.session_state.calculate_btn = False
if 'results' not in st.session_state:
    st.session_state.results = None
if 'use_custom_values' not in st.session_state:
    st.session_state.use_custom_values = False
if 'custom_values' not in st.session_state:
    st.session_state.custom_values = {}

# Create two columns for the main layout
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    # ===== CONTROL PANEL =====
    st.markdown("## 🎛️ Control Panel")
    
    with st.container():
        # Option selection
        option = st.selectbox(
            "**Production Type**",
            ["Net Production", "Total Production"],
            help="Select between Net Production or Total Production",
            key="option_select"
        )
        
        # Data Source Selection
        data_source = st.radio(
            "**Data Source**",
            ["Use CSV Dataset", "Use Custom Values"],
            horizontal=True,
            help="Choose between pre-loaded CSV data or enter custom MTCO2 values",
            key="data_source"
        )
        
        st.session_state.use_custom_values = (data_source == "Use Custom Values")
        
        if not st.session_state.use_custom_values:
            # Load countries from CSV
            sample_file = "1.1RMV.csv" if option == "Net Production" else "11.1RMV.csv"
            sample_path = get_file_path(option, sample_file.replace(".csv", ""))
            df_sample = load_csv_file(sample_path)
            
            if df_sample is not None:
                countries = sorted(list(df_sample.index))  # Sorted in ascending order
            else:
                countries = sorted(["USA", "China", "Germany", "Japan", "India", 
                                  "Brazil", "France", "UK", "Italy", "Canada"])
            
            # Add "Other" option
            countries_with_other = ["Select Country"] + countries + ["Other"]
            
            country = st.selectbox(
                "**Country**",
                countries_with_other,
                index=0,
                help="Select a country from the dataset",
                key="country_select"
            )
            
            if country == "Select Country":
                st.warning("⚠️ Please select a country")
                year = None
            elif country == "Other":
                st.info("ℹ️ 'Other' selected - using average values")
                year = st.selectbox("**Year**", ["N/A - Using Average"] + list(range(2011, 2041)))
            else:
                year = st.selectbox("**Year**", list(range(2011, 2041)), key="year_select")
                
                # Display sample data
                if df_sample is not None and country in df_sample.index and str(year) in df_sample.columns:
                    value = df_sample.loc[country, str(year)]
                    st.metric("📊 Sample Data Value", f"{value:,.0f} MTCO2", 
                             delta=f"{sample_file} at {year}")
        else:
            # Custom values mode
            st.markdown('<div class="custom-value-box">', unsafe_allow_html=True)
            st.markdown("### 📝 Custom MTCO2 Values")
            st.info("Enter custom MTCO2 values for each parameter group. Values will be used in calculations.")
            
            # Group 1-6 custom values
            col_custom1, col_custom2 = st.columns(2)
            
            with col_custom1:
                st.markdown("**Group 1-4 & Logistics**")
                st.session_state.custom_values['virgin_raw'] = st.number_input(
                    "Virgin Raw Material (MTCO2)",
                    min_value=0.0,
                    value=2000.0,
                    step=100.0,
                    key="custom_virgin",
                    help="Base MTCO2 value for virgin raw materials"
                )
                st.session_state.custom_values['recycled_raw'] = st.number_input(
                    "Recycled Raw Material (MTCO2)",
                    min_value=0.0,
                    value=1200.0,
                    step=100.0,
                    key="custom_recycled",
                    help="Base MTCO2 value for recycled raw materials"
                )
                st.session_state.custom_values['sustainable'] = st.number_input(
                    "Sustainable Sourcing (MTCO2)",
                    min_value=0.0,
                    value=800.0,
                    step=100.0,
                    key="custom_sustainable",
                    help="MTCO2 value for sustainable sourcing"
                )
                st.session_state.custom_values['waste'] = st.number_input(
                    "Waste (MTCO2)",
                    min_value=0.0,
                    value=600.0,
                    step=100.0,
                    key="custom_waste",
                    help="MTCO2 value for waste management"
                )
                st.session_state.custom_values['water'] = st.number_input(
                    "Water Conservation (MTCO2)",
                    min_value=0.0,
                    value=400.0,
                    step=100.0,
                    key="custom_water",
                    help="MTCO2 value for water conservation"
                )
                st.session_state.custom_values['logistics_virgin'] = st.number_input(
                    "Logistics Virgin (MTCO2)",
                    min_value=0.0,
                    value=1200.0,
                    step=100.0,
                    key="custom_log_virgin",
                    help="Base MTCO2 value for virgin material logistics"
                )
                st.session_state.custom_values['logistics_recycled'] = st.number_input(
                    "Logistics Recycled (MTCO2)",
                    min_value=0.0,
                    value=800.0,
                    step=100.0,
                    key="custom_log_recycled",
                    help="Base MTCO2 value for recycled material logistics"
                )
            
            with col_custom2:
                st.markdown("**Group 6 & 7**")
                st.session_state.custom_values['usage'] = st.number_input(
                    "Life Cycle Usage (MTCO2)",
                    min_value=0.0,
                    value=1800.0,
                    step=100.0,
                    key="custom_usage",
                    help="MTCO2 value for life cycle usage"
                )
                
                # Group 7: End of Life - Custom MTCO2 values for each disposal method
                st.markdown("---")
                st.markdown("**Group 7: End of Life Disposal (Base MTCO2 Values)**")
                st.info("Enter base MTCO2 values for each disposal method. Final emissions will be calculated using percentages from Group 7 parameters.")
                
                st.session_state.custom_values['retreading_base'] = st.number_input(
                    "Retreading/Reuse Base (MTCO2)",
                    min_value=0.0,
                    value=400.0,
                    step=50.0,
                    key="custom_retreading_base",
                    help="Base MTCO2 value for retreading/reuse disposal"
                )
                st.session_state.custom_values['recycling_base'] = st.number_input(
                    "Recycling Base (MTCO2)",
                    min_value=0.0,
                    value=300.0,
                    step=50.0,
                    key="custom_recycling_base",
                    help="Base MTCO2 value for recycling disposal"
                )
                st.session_state.custom_values['pyro_base'] = st.number_input(
                    "Pyro/Gasification Base (MTCO2)",
                    min_value=0.0,
                    value=600.0,
                    step=50.0,
                    key="custom_pyro_base",
                    help="Base MTCO2 value for pyrolysis/gasification disposal"
                )
                st.session_state.custom_values['combustion_base'] = st.number_input(
                    "Combustion Base (MTCO2)",
                    min_value=0.0,
                    value=800.0,
                    step=50.0,
                    key="custom_combustion_base",
                    help="Base MTCO2 value for combustion disposal"
                )
                st.session_state.custom_values['landfill_base'] = st.number_input(
                    "Landfill Base (MTCO2)",
                    min_value=0.0,
                    value=1000.0,
                    step=50.0,
                    key="custom_landfill_base",
                    help="Base MTCO2 value for landfill disposal"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
            country = "Custom"
            year = "Custom"
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # ===== PARAMETERS SECTION =====
    st.markdown("## 📋 Parameters")
    st.caption("Parameters marked with 🔴 are required for calculations")
    
    # Group 1: Raw Material
    st.markdown('<div class="group-header"><span class="icon">🏭</span> Group 1: Raw Material <span class="required-badge">REQUIRED</span></div>', unsafe_allow_html=True)
    
    with st.container():
        col_g1_1, col_g1_2, col_g1_3 = st.columns(3)
        
        with col_g1_1:
            virgin_percent = st.slider(
                "Virgin Raw Material (%)",
                40, 100, 60,
                key="virgin_percent",
                help="Must be between 40-100%"
            )
            if virgin_percent < 40:
                st.warning("⚠️ Minimum 40% required")
        
        with col_g1_2:
            recycled_percent = 100 - virgin_percent
            st.metric("Recycled Material", f"{recycled_percent}%", 
                     delta="Recommended: Higher" if virgin_percent > 60 else "Good")
        
        with col_g1_3:
            sustainable = st.radio(
                "Sustainable Sourcing",
                ["Not Available", "Yes"],
                horizontal=True,
                key="sustainable",
                help="Select 'Yes' to include sustainable sourcing"
            )
    
    # Energy Type - FIXED EMPTY LABEL
    st.markdown('<div class="group-header"><span class="icon">⚡</span> Energy Type <span class="required-badge">REQUIRED</span></div>', unsafe_allow_html=True)
    
    energy_type = st.radio(
        "Energy Source",
        ["Renewable Energy 🌿", "Non-Renewable Energy 🔥"],
        horizontal=True,
        key="energy_type",
        label_visibility="collapsed"
    )
    energy_type = "Renewable Energy" if "Renewable" in energy_type else "Non-Renewable Energy"
    
    # Group 2: Energy
    st.markdown('<div class="group-header"><span class="icon">🔋</span> Group 2: Energy</div>', unsafe_allow_html=True)
    
    with st.container():
        if energy_type == "Renewable Energy":
            col_g2_1, col_g2_2 = st.columns(2)
            with col_g2_1:
                renew_virgin = st.number_input(
                    "Renewable Virgin (%)",
                    0, 100, int(virgin_percent),
                    key="renew_virgin",
                    help="Percentage of renewable energy for virgin materials"
                )
            with col_g2_2:
                renew_recycled = st.number_input(
                    "Renewable Recycled (%)",
                    0, 100, int(recycled_percent),
                    key="renew_recycled",
                    help="Percentage of renewable energy for recycled materials"
                )
            nonrenew_virgin = 0
            nonrenew_recycled = 0
        else:
            col_g2_1, col_g2_2 = st.columns(2)
            with col_g2_1:
                nonrenew_virgin = st.number_input(
                    "Non-Renewable Virgin (%)",
                    0, 100, int(virgin_percent),
                    key="nonrenew_virgin",
                    help="Percentage of non-renewable energy for virgin materials"
                )
            with col_g2_2:
                nonrenew_recycled = st.number_input(
                    "Non-Renewable Recycled (%)",
                    0, 100, int(recycled_percent),
                    key="nonrenew_recycled",
                    help="Percentage of non-renewable energy for recycled materials"
                )
            renew_virgin = 0
            renew_recycled = 0
    
    # Group 3: Waste
    st.markdown('<div class="group-header"><span class="icon">🗑️</span> Group 3: Waste</div>', unsafe_allow_html=True)
    
    with st.container():
        waste_option = st.selectbox(
            "Select Waste Minimization Level",
            ["Waste Minimization Absolute", "Waste Minimization Medium", "Waste Minimization High"],
            key="waste_option",
            help="Higher minimization levels reduce emissions",
            index=2  # Default to High
        )
    
    # Group 4: Water Conservation
    st.markdown('<div class="group-header"><span class="icon">💧</span> Group 4: Water Conservation</div>', unsafe_allow_html=True)
    
    with st.container():
        water_option = st.selectbox(
            "Select Water Conservation Level",
            ["Water Conservation Absolute", "Water Conservation Medium", "Water Conservation High"],
            key="water_option",
            help="Higher conservation levels reduce emissions",
            index=2  # Default to High
        )
    
    # Group 5: Logistics - UPDATED WITH PERCENTAGE SELECTION
    st.markdown('<div class="group-header"><span class="icon">🚚</span> Group 5: Logistics</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown("**Select Logistics Material Percentages**")
        col_g5_1, col_g5_2 = st.columns(2)
        
        with col_g5_1:
            logistics_virgin = st.number_input(
                "Logistics Virgin Material (%)",
                0, 100, 50,
                key="logistics_virgin",
                help="Percentage of logistics for virgin materials"
            )
        with col_g5_2:
            logistics_recycled = st.number_input(
                "Logistics Recycled Material (%)", 
                0, 100, 50,
                key="logistics_recycled",
                help="Percentage of logistics for recycled materials"
            )
        
        total_logistics = logistics_virgin + logistics_recycled
        if total_logistics != 100:
            st.error(f"❌ Sum should be 100% (Current: {total_logistics}%)")
        else:
            st.success(f"✅ Logistics percentages sum to 100%")
        
        if sustainable == "Yes" and total_logistics == 100:
            st.info("ℹ️ Using custom logistics percentages")
        elif sustainable == "Not Available" and total_logistics == 100:
            st.info("ℹ️ Using custom logistics percentages (independent from Group 1)")
    
    # Group 6: Life Cycle Usage
    st.markdown('<div class="group-header"><span class="icon">🔄</span> Group 6: Life Cycle Usage</div>', unsafe_allow_html=True)
    
    with st.container():
        usage_option = st.selectbox(
            "Select Usage LCA Level",
            ["Usage LCA Absolute", "Usage LCA Medium", "Usage LCA High"],
            key="usage_option",
            help="Higher LCA levels reduce emissions",
            index=2  # Default to High
        )
    
    # Group 7: End of Life
    st.markdown('<div class="group-header"><span class="icon">♻️</span> Group 7: End of Life <span class="required-badge">SUM = 100%</span></div>', unsafe_allow_html=True)
    
    with st.container():
        st.write("Disposal Methods (%): Must sum to 100%")
        col_g7_1, col_g7_2, col_g7_3, col_g7_4, col_g7_5 = st.columns(5)
        
        with col_g7_1:
            retreading = st.number_input("Retreading", 0, 100, 30, key="retreading",
                                        help="Retreading/Reuse percentage")
        with col_g7_2:
            recycling = st.number_input("Recycling", 0, 100, 40, key="recycling",
                                       help="Recycling percentage")
        with col_g7_3:
            pyro = st.number_input("Pyro/Gas", 0, 100, 20, key="pyro",
                                  help="Pyrolysis/Gasification percentage")
        with col_g7_4:
            combustion = st.number_input("Combustion", 0, 100, 5, key="combustion",
                                        help="Combustion percentage")
        with col_g7_5:
            landfill = st.number_input("Landfill", 0, 100, 5, key="landfill",
                                      help="Landfill percentage")
        
        total_end_life = retreading + recycling + pyro + combustion + landfill
        if total_end_life != 100:
            st.error(f"❌ Sum should be 100% (Current: {total_end_life}%)")
        else:
            st.success(f"✅ Sum is 100% - Good!")
    
    # Calculate Button
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    if st.session_state.use_custom_values or (country != "Select Country" and country is not None):
        calculate_btn = st.button("🚀 **Calculate Emissions**", type="primary", use_container_width=True)
    else:
        st.warning("⚠️ Please select a country or enable custom values to calculate emissions")
        calculate_btn = False

with col_right:
    # ===== RESULTS SECTION =====
    st.markdown("## 📊 Results Dashboard")
    
    if calculate_btn or st.session_state.calculate_btn:
        st.session_state.calculate_btn = True
        
        with st.spinner("🔍 Calculating emissions..."):
            # Determine file prefixes
            if option == "Net Production":
                prefix = "1"
                energy_prefix = "2"
                waste_prefix = "3"
                water_prefix = "3"
                logistics_prefix = "4"
                usage_prefix = "5"
                endlife_prefix = "6"
            else:
                prefix = "11"
                energy_prefix = "12"
                waste_prefix = "13"
                water_prefix = "13"
                logistics_prefix = "14"
                usage_prefix = "15"
                endlife_prefix = "16"
            
            # Initialize calculations
            calculations = {}
            
            if not st.session_state.use_custom_values:
                # Use CSV data
                if country == "Other" or country not in ["Select Country", "Custom"]:
                    # For "Other" countries or normal selections
                    if country == "Other":
                        # Use average values from all countries
                        sample_file = "1.1RMV.csv" if option == "Net Production" else "11.1RMV.csv"
                        sample_path = get_file_path(option, sample_file.replace(".csv", ""))
                        df_sample = load_csv_file(sample_path)
                        if df_sample is not None:
                            avg_values = df_sample.mean().mean()
                        else:
                            avg_values = 1500  # Default average
                        
                        # Apply percentages to average values
                        calculations["Raw Material Virgin"] = avg_values * (virgin_percent / 100)
                        calculations["Raw Material Recycled"] = avg_values * 0.7 * (recycled_percent / 100)
                        calculations["Raw Material Sustainable"] = avg_values * 0.5 if sustainable == "Yes" else 0
                        
                        # Set other values based on averages
                        waste_factors = {"Absolute": 0.4, "Medium": 0.6, "High": 0.8}
                        water_factors = {"Absolute": 0.3, "Medium": 0.5, "High": 0.7}
                        usage_factors = {"Absolute": 0.9, "Medium": 1.1, "High": 1.3}
                        
                        waste_factor = waste_factors[waste_option.split()[-1]]
                        water_factor = water_factors[water_option.split()[-1]]
                        usage_factor = usage_factors[usage_option.split()[-1]]
                        
                        calculations["Waste"] = avg_values * waste_factor
                        calculations["Water Conservation"] = avg_values * water_factor
                        calculations["Life Cycle Usage"] = avg_values * usage_factor
                        
                        # Energy calculations
                        if energy_type == "Renewable Energy":
                            calculations["Energy Renewable Virgin"] = avg_values * 0.8 * (renew_virgin / 100)
                            calculations["Energy Renewable Recycled"] = avg_values * 0.6 * (renew_recycled / 100)
                        else:
                            calculations["Energy Non-Renewable Virgin"] = avg_values * 1.2 * (nonrenew_virgin / 100)
                            calculations["Energy Non-Renewable Recycled"] = avg_values * 1.0 * (nonrenew_recycled / 100)
                        
                        # Logistics - Updated to use new percentages
                        calculations["Logistics Virgin"] = avg_values * 0.6 * (logistics_virgin / 100)
                        calculations["Logistics Recycled"] = avg_values * 0.4 * (logistics_recycled / 100)
                        
                        # End of Life (using average values with percentages)
                        endlife_avg = avg_values * 0.5
                        calculations["End Life Retreading"] = endlife_avg * (retreading / 100) * 0.3
                        calculations["End Life Recycling"] = endlife_avg * (recycling / 100) * 0.4
                        calculations["End Life Pyro/Gas"] = endlife_avg * (pyro / 100) * 0.6
                        calculations["End Life Combustion"] = endlife_avg * (combustion / 100) * 0.9
                        calculations["End Life Landfill"] = endlife_avg * (landfill / 100) * 1.2
                    else:
                        # Normal CSV data loading
                        # Group 1: Raw Material
                        rmv_df = load_csv_file(get_file_path(option, f"{prefix}.1RMV"))
                        rmr_df = load_csv_file(get_file_path(option, f"{prefix}.2RMR"))
                        rms_df = load_csv_file(get_file_path(option, f"{prefix}.3RMS"))
                        
                        rmv_value = get_value(rmv_df, country, year)
                        rmr_value = get_value(rmr_df, country, year)
                        rms_value = get_value(rms_df, country, year) if sustainable == "Yes" else 0
                        
                        calculations["Raw Material Virgin"] = rmv_value * (virgin_percent / 100)
                        calculations["Raw Material Recycled"] = rmr_value * (recycled_percent / 100)
                        calculations["Raw Material Sustainable"] = rms_value
                        
                        # Group 2: Energy
                        if energy_type == "Renewable Energy":
                            erv_df = load_csv_file(get_file_path(option, f"{energy_prefix}.1ERV"))
                            err_df = load_csv_file(get_file_path(option, f"{energy_prefix}.2ERR"))
                            
                            erv_value = get_value(erv_df, country, year)
                            err_value = get_value(err_df, country, year)
                            
                            calculations["Energy Renewable Virgin"] = erv_value * (renew_virgin / 100)
                            calculations["Energy Renewable Recycled"] = err_value * (renew_recycled / 100)
                        else:
                            env_df = load_csv_file(get_file_path(option, f"{energy_prefix}.3ENV"))
                            enr_df = load_csv_file(get_file_path(option, f"{energy_prefix}.4ENR"))
                            
                            env_value = get_value(env_df, country, year)
                            enr_value = get_value(enr_df, country, year)
                            
                            calculations["Energy Non-Renewable Virgin"] = env_value * (nonrenew_virgin / 100)
                            calculations["Energy Non-Renewable Recycled"] = enr_value * (nonrenew_recycled / 100)
                        
                        # Group 3: Waste
                        if waste_option == "Waste Minimization Absolute":
                            waste_file = f"{waste_prefix}.1WSA"
                        elif waste_option == "Waste Minimization Medium":
                            waste_file = f"{waste_prefix}.2WSM"
                        else:
                            waste_file = f"{waste_prefix}.3WSH"
                        
                        waste_df = load_csv_file(get_file_path(option, waste_file))
                        calculations["Waste"] = get_value(waste_df, country, year)
                        
                        # Group 4: Water Conservation
                        if water_option == "Water Conservation Absolute":
                            water_file = f"{water_prefix}.4WWA"
                        elif water_option == "Water Conservation Medium":
                            water_file = f"{water_prefix}.5WWM"
                        else:
                            water_file = f"{water_prefix}.6WWH"
                        
                        water_df = load_csv_file(get_file_path(option, water_file))
                        calculations["Water Conservation"] = get_value(water_df, country, year)
                        
                        # Group 5: Logistics - Updated to use new percentages
                        lev_df = load_csv_file(get_file_path(option, f"{logistics_prefix}.1LEV"))
                        ler_df = load_csv_file(get_file_path(option, f"{logistics_prefix}.2LER"))
                        
                        lev_value = get_value(lev_df, country, year)
                        ler_value = get_value(ler_df, country, year)
                        
                        calculations["Logistics Virgin"] = lev_value * (logistics_virgin / 100)
                        calculations["Logistics Recycled"] = ler_value * (logistics_recycled / 100)
                        
                        # Group 6: Life Cycle Usage
                        if usage_option == "Usage LCA Absolute":
                            usage_file = f"{usage_prefix}.1UEA"
                        elif usage_option == "Usage LCA Medium":
                            usage_file = f"{usage_prefix}.2UEM"
                        else:
                            usage_file = f"{usage_prefix}.3UEH"
                        
                        usage_df = load_csv_file(get_file_path(option, usage_file))
                        calculations["Life Cycle Usage"] = get_value(usage_df, country, year)
                        
                        # Group 7: End of Life
                        elu_df = load_csv_file(get_file_path(option, f"{endlife_prefix}.1ELU"))
                        elr_df = load_csv_file(get_file_path(option, f"{endlife_prefix}.2ELR"))
                        elg_df = load_csv_file(get_file_path(option, f"{endlife_prefix}.3ELG"))
                        elc_df = load_csv_file(get_file_path(option, f"{endlife_prefix}.4ELC"))
                        ele_df = load_csv_file(get_file_path(option, f"{endlife_prefix}.5ELE"))
                        
                        calculations["End Life Retreading"] = get_value(elu_df, country, year) * (retreading / 100)
                        calculations["End Life Recycling"] = get_value(elr_df, country, year) * (recycling / 100)
                        calculations["End Life Pyro/Gas"] = get_value(elg_df, country, year) * (pyro / 100)
                        calculations["End Life Combustion"] = get_value(elc_df, country, year) * (combustion / 100)
                        calculations["End Life Landfill"] = get_value(ele_df, country, year) * (landfill / 100)
            else:
                # Use custom values
                custom = st.session_state.custom_values
                
                calculations["Raw Material Virgin"] = custom['virgin_raw'] * (virgin_percent / 100)
                calculations["Raw Material Recycled"] = custom['recycled_raw'] * (recycled_percent / 100)
                calculations["Raw Material Sustainable"] = custom['sustainable'] if sustainable == "Yes" else 0
                
                if energy_type == "Renewable Energy":
                    calculations["Energy Renewable Virgin"] = custom['virgin_raw'] * 0.6 * (renew_virgin / 100)
                    calculations["Energy Renewable Recycled"] = custom['recycled_raw'] * 0.4 * (renew_recycled / 100)
                else:
                    calculations["Energy Non-Renewable Virgin"] = custom['virgin_raw'] * 0.9 * (nonrenew_virgin / 100)
                    calculations["Energy Non-Renewable Recycled"] = custom['recycled_raw'] * 0.7 * (nonrenew_recycled / 100)
                
                calculations["Waste"] = custom['waste']
                calculations["Water Conservation"] = custom['water']
                calculations["Logistics Virgin"] = custom['logistics_virgin'] * (logistics_virgin / 100)
                calculations["Logistics Recycled"] = custom['logistics_recycled'] * (logistics_recycled / 100)
                calculations["Life Cycle Usage"] = custom['usage']
                
                # Group 7: End of Life with custom base values and percentages
                calculations["End Life Retreading"] = custom['retreading_base'] * (retreading / 100)
                calculations["End Life Recycling"] = custom['recycling_base'] * (recycling / 100)
                calculations["End Life Pyro/Gas"] = custom['pyro_base'] * (pyro / 100)
                calculations["End Life Combustion"] = custom['combustion_base'] * (combustion / 100)
                calculations["End Life Landfill"] = custom['landfill_base'] * (landfill / 100)
            
            # Calculate totals
            total_emissions = sum(calculations.values())
            
            # Group totals for visualization
            group_totals = {
                "🏭 Raw Material": calculations.get("Raw Material Virgin", 0) + 
                                 calculations.get("Raw Material Recycled", 0) + 
                                 calculations.get("Raw Material Sustainable", 0),
                "⚡ Energy": (calculations.get("Energy Renewable Virgin", 0) + 
                            calculations.get("Energy Renewable Recycled", 0) +
                            calculations.get("Energy Non-Renewable Virgin", 0) + 
                            calculations.get("Energy Non-Renewable Recycled", 0)),
                "🗑️ Waste": calculations.get("Waste", 0),
                "💧 Water": calculations.get("Water Conservation", 0),
                "🚚 Logistics": calculations.get("Logistics Virgin", 0) + 
                               calculations.get("Logistics Recycled", 0),
                "🔄 Life Cycle": calculations.get("Life Cycle Usage", 0),
                "♻️ End of Life": (calculations.get("End Life Retreading", 0) + 
                                  calculations.get("End Life Recycling", 0) + 
                                  calculations.get("End Life Pyro/Gas", 0) + 
                                  calculations.get("End Life Combustion", 0) + 
                                  calculations.get("End Life Landfill", 0))
            }
            
            # Store results
            st.session_state.results = {
                'calculations': calculations,
                'group_totals': group_totals,
                'total_emissions': total_emissions,
                'country': country,
                'year': year,
                'option': option,
                'use_custom': st.session_state.use_custom_values
            }
        
        # Display Results
        results = st.session_state.results
        total_emissions = results['total_emissions']
        
        # FINAL RESULT BOX
        st.markdown("### 🎯 Final Result")
        
        # Show data source info
        if results['use_custom']:
            st.info("📝 **Using Custom MTCO2 Values**")
        elif results['country'] == "Other":
            st.info("🌐 **Using Average Values (Other Country)**")
        else:
            st.info(f"📊 **Using CSV Data: {results['country']} - {results['year']}**")
        
        if total_emissions < 0:
            st.markdown(f'''
            <div class="result-box sustainable">
                Net Emissions: {total_emissions:,.2f} MTCO2
            </div>
            ''', unsafe_allow_html=True)
            st.success("### ✅ **The selected strategy is sustainable for Net Zero Tyres**")
            st.balloons()
        else:
            st.markdown(f'''
            <div class="result-box not-sustainable">
                Net Emissions: {total_emissions:,.2f} MTCO2
            </div>
            ''', unsafe_allow_html=True)
            st.error("### ❌ **The selected strategy is NOT sustainable for Net Zero Tyres**")
            
            # SUSTAINABILITY RECOMMENDATIONS
            st.markdown("### 💡 Recommendations for Carbon Neutrality")
            st.markdown('<div class="instruction-box">', unsafe_allow_html=True)
            st.markdown("""
            **For carbon-neutrality, better to use:**
            
            **1. 🏭 Group 1 - Raw Material**: More **Recycled Raw Material** (reduce virgin material percentage)
            
            **2. ⚡ Group 2 - Energy**: Switch to **Renewable Energy** sources
            
            **3. 🗑️ Group 3 - Waste**: Select **Waste Minimization High** 
            
            **4. 💧 Group 4 - Water Conservation**: Select **Water Conservation High**
            
            **5. 🔄 Group 6 - Life Cycle Usage**: Select **Usage LCA High**
            
            **6. ♻️ Group 7 - End of Life Disposal**: Prioritize **Retreading/Reuse, Recycling, and Pyro/Gasification** over Combustion and Landfill
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # NEW: Moon Journey Visualization with Galaxy Stars Night Background
        st.markdown("### 🚗 Journey to the Moon")
        
        # Calculate values
        miles_co2_eq = abs(total_emissions) / 0.0004
        round_trips = miles_co2_eq / 477710
        
        # Determine text based on emissions sign
        if total_emissions < 0:
            emission_text = "miles CO₂ eq. emissions saving"
        else:
            emission_text = "miles CO₂ eq. emissions"
        
        # Moon journey visualization with galaxy stars night background
        st.markdown(f'''
        <div class="moon-journey">
            <div class="star star1">✧</div>
            <div class="star star2">✦</div>
            <div class="star star3">✧</div>
            <div class="star star4">✦</div>
            <div class="star star5">✧</div>
            <div style="display: flex; justify-content: space-around; align-items: center; margin-bottom: 20px;">
                <div>
                    <div class="car-icon">🚗</div>
                    <div class="journey-text">Passenger Car</div>
                </div>
                <div style="font-size: 2rem;">➡️</div>
                <div>
                    <div class="moon-icon">🌕</div>
                    <div class="journey-text">Moon</div>
                </div>
            </div>
            <div class="journey-stats">
                {miles_co2_eq:,.0f} {emission_text}
            </div>
            <div class="journey-text">
                This is equivalent to {round_trips:.1f} round trips to the moon!
            </div>
            <div style="margin-top: 15px; font-size: 0.9rem; color: #a0a0ff;">
                Based on your total emissions of {abs(total_emissions):,.2f} MTCO₂
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Emission Breakdown Chart
        st.markdown("### 📈 Emissions Breakdown by Group")
        
        chart_df = pd.DataFrame({
            "Group": list(results['group_totals'].keys()),
            "Emissions (MTCO2)": list(results['group_totals'].values())
        })
        
        # Create bar chart
        fig = px.bar(
            chart_df,
            x="Group",
            y="Emissions (MTCO2)",
            title="",
            color="Emissions (MTCO2)",
            color_continuous_scale="RdYlGn_r",
            text="Emissions (MTCO2)"
        )
        fig.update_traces(
            texttemplate='%{y:,.0f}',
            textposition='outside',
            marker_line_width=1,
            marker_line_color='darkgray'
        )
        fig.update_layout(
            height=400,
            showlegend=False,
            yaxis_title="MTCO2",
            xaxis_title="",
            plot_bgcolor='white',
            font=dict(size=12)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed Breakdown Table - FIXED THE BACKGROUND_GRADIENT ERROR
        st.markdown("### 📋 Detailed Emission Breakdown")
        
        with st.expander("View Detailed Calculations", expanded=False):
            detailed_df = pd.DataFrame({
                "Category": list(results['calculations'].keys()),
                "MTCO2": list(results['calculations'].values())
            })
            detailed_df["MTCO2"] = detailed_df["MTCO2"].round(2)
            
            # Display with better formatting - FIXED LINE 924
            if matplotlib_available:
                st.dataframe(
                    detailed_df.style.format({'MTCO2': '{:,.2f}'})
                    .background_gradient(subset=['MTCO2'], cmap='RdYlGn_r'),
                    use_container_width=True,
                    height=300
                )
            else:
                # Fallback without matplotlib
                st.dataframe(
                    detailed_df.style.format({'MTCO2': '{:,.2f}'}),
                    use_container_width=True,
                    height=300
                )
                st.warning("⚠️ Matplotlib not available - using simple formatting")
            
            # Download button
            csv = detailed_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Detailed Results",
                data=csv,
                file_name=f"detailed_emissions_{option}_{country}_{year}.csv",
                mime="text/csv",
                type="secondary"
            )
        
        # Summary Metrics
        st.markdown("### 📊 Summary Metrics")
        
        col_sum1, col_sum2, col_sum3 = st.columns(3)
        
        with col_sum1:
            st.metric(
                "Total Emissions",
                f"{total_emissions:,.0f} MTCO2",
                delta="Sustainable" if total_emissions < 0 else "Needs Improvement",
                delta_color="normal" if total_emissions < 0 else "inverse"
            )
        
        with col_sum2:
            max_group = max(results['group_totals'], key=results['group_totals'].get)
            max_value = results['group_totals'][max_group]
            st.metric(
                "Highest Contributor",
                max_group.split(" ")[-1],
                delta=f"{max_value:,.0f} MTCO2"
            )
        
        with col_sum3:
            num_positive = sum(1 for v in results['group_totals'].values() if v > 0)
            st.metric(
                "Groups with Emissions",
                f"{num_positive}/7",
                delta=f"{num_positive*100/7:.0f}%"
            )
    
    else:
        # Initial state - no calculations yet
        st.markdown("### 📊 Results Dashboard")
        st.info("👈 **Set your parameters on the left and click 'Calculate Emissions' to see results here**")
        
        # Placeholder for results
        st.markdown("""
        <div style="text-align: center; padding: 50px; background: #F9FAFB; border-radius: 10px; border: 2px dashed #E5E7EB;">
            <h3 style="color: #6B7280;">📈 Results will appear here</h3>
            <p style="color: #9CA3AF;">Configure parameters and click the calculate button</p>
            <p style="color: #9CA3AF; font-size: 0.9rem; margin-top: 20px;">
                <span style="color: #EF4444;">🔴 Required parameters</span> must be filled<br>
                <span style="color: #10B981;">🟢 Recommended</span> settings for sustainability
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show sample chart (static)
        st.markdown("### 📈 Sample Results Preview")
        
        sample_data = pd.DataFrame({
            "Group": ["🏭 Raw Material", "⚡ Energy", "🗑️ Waste", "💧 Water", 
                     "🚚 Logistics", "🔄 Life Cycle", "♻️ End of Life"],
            "Emissions (MTCO2)": [2500, 1800, 600, 300, 900, 1500, 800]
        })
        
        fig = px.bar(
            sample_data,
            x="Group",
            y="Emissions (MTCO2)",
            title="Sample Emissions Breakdown",
            color="Emissions (MTCO2)",
            color_continuous_scale="RdYlGn_r"
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

# ===== FOOTER =====
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.caption(f"**Production:** {option}")
with footer_col2:
    if st.session_state.use_custom_values:
        st.caption("**Data Source:** Custom Values")
    else:
        st.caption(f"**Location:** {country} | **Year:** {year}")
with footer_col3:
    st.caption("Dashboard v3.1 • Tyre Emissions Calculator")

# ===== DEBUG SECTION (Collapsed) =====
with st.expander("🔧 Debug & Data Info"):
    st.write("### Data Status")
    
    # Check data directories
    data_dirs = ["data/Option1_NetProduction", "data/Option2_TotalProduction"]
    
    for data_dir in data_dirs:
        if os.path.exists(data_dir):
            files = os.listdir(data_dir)
            st.write(f"**{data_dir}**: {len(files)} files")
            
            if files and st.button(f"Show first file from {data_dir.split('/')[-1]}"):
                sample_file = os.path.join(data_dir, files[0])
                try:
                    df = pd.read_csv(sample_file, index_col=0)
                    st.write(f"**File:** {files[0]}")
                    st.write(f"**Shape:** {df.shape}")
                    st.write(f"**Countries:** {sorted(list(df.index))[:10]}...")
                    st.write(f"**Years:** {list(df.columns)[:5]}...")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.error(f"Directory not found: {data_dir}")


