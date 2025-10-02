"""Download CIS general survey data by automating the public website."""

import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()
DRIVER_PATH = Path("/opt/homebrew/bin/chromedriver")
URL = "https://www.cis.es/catalogo-estudios/resultados-definidos/barometros"
CIS_EMAIL = os.getenv("CIS_EMAIL")


LOG_DIR = Path("logs") / "download_CIS"
LOG_PATH = LOG_DIR / f"{datetime.now().isoformat()}.log"
DOWNLOAD_DATA = True  # Set to False to only map variables without downloading data


def setup_logging() -> None:
    """Configure root logger to log to stdout and file."""
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH),
        ],
    )


def main():
    setup_logging()

    if CIS_EMAIL is None:
        logging.error("CIS_EMAIL environment variable is not set.")
        raise ValueError("CIS_EMAIL environment variable is not set.")

    # Selenium Config
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    service = Service(str(DRIVER_PATH))
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 15)

    try:
        driver.get(URL)

        # Accept cookies
        try:
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cn-ok"))).click()
            print("🍪 Cookies accepted")
        except Exception:
            print("ℹ️ No cookie banner found")

        # Load table
        wait.until(EC.presence_of_element_located((By.ID, "tablaEstudios")))
        estudio_urls = []

        while True:
            print("🔄 Processing page...")
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table#tablaEstudios tbody tr")))
            rows = driver.find_elements(By.CSS_SELECTOR, "table#tablaEstudios tbody tr")

            for row in rows:
                id_estudio = row.get_attribute("id")  # type: ignore
                tds = []
                if id_estudio:
                    tds = row.find_elements(By.TAG_NAME, "td")  # type: ignore
                if len(tds) >= 2:
                    fecha = tds[0].text.strip()  # type: ignore
                    codigo = tds[1].text.strip()  # type: ignore
                else:
                    fecha = codigo = ""  # type: ignore
                url_estudio = f"https://www.cis.es/es/detalle-ficha-estudio?idEstudio={id_estudio}"
                estudio_urls.append((url_estudio, fecha, codigo))  # type: ignore

            try:
                next_btn = driver.find_element(By.ID, "tablaEstudios_next")
                if "disabled" in next_btn.get_attribute("class"):  # type: ignore
                    print("✅ Last page reached")
                    break
                else:
                    next_btn.click()
                    time.sleep(0.1)
            except Exception as e:
                print(f"❌ Not able to check next page: {e}")
                logging.error(f"Not able to check next page: {e}")
                break

        print(f"\n🔗 Total number of studies found: {len(estudio_urls)}")  # type: ignore

        # Visit each study link
        all_var_mappings = {}
        no_data_zip_studies = []
        error_studies = []
        successful_downloads = 0
        missing_vars_summary = ""
        for idx, (url, fecha, codigo) in enumerate(estudio_urls):  # type: ignore
            try:
                print(f"\n➡️ Accessing {idx + 1}/{len(estudio_urls)}: {url}")  # type: ignore
                driver.get(url)  # type: ignore

                # Terms to search for each variable
                variables = {
                    "comunidad_autonoma": ["comunidad autónoma"],
                    "provincia": ["provincia"],
                    "edad": ["edad de la persona entrevistada", "edad del entrevistado", "edad"],
                    "sexo": ["sexo de la persona entrevistada", "sexo del entrevistado", "sexo"],
                    "religiosidad": ["religiosidad de la persona entrevistada", "religiosidad"],
                    "ideologia": [
                        "escala de autoubicación ideológica",
                        "escala de ideología del entrevistado",
                        "autoubicación ideológica",
                        "ideología",
                    ],
                    "problemas_generales": [
                        "problemas principales que existen actualmente en españa",
                        "problemas más importantes en españa",
                        "problemas españa",
                    ],
                    "problemas_personales": [
                        "problemas sociales que personalmente afectan mas",
                        "problema social que afecta más personalmente",
                        "problemas afecta",
                    ],
                }

                # Access variable search form and get variable mappings
                try:
                    consulta_variables_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Consulta de Variables')]"))
                    )
                    consulta_variables_button.click()
                    buscador_variables_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Buscador de variables')]"))
                    )
                    buscador_variables_button.click()
                    titulo_input = wait.until(
                        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Título']"))
                    )

                    # Focus screen for easier debugging
                    # driver.execute_script(  # type: ignore
                    #     "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", titulo_input
                    # )
                    # driver.execute_script("arguments[0].focus();", titulo_input)  # type: ignore

                    var_map = {}
                    var_map["fecha"] = fecha
                    var_map["codigo"] = codigo
                    for var, search_terms in variables.items():
                        for term in search_terms:
                            try:
                                titulo_input.clear()
                                titulo_input.send_keys(term)
                                time.sleep(0.1)
                                first_left_cell = driver.find_element(
                                    By.XPATH, "(//tr[contains(@class, 'odd') or contains(@class, 'even')]/td[1])[1]"
                                )
                                first_left_link = first_left_cell.find_element(By.TAG_NAME, "a")  # type: ignore
                                first_left_text = first_left_link.text
                                var_map[var] = first_left_text
                                break
                            except NoSuchElementException:
                                continue

                    all_var_mappings[url] = var_map
                    if len(var_map) - 2 == len(variables):  # type: ignore
                        print("✅ All variables found")
                    else:
                        missing_vars = set(variables.keys()) - set(var_map.keys())  # type: ignore
                        missing_vars_summary += f"{fecha}\t{codigo}\t{url}:\t {list(missing_vars)}\n"
                        print(f"❓ Some variables not found: {list(missing_vars)}")  # type: ignore

                except (NoSuchElementException, ElementNotInteractableException):
                    print("⚠️ No variable mapping available for this study")
                    logging.warning(f"No variable mapping available for {url}")
                except Exception as e:
                    print("⚠️ Unexpected error during variable mapping")
                    logging.warning(f"Unexpected error during variable mapping for {url}: {e}")

                # Download data zip file if available and if DOWNLOAD_DATA is set to True
                if DOWNLOAD_DATA:
                    try:
                        data_zip_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Fichero datos')]")
                        wait.until(EC.element_to_be_clickable(data_zip_link))
                        print("📥 Data zip file available. Opening form...")
                        driver.execute_script("arguments[0].click();", data_zip_link)  # type: ignore
                    except NoSuchElementException:
                        no_data_zip_studies.append(codigo)  # type: ignore
                        print("⚠️ No data zip file available for this study")
                        logging.warning(f"No data zip file available for {url}")
                        continue

                    if len(driver.window_handles) > 1:
                        driver.switch_to.window(driver.window_handles[-1])

                    wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//label[contains(., 'Email') and not(contains(., 'Confirmar'))]")
                        )
                    )
                    time.sleep(1)

                    # Fill and submit form
                    label_email = driver.find_element(
                        By.XPATH, "//label[contains(., 'Email') and not(contains(., 'Confirmar'))]"
                    )
                    input_email = driver.find_element(By.ID, label_email.get_attribute("for"))  # type: ignore
                    input_email.clear()
                    input_email.send_keys(CIS_EMAIL)

                    label_confirm = driver.find_element(By.XPATH, "//label[contains(., 'Confirmar Email')]")
                    input_confirm = driver.find_element(By.ID, label_confirm.get_attribute("for"))  # type: ignore
                    input_confirm.clear()
                    input_confirm.send_keys(CIS_EMAIL)

                    try:
                        checkbox = driver.find_element(
                            By.XPATH, "//label[contains(., 'acepta')]/input[@type='checkbox']"
                        )
                        checkbox.click()
                    except NoSuchElementException:
                        try:
                            checkbox = driver.find_element(
                                By.XPATH, "//input[@type='checkbox' and contains(@name, 'Checkbox')]"
                            )
                            checkbox.click()
                        except Exception:
                            print("❌ Checkbox not found")
                            logging.error(f"Checkbox not found for {url}")
                            continue

                    submit_btn = driver.find_element(By.ID, "ddm-form-submit")
                    submit_btn.click()

                    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Descargar')]")))
                    download_btn = driver.find_element(By.XPATH, "//a[contains(text(),'Descargar')]")
                    print(f"⬇️ Downloading from: {download_btn.get_attribute('href')}")  # type: ignore
                    driver.execute_script("arguments[0].click();", download_btn)  # type: ignore
                    logging.info(f"Downloaded data for {url}")
                    successful_downloads += 1

                    if len(driver.window_handles) > 1:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                error_studies.append(codigo)  # type: ignore
                print(f"❌ Error processing {url}: {e}")
                logging.error(f"Error processing {url}: {e}")

        # Save variable mappings
        with open("data/debug/CIS_variable_mappings.json", "w", encoding="utf-8") as f:
            json.dump(all_var_mappings, f, ensure_ascii=False, indent=4)
        with open("data/debug/missing_vars.txt", "w", encoding="utf-8") as f:
            f.write(missing_vars_summary)  # type: ignore

        # Summary
        summary = (
            "\n📋 Summary:\n"
            f"Number of listed studies: {len(estudio_urls)}\n"  # type: ignore
            f"Number of successful data downloads: {successful_downloads}\n"  # type: ignore
            f"Number of successful variable mappings: {len(all_var_mappings)}\n"  # type: ignore
            f"Number of studies with no data zip found: {len(no_data_zip_studies)}\n"  # type: ignore
            f"Number of studies with errors: {len(error_studies)}\n"  # type: ignore
            f"Studies with no data zip: {no_data_zip_studies}\n"  # type: ignore
            f"Studies with errors: {error_studies}\n"  # type: ignore
        )
        print(summary)
        logging.info(summary)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
