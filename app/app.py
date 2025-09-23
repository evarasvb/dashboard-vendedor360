import streamlit as st
from utils import read_sheet, kpi_value

st.set_page_config(page_title="Dashboard Vendedor360", page_icon="🧭", layout="wide")

st.title("🧭 Dashboard Unificado — Vendedor360 (MVP)")

# Read data from Google Sheets
inv = read_sheet("Inventario")
lic = read_sheet("Licitaciones")
mkt = read_sheet("Marketing")
sug = read_sheet("Sugerencias")

# Top-level KPI metrics
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("SKUs en catálogo", kpi_value(inv, "sku", "count"))
with c2:
    st.metric("Licitaciones (últimos 30 días)", kpi_value(lic, "id_licitacion", "count"))
with c3:
    st.metric("Publicaciones marketing (30 días)", kpi_value(mkt, "id_post", "count"))
with c4:
    pending = 0 if sug.empty else (sug["estado"].fillna("").str.lower() == "nueva").sum()
    st.metric("Sugerencias pendientes", pending)

st.info("Usa el menú lateral para navegar: Inventario, Licitaciones, Marketing, Sugerencias.")