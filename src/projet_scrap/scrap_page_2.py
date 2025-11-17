from playwright.sync_api import sync_playwright
from scrap_performance_detaillees import ScrapPerformancesDetaillees as s
from scrap_profil import ScrapProfil as sp
import re 
import json

URL = "https://www.transfermarkt.fr/kylian-mbappe/leistungsdatendetails/spieler/342229/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/plus/1"

def goto_profil_page(page, base_url):
    profil_url = base_url.replace("leistungsdatendetails", "profil")
    page.goto(profil_url, wait_until="load")
    return profil_url

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
        "Fin de contrat dans": s.scrap_fin_contrat(page),
        "Valeur": s.scrap_valeur(page),
        "Nombre de sélections internationales": s.scrap_nombre_selections_internationales(page),

        # --- STATS 25/26 ---

        "Minutes jouées 25/26": s.scrap_minutes_jouees_25_26(page),
        "Nombre de matchs 25/26": s.scrap_nombre_matchs_25_26(page),
        "Nombre d'entrées en jeu 25/26": s.scrap_entrees_en_jeu_25_26(page),
        "Nombre de titularisations 25/26": s.scrap_titularisations_25_26(page),
        "Nombre de buts 25/26": s.scrap_nombre_buts_25_26(page),
        "Nombre de penaltys 25/26": s.scrap_nombre_penaltys_25_26(page),
        "Nombre de passes décisives 25/26": s.scrap_nombre_passes_d_25_26(page),
        "Nombre clean de sheets 25/26": s.scrap_nombre_clean_sheets_25_26(page),
        "Nombre de buts encaissés 25/26": s.scrap_nombre_buts_encaisses_25_26(page),

        # --- STATS 24/25 ---

        "Minutes jouées 24/25": s.scrap_minutes_jouees_24_25(page),
        "Nombre de matchs 24/25": s.scrap_nombre_matchs_24_25(page),
        "Nombre d'entrées en jeu 24/25": s.scrap_entrees_en_jeu_24_25(page),
        "Nombre de titularisations 24/25": s.scrap_titularisations_24_25(page),
        "Nombre de buts 24/25": s.scrap_nombre_buts_24_25(page),
        "Nombre de penaltys 24/25": s.scrap_nombre_penaltys_24_25(page),
        "Nombre de passes décisives 24/25": s.scrap_nombre_passes_d_24_25(page),
        "Nombre clean de sheets 24/25": s.scrap_nombre_clean_sheets_24_25(page),
        "Nombre de buts encaissés 24/25": s.scrap_nombre_buts_encaisses_24_25(page),

        # --- STATS 23/24 ---
        "Minutes jouées 23/24": s.scrap_minutes_jouees_23_24(page),
        "Nombre de matchs 23/24": s.scrap_nombre_matchs_23_24(page),
        "Nombre d'entrées en jeu 23/24": s.scrap_entrees_en_jeu_23_24(page),
        "Nombre de titularisations 23/24": s.scrap_titularisations_23_24(page),
        "Nombre de buts 23/24": s.scrap_nombre_buts_23_24(page),
        "Nombre de penaltys 23/24": s.scrap_nombre_penaltys_23_24(page),
        "Nombre de passes décisives 23/24": s.scrap_nombre_passes_d_23_24(page),
        "Nombre clean de sheets 23/24": s.scrap_nombre_clean_sheets_23_24(page),
        "Nombre de buts encaissés 23/24": s.scrap_nombre_buts_encaisses_23_24(page),
        }
    
    goto_profil_page(page, URL)

    data.update({
        "Pied fort": sp.scrap_pied_fort(page)
    })

    browser.close()
    return data

with sync_playwright() as playwright:
    data = run(playwright)

output_file = "info_joueur_2.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)