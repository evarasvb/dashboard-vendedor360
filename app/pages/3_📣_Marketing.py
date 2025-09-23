import streamlit as st
import pandas as pd
from utils import read_sheet

st.title("📣 Marketing — Campañas y desempeño")

# Load marketing data
df = read_sheet("Marketing")
if df.empty:
    st.warning("La hoja 'Marketing' está vacía.")
    st.stop()

# Filters
col1, col2 = st.columns(2)
with col1:
    plataforma = st.selectbox(
        "Plataforma",
        options=["(todas)"] + sorted(df["plataforma"].dropna().unique().tolist()),
    )
with col2:
    min_alcance = st.number_input(
        "Alcance mínimo", min_value=0, value=0, step=100
    )

fil = df.copy()
if plataforma != "(todas)":
    fil = fil[fil["plataforma"] == plataforma]
if "alcance" in fil.columns:
    fil = fil[
        pd.to_numeric(fil["alcance"], errors="coerce").fillna(0) >= min_alcance
    ]

cols = [
    "fecha",
    "plataforma",
    "contenido_resumen",
    "alcance",
    "interacciones",
    "clics",
    "leads",
    "costo_ads",
    "url_post",
]
cols = [c for c in cols if c in fil.columns]
st.dataframe(
    fil[cols].sort_values(by="fecha", ascending=False), use_container_width=True
)

# Simple KPI: cost per lead
try:
    costo = pd.to_numeric(fil["costo_ads"], errors="coerce").fillna(0).sum()
    leads = pd.to_numeric(fil["leads"], errors="coerce").fillna(0).sum()
    cpl = (costo / leads) if leads else 0
    st.metric("Costo por lead (filtro aplicado)", f"${cpl:,.0f}")
except Exception:
    pass

st.caption(
    "Sugerencia: republica formatos con mayor relación interacción/alcance y prueba nuevos horarios."
)