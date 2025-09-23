import streamlit as st
import pandas as pd
from utils import read_sheet

st.title("📈 Licitaciones — Pipeline y resultados")

# Load data
df = read_sheet("Licitaciones")
if df.empty:
    st.warning("La hoja 'Licitaciones' está vacía.")
    st.stop()

# Filters
col_f1, col_f2 = st.columns(2)
with col_f1:
    plataforma = st.selectbox(
        "Plataforma",
        options=["(todas)"] + sorted(df["plataforma"].dropna().unique().tolist()),
    )
with col_f2:
    estado = st.selectbox(
        "Estado",
        options=["(todos)", "enviada", "omitida", "ganada", "perdida"],
    )

fil = df.copy()
if plataforma != "(todas)":
    fil = fil[fil["plataforma"] == plataforma]
if estado != "(todos)":
    fil = fil[fil["estado"].str.lower().fillna("") == estado]

st.subheader("🧾 Oportunidades")
cols = [
    "id_licitacion",
    "plataforma",
    "titulo",
    "fecha_cierre",
    "estado",
    "items_total",
    "items_ofertados",
    "total_ofertado",
    "motivo_omitida",
    "precio_ganador",
    "adjudicatario",
]
cols = [c for c in cols if c in fil.columns]
st.dataframe(
    fil[cols].sort_values(by="fecha_cierre", ascending=True), use_container_width=True
)

# Quick success rate
try:
    tot_env = (df["estado"].str.lower() == "enviada").sum()
    gan = (df["estado"].str.lower() == "ganada").sum()
    tasa = (gan / tot_env * 100) if tot_env else 0
    st.metric("Tasa de éxito (global)", f"{tasa:.1f}%")
except Exception:
    pass

st.caption(
    "Tip: si la mayoría de pérdidas son por precio, ajusta márgenes en esos SKUs/conjuntos."
)