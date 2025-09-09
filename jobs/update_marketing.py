# jobs/update_marketing.py
import os
import pandas as pd
from datetime import datetime
from app.gsheet_helper import upsert_tab

SOURCE = os.getenv("MKT_SOURCE_CSV", "")

OUT_COLS = [
    "id_post","plataforma","fecha","contenido_resumen","url_post",
    "alcance","interacciones","clics","leads","costo_ads","observaciones"
]

def main():
    if SOURCE and os.path.exists(SOURCE):
        df = pd.read_csv(SOURCE)
        df = df[[c for c in OUT_COLS if c in df.columns]]
    else:
        today = datetime.now().date().isoformat()
        df = pd.DataFrame([{
            "id_post": f"demo-{today}",
            "plataforma": "facebook",
            "fecha": today,
            "contenido_resumen": "Post de ejemplo",
            "url_post": "",
            "alcance": 0,
            "interacciones": 0,
            "clics": 0,
            "leads": 0,
            "costo_ads": 0,
            "observaciones": "placeholder"
        }], columns=OUT_COLS)
    upsert_tab("Marketing", df, key_cols=["id_post"])

if __name__ == "__main__":
    main()
