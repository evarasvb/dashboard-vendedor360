import os, csv, json, asyncio, datetime
from pathlib import Path
from dotenv import load_dotenv
from playwright.async_api import async_playwright


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_CSV = BASE_DIR / "DataHub_Licitaciones.csv"
ART = BASE_DIR / "artifacts" / "lici"
SEL_PATH = Path(__file__).with_name("selectors.json")


CSV_HEADER = [
    "datetime","portal","keyword","title","link","status","apply_result","internal_id"
]


def append_csv(row: dict) -> None:
    DATA_CSV.parent.mkdir(parents=True, exist_ok=True)
    new_file = not DATA_CSV.exists()
    with open(DATA_CSV, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        if new_file:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in CSV_HEADER})


async def ensure_dirs():
    ART.mkdir(parents=True, exist_ok=True)


load_dotenv()
LICI_URL = os.getenv("LICI_URL", "https://lici.example.com/login")
LICI_USER = os.getenv("LICI_USER", "")
LICI_PASS = os.getenv("LICI_PASS", "")
APPLY = os.getenv("APPLY", "0") == "1"
KEYWORDS = [kw.strip() for kw in os.getenv("LICI_KEYWORDS", "").split(",") if kw.strip()]


async def run_kw(page, kw: str):
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    art_dir = ART / ts
    art_dir.mkdir(exist_ok=True)


    selectors = json.loads(SEL_PATH.read_text(encoding="utf-8"))
    s_login = selectors["login"]
    s_search = selectors["search"]


    await page.goto(s_login.get("url", LICI_URL), wait_until="load")
    await page.fill(s_login["user"], LICI_USER)
    await page.fill(s_login["pass"], LICI_PASS)
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
                    # si existe un id interno visible tras postular, léelo:
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


        append_csv({
            "datetime": datetime.datetime.now().isoformat(),
            "portal": "LICI",
            "keyword": kw,
            "title": (title or "").strip(),
            "link": link or "",
            "status": "POSTULADA" if (APPLY and apply_result=="OK") else "ENCONTRADA",
            "apply_result": apply_result,
            "internal_id": internal_id,
        })


async def main():
    await ensure_dirs()
    if not LICI_USER or not LICI_PASS:
        raise SystemExit("Faltan LICI_USER/LICI_PASS en .env")


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

