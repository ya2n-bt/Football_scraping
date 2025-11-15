from playwright.sync_api import sync_playwright
from scrap_elements import ScrapElements as s
import re 
import json

URL = "https://www.transfermarkt.fr/kylian-mbappe/nationalmannschaft/spieler/342229/verein_id/3377/hauptwettbewerb//wettbewerb_id//start/2017-03-25/ende/2025-11-15/nurEinsatz/0/plus/1"

def run(playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.route(
        re.compile(r"(.png|.jpg|.jpeg|.svg|.woff|.css)"), 
        lambda route: route.abort()
    )
    page.route(
        re.compile(r"(google-analytics.com|googletagmanager.com)"), 
        lambda route: route.abort()
    )
    page.goto(URL, wait_until="load")
    data: dict = {
        "Nom": s.scrap_nom(page),
        "Nationalité": s.scrap_nationalite(page),
        "Club": s.scrap_club(page),
        "Âge": s.scrap_age(page),
        "Taille": s.scrap_taille(page) ,
        "Position": s.scrap_position(page),
        "Valeur": s.scrap_valeur(page),
        "Minutes jouées 24/25": s.scrap_minutes_jouees_24_25(page),
        "Nombre de matchs 24/25": s.scrap_nombre_matchs_24_25(page),
        "Nombre de buts 24/25": s.scrap_nombre_buts_24_25(page),
        "Nombre de penaltys 24/25": s.scrap_nombre_penaltys_24_25(page),
        "Nombre de passes décisives 24/25": s.scrap_nombre_passes_d_24_25(page),
        "Nombre clean de sheets 24/25": s.scrap_nombre_clean_sheets_24_25(page),
        "Nombre de buts encaissés 24/25": s.scrap_nombre_buts_encaisses_24_25(page),
        }
    
    browser.close()
    return data

with sync_playwright() as playwright:
    data = run(playwright)

output_file = "output.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)