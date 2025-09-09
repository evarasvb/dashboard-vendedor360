import streamlit as st
import pandas as pd
from utils import read_sheet

st.title("Licitaciones - Pipeline y resultados")

df = read_sheet("Licitaciones")
if df.empty:
    st.warning("La hoja 'Licitaciones' esta vacia.")
    st.stop()

plataforma = "(todas)"
estado = "(todos)"
col1, col2 = st.columns(2)
with col1:
    if "plataforma" in df.columns:
        plataforma = st.selectbox("Plataforma", ["(todas)"] + sorted(df["plataforma"].dropna().unique().tolist()))
with col2:
    estado = st.selectbox("Estado", ["(todos)","enviada","omitida","ganada","perdida"])

fil = df.copy()
if plataforma != "(todas)" and "plataforma" in fil.columns:
    fil = fil[fil["plataforma"] == plataforma]
if estado != "(todos)" and "estado" in fil.columns:
    fil = fil[fil["estado"].str.lower().fillna("") == estado]

cols = [c for c in ["id_licitacion","plataforma","titulo","fecha_cierre","estado","items_total","items_ofertados","total_ofertado","motivo_omitida","precio_ganador","adjudicatario"] if c in fil.columns]
st.dataframe(fil[cols].sort_values(by=[c for c in ["fecha_cierre"] if c in cols], ascending=True), use_container_width=True)

try:
    tot_env = (df["estado"].str.lower() == "enviada").sum() if "estado" in df.columns else 0
    gan = (df["estado"].str.lower() == "ganada").sum() if "estado" in df.columns else 0
    tasa = (gan / tot_env * 100) if tot_env else 0
    st.metric("Tasa de exito (global)", f"{tasa:.1f}%")
except Exception:
    pass
