# jobs/update_inventory.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from app.gsheet_helper import upsert_tab

# Config: fuente flexible
# Puedes apuntar a un CSV (commiteado) o Excel. Si tienes una Sheet fuente,
# podriamos leerla tambien, pero para empezar usa un archivo del repo.
SOURCE = os.getenv("INVENTARIO_SOURCE_CSV", "DataHub_Inventario.csv")

OUT_COLS = ["sku", "nombre", "categoria", "costo", "precio", "stock", "stock_min", "dias_sin_venta", "url_imagen", "proveedor"]

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    mapping = {
        "sku": ["sku", "codigo", "codarticulo", "id", "codigo_sku"],
        "nombre": ["nombre", "descripcion", "descripcion articulo", "producto"],
        "categoria": ["categoria", "familia", "rubro"],
        "costo": ["costo", "costo un", "costo unitario", "costo promedio unitario"],
        "precio": ["precio", "precio venta", "precio unitario"],
        "stock": ["stock", "inventario", "saldo stock", "unidades", "cantidad"],
        "stock_min": ["stock_min", "stock min"],
        "dias_sin_venta": ["dias_sin_venta", "dias sin venta"],
        "url_imagen": ["url_imagen", "imagen", "url imagen"],
        "proveedor": ["proveedor", "empresa", "vendor"]
    }
    out = pd.DataFrame(columns=OUT_COLS)
    # Normalizar nombres de columnas
    df = df.rename(columns={c: str(c).strip().lower() for c in df.columns})

    def pick(key):
        for cand in mapping[key]:
            if cand in df.columns:
                return df[cand]
        return None

    for k in OUT_COLS:
        out[k] = pick(k)

    # Convertir columnas numericas
    for n in ["costo", "precio", "stock", "stock_min", "dias_sin_venta"]:
        if n in out.columns:
            out[n] = pd.to_numeric(out[n], errors="coerce")

    # Si stock_min esta vacio, llenar con 0
    if out["stock_min"].isna().all():
        out["stock_min"] = 0

    # Eliminar filas sin SKU y resetear indice
    out = out.dropna(subset=["sku"]).reset_index(drop=True)
    return out

def main():
    if not os.path.exists(SOURCE):
        print(f"Source not found: {SOURCE}")
        return
    # Leer archivo CSV o Excel segun extension
    df = pd.read_excel(SOURCE) if SOURCE.lower().endswith(".xlsx") else pd.read_csv(SOURCE)
    clean = normalize(df)
    if clean.empty:
        print("No inventory data to update.")
        return
    upsert_tab("Inventario", clean, key_cols=["sku"])

if __name__ == "__main__":
    main()
