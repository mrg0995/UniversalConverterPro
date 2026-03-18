import streamlit as st
import requests
import pandas as pd

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Universal Converter Pro", page_icon="⚖️", layout="wide")

st.title("⚖️ Universal Converter Pro")
st.write("Herramienta integral de conversión para ingeniería, ciencia y finanzas.")

# --- 2. DICCIONARIO DE CONVERSIONES (Unidades Base) ---
categorias = {
    "📏 Longitud": {
        "Metros": 1.0, "Kilómetros": 1000.0, "Centímetros": 0.01, 
        "Millas": 1609.34, "Pies": 0.3048, "Pulgadas": 0.0254
    },
    "⚖️ Peso/Masa": {
        "Kilogramos": 1.0, "Gramos": 0.001, "Libras": 0.453592, "Onzas": 0.0283495
    },
    "📐 Área": {
        "Metros cuadrados": 1.0, "Hectáreas": 10000.0, "Kilómetros cuadrados": 1000000.0, "Acres": 4046.86
    },
    "🧪 Volumen": {
        "Litros": 1.0, "Mililitros": 0.001, "Metros cúbicos": 1000.0, "Galones": 3.78541
    },
    "⏱️ Tiempo": {
        "Segundos": 1.0, "Minutos": 60.0, "Horas": 3600.0, "Días": 86400.0
    },
    "🚀 Velocidad": {
        "m/s": 1.0, "km/h": 0.277778, "Millas/h": 0.44704, "Nudos": 0.514444
    },
    "💾 Datos (Digital)": {
        "Bytes": 1.0, "Kilobytes": 1024.0, "Megabytes": 1048576.0, "Gigabytes": 1073741824.0
    }
}

# --- 3. CREACIÓN DE PESTAÑAS ---
# Definimos los nombres de las pestañas
nombres_tabs = list(categorias.keys()) + ["🌡️Temperatura", "💰Divisa"]
tabs = st.tabs(nombres_tabs)

# --- 4. LÓGICA DE LAS PESTAÑAS AUTOMÁTICAS ---
for i, nombre in enumerate(list(categorias.keys())):
    with tabs[i]:
        st.header(f"Conversor de {nombre}")
        unidades = categorias[nombre]
        
        col1, col2 = st.columns(2)
        with col1:
            valor = st.number_input("Cantidad:", value=1.0, step=0.1, key=f"val_{nombre}")
            de = st.selectbox("De:", list(unidades.keys()), key=f"de_{nombre}")
        with col2:
            a = st.selectbox("A:", list(unidades.keys()), key=f"a_{nombre}")
            resultado = (valor * unidades[de]) / unidades[a]
            st.metric("Resultado:", f"{resultado:.4f} {a}")

# --- 5. PESTAÑA: TEMPERATURA ---
with tabs[-2]:
    st.header("Conversor de 🌡️Temperatura")
    opciones_temp = ["Celsius", "Fahrenheit", "Kelvin"]
    col1, col2 = st.columns(2)
    
    with col1:
        t_val = st.number_input("Grados:", value=25.0, key="t_val")
        t_de = st.selectbox("De:", opciones_temp, key="t_de")
    with col2:
        t_a = st.selectbox("A:", opciones_temp, key="t_a")
        
        # Lógica manual
        if t_de == t_a: res = t_val
        elif t_de == "Celsius":
            res = (t_val * 9/5) + 32 if t_a == "Fahrenheit" else t_val + 273.15
        elif t_de == "Fahrenheit":
            res = (t_val - 32) * 5/9 if t_a == "Celsius" else (t_val - 32) * 5/9 + 273.15
        elif t_de == "Kelvin":
            res = t_val - 273.15 if t_a == "Celsius" else (t_val - 273.15) * 9/5 + 32
            
        st.metric("Resultado:", f"{res:.2f} °{t_a[0]}")

# --- 6. PESTAÑA: DIVISA ---
with tabs[-1]:
    st.header("Conversor de 💰Divisas (Real-time)")
    col1, col2 = st.columns(2)
    monedas = ["EUR", "USD", "GBP", "JPY", "MXN", "ARS", "CLP"]
    
    with col1:
        m_cant = st.number_input("Monto:", value=1.0, key="m_val")
        m_de = st.selectbox("Moneda origen:", monedas, key="m_de")
    with col2:
        m_a = st.selectbox("Moneda destino:", monedas, key="m_a")
        
        if st.button("Actualizar Cambio"):
            try:
                url = f"https://api.exchangerate-api.com/v4/latest/{m_de}"
                datos = requests.get(url).json()
                tasa = datos["rates"][m_a]
                st.success(f"### {m_cant * tasa:.2f} {m_a}")
                st.caption(f"1 {m_de} = {tasa} {m_a}")
            except:
                st.error("Error al conectar con la API de divisas.")

st.divider()
st.caption("Desarrollado por Mario Ramírez • Datos de divisas vía ExchangeRate API")
