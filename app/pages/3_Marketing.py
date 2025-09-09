import streamlit as st
import pandas as pd
from utils import read_sheet

st.title("Marketing - Campanas y desempeno")

# Cargar datos



df = read_sheet("Marketing")
if df.empty:
    st.warning("La hoja 'Marketing' esta vacia.")
    st.stop()

# Filtros
plataforma = "(todas)"
min_alcance = 0
col1, col2 = st.columns(2)
with col1:
    if "plataforma" in df.columns:
        plataforma = st.selectbox("Plataforma", ["(todas)"] + sorted(df["plataforma"].dropna().unique().tolist()))
with col2:
    min_alcance = st.number_input("Alcance minimo", min_value=0, value=0, step=100)

# Filtrado
fil = df.copy()
if plataforma != "(todas)" and "plataforma" in fil.columns:
    fil = fil[fil["plataforma"] == plataforma]
if "alcance" in fil.columns:
    fil = fil[pd.to_numeric(fil["alcance"], errors="coerce").fillna(0) >= min_alcance]

# Columnas a mostrar
cols = [c for c in ["fecha","plataforma","contenido_resumen","alcance","interacciones","clics","leads","costo_ads","url_post"] if c in fil.columns]

# Mostrar datos
if cols:
    st.dataframe(
        fil[cols].sort_values(by=[c for c in ["fecha"] if c in cols], ascending=False),
        use_container_width=True
    )

# Calcula costo por lead
try:
    costo = pd.to_numeric(fil.get("costo_ads", 0), errors="coerce").fillna(0).sum()
    leads = pd.to_numeric(fil.get("leads", 0), errors="coerce").fillna(0).sum()
    cpl = (costo / leads) if leads else 0
    st.metric("Costo por lead (filtro aplicado)", f"{cpl:,.0f}")
except Exception:
    pass
