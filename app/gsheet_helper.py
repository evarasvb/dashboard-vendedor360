import os
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe

"""
Helper functions for interacting with Google Sheets.

This module centralizes reading and writing operations to the Google
Sheets-based DataHub. It uses the service account credentials
configured via environment variables to authenticate and perform
actions against the spreadsheet defined by `SHEET_NAME`.

Functions
---------
read_tab(tab: str) -> pd.DataFrame
    Return a pandas DataFrame for a given sheet tab. Columns are
    normalized to strings and rows with all NaN values are dropped.

write_tab(tab: str, df: pd.DataFrame)
    Clear the contents of the specified tab and write the provided
    DataFrame, including column headers, but excluding the index.

upsert_tab(tab: str, df_new: pd.DataFrame, key_cols: list[str])
    Merge the existing tab with `df_new` on `key_cols`, updating any
    overlapping records with values from `df_new`. Non-overlapping
    rows are preserved from both datasets. This is useful for
    accumulating incremental updates while preserving historical data.
"""

SHEET_NAME = os.getenv("SHEET_NAME", "Vendedor360_DataHub")
SA_PATH = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "data/service_account.json")

def _gc() -> gspread.client.Client:
    """Authorize and return a gspread client using service account credentials."""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(SA_PATH, scopes)
    return gspread.authorize(creds)

def read_tab(tab: str) -> pd.DataFrame:
    """
    Read a tab from the Google Sheet into a pandas DataFrame.

    Parameters
    ----------
    tab : str
        The name of the worksheet tab to read.

    Returns
    -------
    pd.DataFrame
        DataFrame with normalized column names; all-NaN rows removed.
    """
    gc = _gc()
    sh = gc.open(SHEET_NAME)
    ws = sh.worksheet(tab)
    df = get_as_dataframe(ws, evaluate_formulas=True, header=0)
    if df.empty:
        return pd.DataFrame()
    df = df.dropna(how="all")
    df.columns = [str(c).strip() for c in df.columns]
    return df

def write_tab(tab: str, df: pd.DataFrame) -> None:
    """
    Overwrite a sheet tab with the contents of a DataFrame.

    Parameters
    ----------
    tab : str
        The tab name to clear and write to.
    df : pd.DataFrame
        The DataFrame to write. Index is not included.
    """
    gc = _gc()
    sh = gc.open(SHEET_NAME)
    ws = sh.worksheet(tab)
    ws.clear()
    set_with_dataframe(ws, df, include_index=False, include_column_header=True)

def upsert_tab(tab: str, df_new: pd.DataFrame, key_cols: list[str]) -> None:
    """
    Upsert new rows into an existing tab based on key columns.

    This function reads the existing tab, merges it with the new
    DataFrame on the specified key columns, and writes back the result.
    New values take precedence over old ones.

    Parameters
    ----------
    tab : str
        The name of the tab to upsert into.
    df_new : pd.DataFrame
        The new DataFrame with updates.
    key_cols : list[str]
        Columns used to match rows between the existing sheet and
        new data. Duplicate keys in the new data will overwrite
        previous values.
    """
    df_old = read_tab(tab)
    if df_old.empty:
        write_tab(tab, df_new)
        return
    # ensure keys are string for proper matching
    for c in key_cols:
        if c in df_old.columns:
            df_old[c] = df_old[c].astype(str)
        if c in df_new.columns:
            df_new[c] = df_new[c].astype(str)
    merged = pd.merge(
        df_old,
        df_new,
        on=key_cols,
        how="outer",
        suffixes=("_old", ""),
    )
    # prefer new data (non-suffixed) over old
    cols_final = []
    for col in merged.columns:
        if col.endswith("_old"):
            base = col[:-4]
            # skip old if new exists
            if base in merged.columns:
                continue
        cols_final.append(col)
    merged = merged[cols_final]
    write_tab(tab, merged)
