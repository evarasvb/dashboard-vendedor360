# jobs/update_bids.py
import os, glob, json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from datetime import datetime
from app.gsheet_helper import upsert_tab

LOGS_DIR = os.getenv("V360_LOGS_DIR", "logs")

OUT_COLS = [
    "id_licitacion","plataforma","titulo","fecha_publicacion","fecha_cierre",
    "estado","items_total","items_ofertados","total_ofertado","motivo_omitida",
    "precio_ganador","adjudicatario"
]

def read_jsons(pattern: str):
    rows = []
    for p in glob.glob(pattern):
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    rows.extend(data)
        except Exception:
            # Ignorar archivos mal formados
            pass
    return rows

def normalize(rows):
    out = []
    for r in rows:
        idl = r.get("id_licitacion") or r.get("id") or ""
        plataforma = r.get("plataforma") or r.get("source") or ""
        titulo = r.get("titulo") or r.get("title") or ""
        estado = r.get("estado") or r.get("status") or ""
        fp = r.get("fecha_publicacion") or r.get("publicacion") or ""
        fc = r.get("fecha_cierre") or r.get("cierre") or ""
        items_tot = r.get("items_total") or r.get("items")
        items_of = r.get("items_ofertados")
        total_ofe = r.get("total_ofertado")
        motivo = r.get("motivo_omitida") or r.get("motivo") or ""
        ganador = r.get("precio_ganador")
        adj = r.get("adjudicatario") or ""

        # Generar ID si falta (p. ej., fuentes privadas)
        if not idl and titulo:
            idl = f"WXRX-{abs(hash(titulo))%1000000}"

        out.append({
            "id_licitacion": idl,
            "plataforma": plataforma,
            "titulo": titulo,
            "fecha_publicacion": fp,
            "fecha_cierre": fc,
            "estado": estado,
            "items_total": items_tot,
            "items_ofertados": items_of,
            "total_ofertado": total_ofe,
            "motivo_omitida": motivo,
            "precio_ganador": ganador,
            "adjudicatario": adj
        })

    df = pd.DataFrame(out, columns=OUT_COLS)
    for c in ["fecha_publicacion", "fecha_cierre"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce").dt.date.astype(str)
    return df

def main():
    rows = []
    rows += read_jsons(os.path.join(LOGS_DIR, "mp_*.json"))
    rows += read_jsons(os.path.join(LOGS_DIR, "wherex_*.json"))
    rows += read_jsons(os.path.join(LOGS_DIR, "senegocia_*.json"))

    if not rows:
        print("No bid logs found.")
        return

    df = normalize(rows).dropna(subset=["id_licitacion"]).reset_index(drop=True)
    upsert_tab("Licitaciones", df, key_cols=["id_licitacion"])

if __name__ == "__main__":
    main()
