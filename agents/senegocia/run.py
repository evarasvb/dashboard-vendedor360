import os
import csv
import json
import asyncio
import datetime
import pathlib

from dotenv import load_dotenv
from playwright.async_api import async_playwright, Page


load_dotenv()


ROOT_DIR = pathlib.Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
ART = DATA_DIR / "artifacts" / "senegocia"
OUT_DIR = DATA_DIR / "out"
SEL_PATH = pathlib.Path(__file__).resolve().parent / "selectors.json"


CSV_FILE = OUT_DIR / "licitaciones.csv"
CSV_HEADER = [
    "datetime",
    "portal",
    "keyword",
    "title",
    "link",
    "status",
    "apply_result",
    "internal_id",
]


URL = os.getenv("SENEGOCIA_URL", "https://senegocia.example.com/login")
USER = os.getenv("SENEGOCIA_USER", "")
PASS = os.getenv("SENEGOCIA_PASS", "")
APPLY = os.getenv("APPLY", "0") == "1"
KEYWORDS = [
    kw.strip() for kw in os.getenv("SENEGOCIA_KEYWORDS", "").split(",") if kw.strip()
]


async def ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)


def append_csv(row: dict) -> None:
    new = not CSV_FILE.exists()
    with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEADER)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in CSV_HEADER})


async def run_kw(page: Page, kw: str) -> None:
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    art_dir = ART / ts
    art_dir.mkdir(exist_ok=True)

    selectors = json.loads(SEL_PATH.read_text(encoding="utf-8"))
    s_login = selectors["login"]
    s_search = selectors["search"]

    await page.goto(s_login.get("url", URL), wait_until="load")
    await page.fill(s_login["user"], USER)
    await page.fill(s_login["pass"], PASS)
    await page.click(s_login["submit"])
    await page.wait_for_load_state("networkidle")

    await page.fill(s_search["box"], kw)
    await page.press(s_search["box"], "Enter")
    await page.wait_for_load_state("networkidle")

    rows = await page.locator(s_search["row"]).all()
    for idx, r in enumerate(rows, start=1):
        try:
            title = await r.locator(s_search["title"]).inner_text()
            link = await r.locator(s_search["link"]).first.get_attribute("href")
        except Exception:
            title, link = "", ""

        apply_result = "SKIPPED"
        internal_id = ""
        if APPLY:
            try:
                btn = r.locator(s_search["apply"])
                if await btn.count() > 0:
                    await btn.first.click()
                    await page.wait_for_load_state("networkidle")
                    apply_result = "OK"
                    try:
                        internal_id_sel = s_search.get("apply_result_id")
                        if internal_id_sel:
                            internal_id = await page.locator(internal_id_sel).inner_text()
                    except Exception:
                        internal_id = ""
                else:
                    apply_result = "NO_BUTTON"
            except Exception as e:
                apply_result = f"ERR:{type(e).__name__}"

        shot = art_dir / f"{kw}_{idx}.png"
        try:
            await r.screenshot(path=str(shot))
        except Exception:
            pass

        append_csv(
            {
                "datetime": datetime.datetime.now().isoformat(),
                "portal": "SENEGOCIA",
                "keyword": kw,
                "title": title.strip(),
                "link": link or "",
                "status": "POSTULADA" if (APPLY and apply_result == "OK") else "ENCONTRADA",
                "apply_result": apply_result,
                "internal_id": internal_id,
            }
        )


async def main() -> None:
    await ensure_dirs()
    if not USER or not PASS:
        raise SystemExit("Faltan SENEGOCIA_USER/SENEGOCIA_PASS en .env")

    if not KEYWORDS:
        raise SystemExit("SENEGOCIA_KEYWORDS vacío. Configure palabras clave en .env")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context()
        page = await ctx.new_page()
        try:
            for kw in KEYWORDS:
                await run_kw(page, kw)
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())

