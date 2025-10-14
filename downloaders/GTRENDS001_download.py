"""Fetch Google Trends popularity data using Selenium (undetected-chromedriver).

Overview
- Launches a headful Chrome via undetected-chromedriver (UC).
- Applies basic stealth patches and accepts consent.
- Batches queries (anchor + up to BATCH_SIZE terms) and downloads CSVs.
- On failure or soft-throttling, rotates to a fresh Chrome profile directory automatically
  under: ~/ChromeRemoteProfiles (profile_0, profile_1, ...). No remote debugging required."""

import logging
import subprocess
import time
from datetime import datetime
from itertools import islice
from pathlib import Path
from typing import Iterable, Iterator, List
from urllib.parse import quote

import undetected_chromedriver as uc  # type: ignore
from numpy import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DRIVER_PATH = Path("/opt/homebrew/bin/chromedriver")
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE_ROOT = Path.home() / "ChromeRemoteProfiles"
BASE_PORT = 9222
ROTATE_EVERY = 18  # pages per session before rotating
BATCH_SIZE = 4  # anchor + up to 4 terms => 5 total per request
MAX_RETRIES = 3
ANCHOR_TERM = "google"
REGIONS = {
    "Andalucía": "ES-AN",
    "Aragón": "ES-AR",
    "Asturias": "ES-AS",
    "Islas Baleares": "ES-IB",
    "Canarias": "ES-CN",
    "Cantabria": "ES-CB",
    "Castilla-La Mancha": "ES-CM",
    "Castilla y León": "ES-CL",
    "Cataluña": "ES-CT",
    "Comunidad Valenciana": "ES-VC",
    "Extremadura": "ES-EX",
    "Galicia": "ES-GA",
    "Madrid": "ES-MD",
    "Murcia": "ES-MC",
    "Navarra": "ES-NC",
    "País Vasco": "ES-PV",
    "La Rioja": "ES-RI",
}
PORN_PLATFORMS = [
    "pornhub",
    "xvideos",
    "xhamster",
    "redtube",
    "xnxx",
    "youporn",
    "spankbang",
    "tnaflix",
    "tube8",
    "youjizz",
    "youporn",
    "porndoe",
    "empflix",
    "hclips",
    "xtube",
    "efukt",
    "drtuber",
    "motherless",
    "javhd",
    "porntrex",
    "porngo",
    "sheshaft",
    "beeg",
    "nuvid",
    "fux",
    "hqporner",
    "bellesa",
    "brazzers",
    "bangbros",
    "naughtyamerica",
    "teamSkeet",
    "mofos",
    "realitykings",
    "fakehub",
    "onlyfans porno",
    "onlyfans filtrado",
    "onlyfans leaks",
    "mydirtyhobby",
    "webcams amateur",
    "livejasmin",
    "stripchat",
    "chaturbate",
    "cam4",
    "camsoda",
    "camgirls",
    "pornohub",
    "ponhub",
    "xvidios",
    "pornjizz",
    "xhamter",
    "porno español gratis",
    "pornohub españa",
    "porntube",
    "pornmature",
    "pornhube",
    "porn hab",
    "porhub",
    "pornhub español",
    "pornhub gratis",
]
PORN_SEARCHES = [
    "porno",
    "pornografía",
    "videos porno",
    "porno gratis",
    "ver porno",
    "ver porno gratis",
    "sexo gratis",
    "sexo casero",
    "mujeres desnudas",
    "mujeres follando",
    "videos para adultos",
    "sexo español",
    "porno español",
    "porno casero",
    "porno amateur",
    "maduras follando",
    "maduras calientes",
    "chicas calientes",
    "follando duro",
    "sexo anal",
    "trios sexuales",
    "orgías",
    "lesbianas calientes",
    "lesbianas porno",
    "porno lésbico",
    "colegialas calientes",
    "colegialas follando",
    "putas follando",
    "videos de putas",
    "putas españolas",
    "pajas españolas",
    "videos de pajas",
    "porno gay",
    "porno trans",
    "mamadas",
    "mamadas profundas",
    "sexo oral",
    "culonas calientes",
    "tetonas desnudas",
    "tetas grandes",
    "culonas follando",
    "rubias calientes",
    "brunettes porno",
    "dominación sexual",
    "bdsm español",
    "porno duro",
    "follando en público",
    "videos porno 4k",
    "sexo en directo",
    "porno online",
    "sexo por webcam",
    "ver chicas desnudas",
    "desnudos gratis",
    "mamitas calientes",
    "videos cachondos",
    "gente follando",
    "españolas calientes",
    "latinas desnudas",
    "porno con latinas",
    "videos sexuales gratis",
    "sexo con madrastra",
    "incesto porno",
    "hermanastra porno",
    "madre e hijo porno",
    "porno tabú",
    "esposa infiel porno",
    "videos calientes gratis",
    "páginas de sexo",
    "busco porno",
    "buscar porno gratis",
    "sexo en casa",
]

LOG_DIR = Path("logs") / "download_GTRENDS"
LOG_PATH = LOG_DIR / f"{datetime.now().isoformat()}.log"


def setup_logging() -> None:
    LOG_DIR.mkdir(exist_ok=True, parents=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(LOG_PATH)],
    )


def chunked(iterable: Iterable[str], n: int) -> Iterator[List[str]]:
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            break
        yield batch


def trends_ready(driver: webdriver.Chrome, timeout: int = 20):
    w = WebDriverWait(driver, timeout)
    w.until(lambda d: d.execute_script("return document.readyState") == "complete")  # type: ignore
    w.until(EC.presence_of_element_located((By.CSS_SELECTOR, "trends-widget, .widget")))


def clear_trends_storage(driver: webdriver.Chrome):
    try:
        driver.execute_cdp_cmd("Network.clearBrowserCache", {})  # type: ignore
        driver.execute_cdp_cmd(  # type: ignore
            "Storage.clearDataForOrigin",
            {
                "origin": "https://trends.google.com",
                "storageTypes": "local_storage,session_storage,cache_storage,indexeddb,service_workers",
            },
        )
    except Exception:
        pass


def apply_stealth(driver: webdriver.Chrome):
    try:
        driver.execute_cdp_cmd(  # type: ignore
            "Network.setUserAgentOverride",
            {
                "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",  # noqa: E501
                "platform": "MacIntel",
                "acceptLanguage": "es-ES,es;q=0.9,en;q=0.8",
            },
        )
    except Exception:
        pass

    stealth_js = r"""
Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
Object.defineProperty(navigator, 'languages', {get: () => ['es-ES','es','en-US','en']});
Object.defineProperty(navigator, 'platform', {get: () => 'MacIntel'});
Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4]});
Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
const getParameter = WebGLRenderingContext.prototype.getParameter;
WebGLRenderingContext.prototype.getParameter = function(param){
  if (param === 37445) return 'Intel Inc.';           // UNMASKED_VENDOR_WEBGL
  if (param === 37446) return 'Apple M2';             // UNMASKED_RENDERER_WEBGL
  return getParameter.call(this, param);
};
const originalQuery = window.Notification && Notification.requestPermission;
if (originalQuery) {
  Notification.requestPermission = function() { return Promise.resolve('default'); }
}
const originalPermissions = navigator.permissions && navigator.permissions.query;
if (originalPermissions) {
  navigator.permissions.query = (p) => p && p.name === 'notifications'
    ? Promise.resolve({ state: 'default' })
    : originalPermissions(p);
}
"""
    try:
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": stealth_js})  # type: ignore
    except Exception:
        pass


def establish_session(driver: webdriver.Chrome):
    driver.set_window_size(1368, 820)  # type: ignore
    driver.get("https://www.google.com/?hl=es")
    try:
        btn = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceptar') or contains(., 'Accept')]"))
        )
        btn.click()
        time.sleep(1.2)
    except Exception:
        pass
    driver.get("https://trends.google.com/?hl=es")
    time.sleep(1.5)


def build_explore_url(region_code: str, terms: list[str]) -> str:
    q = ",".join(quote(t) for t in [ANCHOR_TERM] + terms)
    return f"https://trends.google.com/trends/explore?date=all,all&geo=ES,{region_code}&q={q}&hl=es"


def apply_emulation(driver: webdriver.Chrome):
    """Set stable, human-like emulation via CDP before navigation."""
    try:
        driver.execute_cdp_cmd("Emulation.setTimezoneOverride", {"timezoneId": "Europe/Madrid"})  # type: ignore
    except Exception:
        pass
    try:
        driver.execute_cdp_cmd("Emulation.setLocaleOverride", {"locale": "es-ES"})  # type: ignore
    except Exception:
        pass
    try:
        driver.execute_cdp_cmd(  # type: ignore
            "Emulation.setGeolocationOverride",
            {
                "latitude": 40.4168,
                "longitude": -3.7038,
                "accuracy": 30,
            },
        )
    except Exception:
        pass
    # UA + Client Hints metadata (helps align Sec-CH-UA with UA)
    try:
        driver.execute_cdp_cmd(  # type: ignore
            "Network.setUserAgentOverride",
            {
                "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "platform": "MacIntel",
                "acceptLanguage": "es-ES,es;q=0.9,en;q=0.8",
                "userAgentMetadata": {
                    "brands": [
                        {"brand": "Chromium", "version": "120"},
                        {"brand": "Google Chrome", "version": "120"},
                        {"brand": "Not:A-Brand", "version": "99"},
                    ],
                    "fullVersion": "120.0.0.0",
                    "platform": "macOS",
                    "platformVersion": "15.6.1",
                    "architecture": "arm",
                    "model": "",
                    "mobile": False,
                },
            },
        )
    except Exception:
        pass


def new_driver_for_profile(profile_dir: Path) -> webdriver.Chrome:
    profile_dir.mkdir(parents=True, exist_ok=True)

    # undetected-chromedriver options
    uopts = uc.ChromeOptions()
    uopts.add_argument(f"--user-data-dir={str(profile_dir)}")
    uopts.add_argument("--profile-directory=Default")
    uopts.add_argument("--no-first-run")
    uopts.add_argument("--no-default-browser-check")
    uopts.add_argument("--disable-features=BlockThirdPartyCookies")
    uopts.add_argument("--lang=es-ES,es")
    uopts.add_argument("--start-maximized")
    # Do NOT add AutomationControlled flag

    # Optional: preferences (downloads, etc.)
    # uopts.add_experimental_option("prefs", {"download.prompt_for_download": False})

    # Start UC (no Service/DRIVER_PATH needed)
    drv = uc.Chrome(options=uopts, headless=False)

    # Bring Chrome to foreground (macOS)
    try:
        subprocess.run(["osascript", "-e", 'tell application "Google Chrome" to activate'], check=False)
    except Exception:
        pass

    # Apply stealth and warm-up
    apply_emulation(drv)
    apply_stealth(drv)
    establish_session(drv)
    return drv


def click_export(driver: webdriver.Chrome) -> bool:
    locators = [
        "//button[contains(@class,'widget-actions-item') and contains(@class,'export')]",
        "//button[@title='CSV' or contains(@aria-label,'CSV')]",
        "//div[contains(@class,'widget-actions')]//button[contains(@aria-label,'CSV')]",
    ]
    for xp in locators:
        btns = driver.find_elements(By.XPATH, xp)
        if btns:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(btns[0])).click()
            return True
    return False


def main():
    setup_logging()
    PROFILE_ROOT.mkdir(exist_ok=True, parents=True)

    profile_idx = 325
    driver = new_driver_for_profile(PROFILE_ROOT / f"profile_{profile_idx}")
    WebDriverWait(driver, 15)

    try:
        all_terms = PORN_SEARCHES + PORN_PLATFORMS  # ...existing code...
        for region_name, region_code in REGIONS.items():
            for terms_batch in chunked(all_terms, BATCH_SIZE):
                url = build_explore_url(region_code, terms_batch)
                attempt = 0
                success = False

                while attempt < MAX_RETRIES and not success:
                    attempt += 1
                    logging.info(f"Exploring [{region_name}] terms={terms_batch} (attempt {attempt}/{MAX_RETRIES})")

                    try:
                        driver.get(url)
                        time.sleep(random.uniform(1.8, 3.2))  # type: ignore
                        trends_ready(driver, timeout=25)

                        if not click_export(driver):
                            # Soft degradation; try clearing storage once within same profile
                            clear_trends_storage(driver)
                            time.sleep(1.5)
                            driver.get(url)
                            trends_ready(driver, timeout=25)
                            if not click_export(driver):
                                raise RuntimeError("Export button not found")

                        logging.info(f"✅ Exported: {region_name} | {terms_batch}")
                        time.sleep(random.uniform(2.8, 5.2))  # type: ignore
                        success = True

                    except Exception as e:
                        logging.warning(f"⚠️ Failed on profile_{profile_idx}: {type(e).__name__}: {e}")
                        # Rotate profile immediately on failure
                        try:
                            driver.quit()
                        except Exception:
                            pass
                        profile_idx += 1
                        driver = new_driver_for_profile(PROFILE_ROOT / f"profile_{profile_idx}")
                        WebDriverWait(driver, 15)
                        time.sleep(random.uniform(3.0, 6.0))  # type: ignore

                if not success:
                    logging.error(
                        f"❌ Skipping batch after {MAX_RETRIES} profile rotations: {region_name} | {terms_batch}"
                    )

    finally:
        try:
            driver.quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
