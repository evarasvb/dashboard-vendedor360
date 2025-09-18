import csv
import sys
import json
import pathlib


REQ = [
    "id",
    "title",
    "description",
    "availability",
    "condition",
    "price",
    "link",
    "image_link",
    "brand",
]


def to_row(p):
    precio_neto = float(p.get("precio_neto", 0) or 0)
    precio_bruto = int(round(precio_neto * 1.19))
    return {
        "id": p.get("sku", ""),
        "title": (p.get("nombre", "") or "")[:150],
        "description": (p.get("descripcion", "") or "")[:5000],
        "availability": "in stock" if (p.get("stock", 0) or 0) > 0 else "out of stock",
        "condition": "new",
        "price": f"{precio_bruto} CLP",
        "link": p.get("url_pdp", ""),
        "image_link": p.get("url_imagen", ""),
        "brand": p.get("marca", ""),
        "gtin": p.get("gtin", ""),
        "mpn": p.get("mpn", ""),
    }


def main(in_json, out_csv):
    items = json.loads(pathlib.Path(in_json).read_text(encoding="utf-8"))
    with open(out_csv, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "title",
                "description",
                "availability",
                "condition",
                "price",
                "link",
                "image_link",
                "brand",
                "gtin",
                "mpn",
            ],
        )
        w.writeheader()
        for p in items:
            w.writerow(to_row(p))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python tasks/meta_catalog_csv.py productos.json products.csv")
        raise SystemExit(2)
    main(sys.argv[1], sys.argv[2])

