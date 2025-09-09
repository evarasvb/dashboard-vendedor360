import os
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Name of the Google Sheet to read from; can be set via environment variable
SHEET_NAME = os.getenv("SHEET_NAME", "Vendedor360_DataHub")


def _gc():
    """Return an authorized gspread client using a service account JSON."""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "data/service_account.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scopes)
    return gspread.authorize(creds)


def read_sheet(tab_name: str) -> pd.DataFrame:
    """
    Read a worksheet by name from the configured Google Sheet into a Pandas DataFrame.

    Parameters
    ----------
    tab_name : str
        Name of the tab/worksheet to read.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the sheet's data. Empty DataFrame if the sheet is empty.
    """
    gc = _gc()
    sh = gc.open(SHEET_NAME)
    ws = sh.worksheet(tab_name)
    df = get_as_dataframe(ws, evaluate_formulas=True, header=0)
    # Drop completely empty rows
    df = df.dropna(how="all")
    # Clean column names
    df.columns = [str(c).strip() for c in df.columns]
    return df


def kpi_value(df: pd.DataFrame, col: str, agg: str = "sum"):
    """
    Calculate a simple KPI value from a column of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to aggregate over.
    col : str
        The column name to aggregate.
    agg : str, default "sum"
        The aggregation to perform: 'sum', 'count' or 'mean'.

    Returns
    -------
    float or int
        The aggregated value. Returns 0 if column not found or DataFrame empty.
    """
    if df.empty or col not in df.columns:
        return 0
    if agg == "sum":
        return float(pd.to_numeric(df[col], errors="coerce").fillna(0).sum())
    if agg == "count":
        return int(len(df))
    if agg == "mean":
        s = pd.to_numeric(df[col], errors="coerce").dropna()
        return float(s.mean()) if len(s) else 0
    return 0
