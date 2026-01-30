from playwright.sync_api import sync_playwright
from projet_scrap.scrap_performance_detaillees import ScrapPerformancesDetaillees as s
from projet_scrap.scrap_profil import ScrapProfil as sp
from projet_scrap.scrap_blessure import ScrapBlessure as sb
from projet_scrap.scrap_trophees import ScrapTrophees as st
from projet_scrap.basemodel import JoueurStats 
import re
import json
import time
import random

def goto_profil_page(page, base_url):
    profil_url = base_url.replace("leistungsdatendetails", "profil")
    page.goto(profil_url, wait_until="domcontentloaded", timeout=60000)

def goto_blessure_page(page, base_url):
    profil_url = base_url.replace("leistungsdatendetails", "verletzungen")
    page.goto(profil_url, wait_until="domcontentloaded", timeout=60000)

def goto_trophees_page(page, base_url):
    profil_url = base_url.replace("leistungsdatendetails", "erfolge")
    page.goto(profil_url, wait_until="domcontentloaded", timeout=60000)

def scraper_un_joueur(page, url_joueur):
    print(f"Scraping de : {url_joueur}")
    
    if "profil" in url_joueur:
        url_stats = url_joueur.replace("profil", "leistungsdatendetails")
        url_stats += "/plus/1"
    else:
        url_stats = url_joueur

    try:
        page.goto(url_stats, wait_until="domcontentloaded", timeout=60000)
        
        raw_data = {
            "Nom": s.scrap_nom(page),
            "Nationalité": s.scrap_nationalite(page),
            "Ligue": s.scrap_ligue(page),
            "Club": s.scrap_club(page),
            "Âge": s.scrap_age(page),
            "Taille": s.scrap_taille(page),
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

        goto_profil_page(page, url_stats)
        raw_data["Pied fort"] = sp.scrap_pied_fort(page)

        goto_blessure_page(page, url_stats)
        raw_data.update({
            "Nombre de blessures sur les 3 dernières saisons": sb.scrap_nombre_blessures(page),
            "Nombre de matchs manqués sur les 3 dernières saisons": sb.scrap_matchs_manques(page),
            "Nombre de jours sous blessures": sb.scrap_jours_blessures(page)
        })

        goto_trophees_page(page, url_stats)
        raw_data["Nombre de trophées sur les 3 dernières saisons"] = st.scrap_nombre_trophees(page)

        return JoueurStats(**raw_data)

    except Exception as e:
        print(f"Erreur sur {url_joueur}: {e}")
        return None


def run_equipe():    
    URL_CLUB = "https://www.transfermarkt.fr/paris-saint-germain/startseite/verein/583"
    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context() 
        page = context.new_page()
        page.route(re.compile(r"(.png|.jpg|.jpeg|.svg|.woff|.css)"), lambda route: route.abort())
        
        print(f"Navigation directe vers {URL_CLUB}...")
        page.goto(URL_CLUB, wait_until="domcontentloaded", timeout=60000)

        print("Récupération des URLs des joueurs...")
        page.wait_for_selector("td.hauptlink a", timeout=10000)
        
        liens = page.locator("td.hauptlink a").all()
        urls_joueurs = set()
        
        for lien in liens:
            href = lien.get_attribute("href")
            if href and "/profil/spieler/" in href:
                full_url = "https://www.transfermarkt.fr" + href
                urls_joueurs.add(full_url)
        
        print(f"{len(urls_joueurs)} joueurs trouvés.")

        equipe_data = []
        nb_succes = 0
        nb_erreurs = 0
        erreurs_logs = [] 

        for i, url in enumerate(urls_joueurs):
            print(f"[{i+1}/{len(urls_joueurs)}] Traitement en cours...")
            
            joueur = scraper_un_joueur(page, url)
            
            if joueur:
                equipe_data.append(joueur.model_dump(by_alias=False))
                nb_succes += 1
            else:
                nb_erreurs += 1
                erreurs_logs.append(url)
            
            time.sleep(random.uniform(2, 4)) 

        browser.close()
        
        # --- BILAN FINAL ---
        print(f"Scraping terminé : ")
        print(f"Succès : {nb_succes}")
        print(f"Erreurs : {nb_erreurs}")
        if erreurs_logs:
            print("Joueurs échoués :")
            for err_url in erreurs_logs:
                print(f" - {err_url}")

        return equipe_data

data_finale = run_equipe()

output_file = "psg_complet.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data_finale, f, indent=4, ensure_ascii=False)

print(f"Données sauvegardées dans {output_file}")