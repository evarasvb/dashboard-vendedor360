import csv
import json
import sys
import pathlib


# Lee productos.json y genera convenio_marco.csv con columnas estándar.
# Ajusta FIELD_MAP según tu fuente.
FIELD_MAP = {
    "sku": "sku",
    "nombre": "nombre",
    "descripcion": "descripcion",
    "precio_neto": "precio_neto",
    "unidad": "unidad",
    "marca": "marca",
    "gtin": "gtin",
    "imagen": "url_imagen",
    "categoria": "categoria",
    "stock": "stock",
}


OUT_COLUMNS = [
    "SKU",
    "Nombre",
    "Descripción",
    "PrecioNeto",
    "IVA",
    "PrecioBruto",
    "Unidad",
    "Marca",
    "GTIN",
    "URLImagen",
    "Categoría",
    "Stock",
]


def to_row(p):
    precio_neto = float(p.get(FIELD_MAP["precio_neto"], 0) or 0)
    iva = round(precio_neto * 0.19, 2)
    bruto = round(precio_neto + iva, 2)
    return {
        "SKU": p.get(FIELD_MAP["sku"], ""),
        "Nombre": (p.get(FIELD_MAP["nombre"], "") or "")[:150],
        "Descripción": (p.get(FIELD_MAP["descripcion"], "") or "")[:5000],
        "PrecioNeto": f"{precio_neto:.2f}",
        "IVA": f"{iva:.2f}",
        "PrecioBruto": f"{bruto:.2f}",
        "Unidad": p.get(FIELD_MAP["unidad"], "UN"),
        "Marca": p.get(FIELD_MAP["marca"], ""),
        "GTIN": p.get(FIELD_MAP["gtin"], ""),
        "URLImagen": p.get(FIELD_MAP["imagen"], ""),
        "Categoría": p.get(FIELD_MAP["categoria"], ""),
        "Stock": p.get(FIELD_MAP["stock"], 0),
    }


def main(in_json: str, out_csv: str):
    items = json.loads(pathlib.Path(in_json).read_text(encoding="utf-8"))
    with open(out_csv, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=OUT_COLUMNS)
        w.writeheader()
        for p in items:
            w.writerow(to_row(p))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python tasks/cm_catalog_export.py productos.json convenio_marco.csv")
        raise SystemExit(2)
    main(sys.argv[1], sys.argv[2])

