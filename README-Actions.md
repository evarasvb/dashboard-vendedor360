# DataHub - GitHub Actions

This repository uses GitHub Actions to keep the internal DataHub (a
Google Sheet named `Vendedor360_DataHub`) up to date. The workflow
fetches data from local sources (inventory CSV/Excel, logs from the
Vendedor360 bots, and marketing metrics) and writes it into the
appropriate tabs.

## Setup

Before running the workflow, you must:

1. **Share the Google Sheet** `Vendedor360_DataHub` with the service
   account email specified in your `service_account.json` file. This
   ensures the action can read and write the sheet.
2. **Add a GitHub secret** named `GOOGLE_SERVICE_ACCOUNT_JSON` in
   Settings → Secrets and variables → Actions. The value should be
   the entire JSON content of your service account key file.
3. (Optional) Create additional secrets or environment variables if
   your data sources are not committed to the repository. For example,
   you can set `INVENTARIO_SOURCE_CSV`, `V360_LOGS_DIR`, or
   `MKT_SOURCE_CSV` through repository variables.

## Running the workflow

The workflow is scheduled to run every hour via cron. You can also
trigger it manually from the GitHub Actions tab by selecting
“Vendedor360 DataHub - Hourly” and clicking **Run workflow**.

### What it does

The workflow performs three main tasks:

1. **Update Inventario**: reads your configured inventory source
   (default is `DataHub_Inventario.csv` in the repo) and upserts
   products into the `Inventario` tab using `app/gsheet_helper.py`.
2. **Update Licitaciones**: parses JSON logs from the Vendedor360
   agents (expected in `logs/`) and upserts results into the
   `Licitaciones` tab.
3. **Update Marketing**: placeholder script that can be extended to
   pull metrics from Meta/LinkedIn via `metaops` or other sources and
   update the `Marketing` tab.

It optionally commits any modified artifacts back into the repository
for auditing. If there are no changes, it simply exits.

## Customizing

- To change the schedule, modify the `cron` entry in
  `.github/workflows/datahub.yml`.
- To use a different inventory file, set the `INVENTARIO_SOURCE_CSV`
  variable either in the workflow file or as a repository variable.
- To integrate marketing metrics, implement the logic in
  `jobs/update_marketing.py` and set `MKT_SOURCE_CSV` accordingly.

By centralizing data flows in this repository and using GitHub
Actions, you maintain a reproducible and auditable pipeline for your
business data.
