import streamlit as st
import pandas as pd
from utils import read_sheet

st.title("Inventario - Productos y cobertura")

df = read_sheet("Inventario")
if df.empty:
    st.warning("La hoja 'Inventario' esta vacia.")
    st.stop()

cat = "(todas)"
dias_min = 60
stock_min = 1

col1, col2, col3 = st.columns(3)
with col1:
    if "categoria" in df.columns:
        cat = st.selectbox("Categoria", ["(todas)"] + sorted(df["categoria"].dropna().unique().tolist()))
with col2:
    dias_min = st.number_input("Dias sin venta (minimo)", min_value=0, value=60, step=5)
with col3:
    stock_min = st.number_input("Stock minimo", min_value=0, value=1)

fil = df.copy()
if cat != "(todas)" and "categoria" in fil.columns:
    fil = fil[fil["categoria"] == cat]
if "dias_sin_venta" in fil.columns:
    fil = fil[pd.to_numeric(fil["dias_sin_venta"], errors="coerce").fillna(0) >= dias_min]
if "stock" in fil.columns:
    fil = fil[pd.to_numeric(fil["stock"], errors="coerce").fillna(0) >= stock_min]

cols = [c for c in ["sku","nombre","categoria","precio","stock","dias_sin_venta","url_imagen","proveedor"] if c in fil.columns]
st.dataframe(fil[cols].sort_values(by=[x for x in ["dias_sin_venta","stock"] if x in cols], ascending=[False, False]), use_container_width=True)
