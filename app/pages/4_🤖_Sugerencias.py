import streamlit as st
from utils import read_sheet

st.title("🤖 Sugerencias — Aprendizaje continuo")

# Load suggestions
df = read_sheet("Sugerencias")
if df.empty:
    st.info(
        "Sin sugerencias todavía. Cuando conectemos los jobs, aquí verás recomendaciones diarias."
    )
else:
    st.dataframe(
        df.sort_values(by=["prioridad", "fecha"], ascending=[True, False]),
        use_container_width=True,
    )

st.markdown(
    """
**Cómo se llenará esta sección (al conectar los jobs):**
- Inventario: SKUs con >60 días sin venta → crear combos/flash sale.
- Licitaciones: pérdidas por precio → bajar margen o buscar proveedor alternativo.
- Marketing: republicar contenidos con mejor CTR/engagement; cambiar horarios.
"""
)