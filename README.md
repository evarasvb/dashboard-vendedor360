# Dashboard Vendedor360 (MVP)

Este proyecto contiene un panel de control inicial (MVP) construido con
[Streamlit](https://streamlit.io/) para integrar información de inventario,
licitaciones, marketing y sugerencias en una sola interfaz.

## Estructura

```
dashboard-vendedor360/
├── app/                  # Aplicación Streamlit
│   ├── app.py            # Página principal con KPIs
│   ├── utils.py          # Conectores a Google Sheets
│   └── pages/            # Subpáginas del dashboard
│       ├── 1_📦_Inventario.py    # Inventario y SKUs sin rotación
│       ├── 2_💍_Licitaciones.py   # Licitaciones enviadas/ganadas/perdidas
│       ├── 3_🔣_Marketing.py      # Desempeño de campañas en redes
│       └── 4_🤖_Sugerencias.py    # Recomendaciones automáticas
├── data/
│   └── service_account.json      # Credenciales de la cuenta de servicio (no incluido)
├── jobs/                 # Scripts para alimentar las hojas
│   ├── update_inventory.py
│   ├── update_bids.py
│   └── update_marketing.py
├── requirements.txt      # Dependencias del entorno
└── README.md
```

## Instalación y uso

1. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

2. Configura tus variables de entorno en un archivo `.env` o exporta variables
   en tu shell:

   ```env
   SHEET_NAME=Vendedor360_DataHub
   GOOGLE_SERVICE_ACCOUNT_JSON=data/service_account.json
   ```

   Debes crear una hoja de cálculo de Google llamada `Vendedor360_DataHub` con
   las pestañas `Inventario`, `Licitaciones`, `Marketing` y
   `Sugerencias`, y compartirla con la cuenta de servicio.

3. Ejecuta el dashboard localmente:

   ```bash
   streamlit run app/app.py
   ```

   Luego abre tu navegador en la URL indicada (por defecto
   `http://localhost:8501`).

## Próximos pasos

- Completar los scripts en `jobs/` para que lean datos de los agentes
  automatizados (Vendedor360, metaops, etc.) y actualicen las hojas de
  Google automáticamente.
- Desplegar el dashboard en un servicio cloud o mediante GitHub Actions.
- Agregar autenticación y control de permisos si se requiere.
