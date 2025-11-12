from playwright.sync_api import sync_playwright
from scrap_elements import ScrapElements as s
import re 
import json

URL = "https://www.transfermarkt.fr/kylian-mbappe/leistungsdatendetails/spieler/342229/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/plus/1"

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
        "Âge": s.scrap_age(page),
        "Taille": s.scrap_taille(page) ,
        "Position": s.scrap_position(page)
        }
    browser.close()
    return data

with sync_playwright() as playwright:
    data = run(playwright)


output_file = "output.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
    
    