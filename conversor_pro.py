import streamlit as st
import requests
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Universal Converter Pro", page_icon="⚖️", layout="wide")

st.title("⚖️ Universal Converter Pro")
st.write("Comprehensive conversion tool for engineering, science, and finance.")

# --- 2. CONVERSION DICTIONARY (Base Units) ---
categories = {
    "📏 Length": {
        "Meters": 1.0, "Kilometers": 1000.0, "Centimeters": 0.01, 
        "Miles": 1609.34, "Feet": 0.3048, "Inches": 0.0254
    },
    "⚖️ Weight/Mass": {
        "Kilograms": 1.0, "Grams": 0.001, "Pounds": 0.453592, "Ounces": 0.0283495
    },
    "📐 Area": {
        "Square Meters": 1.0, "Hectares": 10000.0, "Square Kilometers": 1000000.0, "Acres": 4046.86
    },
    "🧪 Volume": {
        "Liters": 1.0, "Milliliters": 0.001, "Cubic Meters": 1000.0, "Gallons": 3.78541
    },
    "⏱️ Time": {
        "Seconds": 1.0, "Minutes": 60.0, "Hours": 3600.0, "Days": 86400.0
    },
    "🚀 Speed": {
        "m/s": 1.0, "km/h": 0.277778, "mph": 0.44704, "Knots": 0.514444
    },
    "💾 Data (Digital)": {
        "Bytes": 1.0, "Kilobytes": 1024.0, "Megabytes": 1048576.0, "Gigabytes": 1073741824.0
    }
}

# --- 3. TAB CREATION ---
tab_names = list(categories.keys()) + ["🌡️ Temperature", "💰 Currency"]
tabs = st.tabs(tab_names)

# --- 4. AUTOMATIC TABS LOGIC (Standard Units) ---
for i, name in enumerate(list(categories.keys())):
    with tabs[i]:
        st.header(f"{name} Converter")
        units = categories[name]
        
        col1, col2 = st.columns(2)
        with col1:
            value = st.number_input("Amount:", value=1.0, step=0.1, key=f"val_{name}")
            from_unit = st.selectbox("From:", list(units.keys()), key=f"from_{name}")
        with col2:
            to_unit = st.selectbox("To:", list(units.keys()), key=f"to_{name}")
            result = (value * units[from_unit]) / units[to_unit]
            st.metric("Result:", f"{result:.4f} {to_unit}")

# --- 5. TAB: TEMPERATURE ---
with tabs[-2]:
    st.header("🌡️ Temperature Converter")
    temp_options = ["Celsius", "Fahrenheit", "Kelvin"]
    col1, col2 = st.columns(2)
    
    with col1:
        t_val = st.number_input("Degrees:", value=25.0, key="t_val")
        t_from = st.selectbox("From:", temp_options, key="t_from")
    with col2:
        t_to = st.selectbox("To:", temp_options, key="t_to")
        
        # Manual conversion logic
        if t_from == t_to: 
            res = t_val
        elif t_from == "Celsius":
            res = (t_val * 9/5) + 32 if t_to == "Fahrenheit" else t_val + 273.15
        elif t_from == "Fahrenheit":
            res = (t_val - 32) * 5/9 if t_to == "Celsius" else (t_val - 32) * 5/9 + 273.15
        elif t_from == "Kelvin":
            res = t_val - 273.15 if t_to == "Celsius" else (t_val - 273.15) * 9/5 + 32
            
        st.metric("Result:", f"{res:.2f} °{t_to[0]}")

# --- 6. TAB: CURRENCY ---
with tabs[-1]:
    st.header("💰 Currency Converter (Real-time)")
    col1, col2 = st.columns(2)
    currencies = ["EUR", "USD", "GBP", "JPY", "MXN", "ARS", "CLP"]
    
    with col1:
        m_amount = st.number_input("Amount:", value=1.0, key="m_val")
        m_from = st.selectbox("Source Currency:", currencies, key="m_from")
    with col2:
        m_to = st.selectbox("Target Currency:", currencies, key="m_to")
        
        if st.button("Update Exchange Rate"):
            try:
                url = f"https://api.exchangerate-api.com/v4/latest/{m_from}"
                data = requests.get(url).json()
                rate = data["rates"][m_to]
                st.success(f"### {m_amount * rate:.2f} {m_to}")
                st.caption(f"1 {m_from} = {rate} {m_to}")
            except:
                st.error("Error connecting to the Currency API.")

st.divider()
st.caption("Developed by Mario Ramírez • Currency data via ExchangeRate API")
