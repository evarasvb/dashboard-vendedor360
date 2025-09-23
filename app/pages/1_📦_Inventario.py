import streamlit as st
import pandas as pd
from utils import read_sheet

st.title("📦 Inventario — Productos sin rotación y cobertura")

# Load inventory data
df = read_sheet("Inventario")

if df.empty:
    st.warning("La hoja 'Inventario' está vacía.")
    st.stop()

# Filters
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    categoria = st.selectbox(
        "Categoría",
        options=["(todas)"] + sorted(df["categoria"].dropna().unique().tolist()),
    )
with col_f2:
    dias_min = st.number_input(
        "Días sin venta (mínimo)", min_value=0, value=60, step=5
    )
with col_f3:
    stock_min = st.number_input("Stock mínimo", min_value=0, value=1)

fil = df.copy()
if categoria != "(todas)":
    fil = fil[fil["categoria"] == categoria]
if "dias_sin_venta" in fil.columns:
    fil = fil[
        pd.to_numeric(fil["dias_sin_venta"], errors="coerce").fillna(0) >= dias_min
    ]
if "stock" in fil.columns:
    fil = fil[
        pd.to_numeric(fil["stock"], errors="coerce").fillna(0) >= stock_min
    ]

st.subheader("⚠️ Productos a impulsar")
st.dataframe(
    fil[
        [
            "sku",
            "nombre",
            "categoria",
            "precio",
            "stock",
            "dias_sin_venta",
            "url_imagen",
            "proveedor",
        ]
    ]
    .sort_values(by=["dias_sin_venta", "stock"], ascending=[False, False]),
    use_container_width=True,
)

st.caption(
    "Sugerencia: lanza campañas flash/combos para los SKUs con más días sin venta."
)