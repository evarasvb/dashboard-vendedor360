import streamlit as st
from utils import read_sheet

st.title("Sugerencias - Aprendizaje continuo")

df = read_sheet("Sugerencias")
if df.empty:
    st.info("Sin sugerencias todavia. Cuando conectemos los jobs, aqui veras recomendaciones diarias.")
else:
    cols_orden = [c for c in ["prioridad","fecha","origen","sugerencia","impacto_esperado","estado"] if c in df.columns]
    st.dataframe(
        df[cols_orden].sort_values(by=[c for c in ["prioridad","fecha"] if c in cols_orden], ascending=[True, False]),
        use_container_width=True
    )
