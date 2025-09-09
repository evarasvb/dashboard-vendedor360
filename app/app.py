import streamlit as st
from utils import read_sheet, kpi_value

st.set_page_config(page_title="Dashboard Vendedor360", page_icon="D", layout="wide")
st.title("Dashboard Unificado - Vendedor360 (MVP)")

inv = read_sheet("Inventario")
lic = read_sheet("Licitaciones")
mkt = read_sheet("Marketing")
sug = read_sheet("Sugerencias")

# KPIs superiores
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("SKUs en catalogo", kpi_value(inv, "sku", "count"))
with c2:
    st.metric("Licitaciones (ultimos 30 dias)", kpi_value(lic, "id_licitacion", "count"))
with c3:
    st.metric("Publicaciones marketing (30 dias)", kpi_value(mkt, "id_post", "count"))
with c4:
    pendientes = 0
    if not sug.empty and "estado" in sug.columns:
        pendientes = (sug["estado"].fillna("").str.lower() == "nueva").sum()
    st.metric("Sugerencias pendientes", pendientes)

st.info("Usa el menu lateral para navegar: Inventario, Licitaciones, Marketing, Sugerencias.")
