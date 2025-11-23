from playwright.sync_api import sync_playwright
from scrap_performance_detaillees import ScrapPerformancesDetaillees as s
from scrap_profil import ScrapProfil as sp
from scrap_blessure import ScrapBlessure as sb
from scrap_trophees import ScrapTrophees as st
from Basemodel import JoueurStats 
import re
import json
import time
import random

# --- FONCTIONS DE NAVIGATION (Identiques) ---
def goto_profil_page(page, base_url):
    profil_url = base_url.replace("leistungsdatendetails", "profil")
    page.goto(profil_url, wait_until="domcontentloaded", timeout=60000)

def goto_blessure_page(page, base_url):
    profil_url = base_url.replace("leistungsdatendetails", "verletzungen")
    page.goto(profil_url, wait_until="domcontentloaded", timeout=60000)

def goto_trophees_page(page, base_url):
    profil_url = base_url.replace("leistungsdatendetails", "erfolge")
    page.goto(profil_url, wait_until="domcontentloaded", timeout=60000)

# --- SCRAPING D'UN JOUEUR (Identique) ---
def scraper_un_joueur(page, url_joueur):
    # ... (Ton code scraper_un_joueur reste EXACTEMENT le même ici) ...
    # Pour ne pas surcharger la réponse, je ne le recolle pas, 
    # mais garde ta fonction telle quelle ! 
    
    if "profil" in url_joueur:
        url_stats = url_joueur.replace("profil", "leistungsdatendetails")
        url_stats += "/plus/1"
    else:
        url_stats = url_joueur

    try:
        page.goto(url_stats, wait_until="domcontentloaded", timeout=60000)
        
        # --- RECUPERATION INFORMATIONS PROFIL ---
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
            
            # SAISON 25/26
            "Minutes jouées 25/26": s.scrap_minutes_jouees_25_26(page),
            "Nombre de matchs 25/26": s.scrap_nombre_matchs_25_26(page),
            "Nombre d'entrées en jeu 25/26": s.scrap_entrees_en_jeu_25_26(page),
            "Nombre de titularisations 25/26": s.scrap_titularisations_25_26(page),
            "Nombre de buts 25/26": s.scrap_nombre_buts_25_26(page),
            "Nombre de penaltys 25/26": s.scrap_nombre_penaltys_25_26(page),
            "Nombre de passes décisives 25/26": s.scrap_nombre_passes_d_25_26(page),
            "Nombre clean de sheets 25/26": s.scrap_nombre_clean_sheets_25_26(page),
            "Nombre de buts encaissés 25/26": s.scrap_nombre_buts_encaisses_25_26(page),

            # SAISON 24/25
            "Minutes jouées 24/25": s.scrap_minutes_jouees_24_25(page),
            "Nombre de matchs 24/25": s.scrap_nombre_matchs_24_25(page),
            "Nombre d'entrées en jeu 24/25": s.scrap_entrees_en_jeu_24_25(page),
            "Nombre de titularisations 24/25": s.scrap_titularisations_24_25(page),
            "Nombre de buts 24/25": s.scrap_nombre_buts_24_25(page),
            "Nombre de penaltys 24/25": s.scrap_nombre_penaltys_24_25(page),
            "Nombre de passes décisives 24/25": s.scrap_nombre_passes_d_24_25(page),
            "Nombre clean de sheets 24/25": s.scrap_nombre_clean_sheets_24_25(page),
            "Nombre de buts encaissés 24/25": s.scrap_nombre_buts_encaisses_24_25(page),

            # SAISON 23/24
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
        print(f"❌ Erreur sur {url_joueur}: {e}")
        return None

# --- NOUVELLE FONCTION : SCRAPER UN CLUB ENTIER ---
# Cette fonction ne lance pas de navigateur, elle utilise celui qu'on lui donne (page)
def scraper_club(page, url_club):
    print(f"\n🔵 TRAITEMENT DU CLUB : {url_club}")
    
    page.goto(url_club, wait_until="domcontentloaded", timeout=60000)
    

    # Récupération des liens
    print("   Récupération des joueurs...")
    page.wait_for_selector("td.hauptlink a", timeout=15000)
    liens = page.locator("td.hauptlink a").all()
    urls_joueurs = set()
    
    for lien in liens:
        href = lien.get_attribute("href")
        if href and "/profil/spieler/" in href:
            full_url = "https://www.transfermarkt.fr" + href
            urls_joueurs.add(full_url)
            
    print(f"   {len(urls_joueurs)} joueurs trouvés dans ce club.")

    club_data = []
    
    # Boucle sur les joueurs du club
    for i, url in enumerate(urls_joueurs):
        joueur = scraper_un_joueur(page, url)
        if joueur:
            club_data.append(joueur.model_dump(by_alias=False))
        
        # Pause courte entre les joueurs
        time.sleep(random.uniform(1.5, 3))
        
    return club_data

# --- FONCTION PRINCIPALE : LIGUE 1 ---
def run_ligue_1():
    URL_LIGUE = "https://www.transfermarkt.fr/ligue-1/startseite/wettbewerb/FR1"
    
    data_globale = []
    
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        # On bloque les images pour aller plus vite
        page.route(re.compile(r"(.png|.jpg|.jpeg|.svg|.woff|.css)"), lambda route: route.abort())

        # 1. Récupérer les liens des 18 clubs
        print("🌍 Navigation vers la Ligue 1...")
        page.goto(URL_LIGUE, wait_until="domcontentloaded")
        
        print("📋 Récupération de la liste des clubs...")
        # Le sélecteur pour avoir les liens des clubs dans le tableau du classement
        # On cible td.hauptlink.no-border-links > a
        liens_clubs = page.locator("td.hauptlink.no-border-links a").all()
        
        urls_clubs = set()
        for lien in liens_clubs:
            href = lien.get_attribute("href")
            # On vérifie que c'est bien un lien de club (/startseite/verein/)
            if href and "/startseite/verein/" in href:
                full_url = "https://www.transfermarkt.fr" + href
                urls_clubs.add(full_url)
        
        print(f"✅ {len(urls_clubs)} clubs trouvés. Début du scraping général.")
        print("-" * 40)

        # 2. Boucle sur chaque club
        for index_club, url_club in enumerate(urls_clubs):
            print(f"\n🏟️ CLUB {index_club + 1}/{len(urls_clubs)}")
            
            # On lance le scraping du club
            donnees_club = scraper_club(page, url_club)
            
            # On ajoute les données du club à la liste globale
            data_globale.extend(donnees_club)
            
            # SAUVEGARDE INTERMÉDIAIRE (Sécurité)
            # Comme c'est long, on sauvegarde après chaque club pour ne rien perdre si ça plante
            with open("ligue1_intermediaire.json", "w", encoding="utf-8") as f:
                json.dump(data_globale, f, indent=4, ensure_ascii=False)
            print(f"💾 Données sauvegardées (Total joueurs: {len(data_globale)})")

            # PAUSE LONGUE ENTRE LES CLUBS
            # C'est vital pour ne pas se faire bannir après le 3ème club
            pause = random.uniform(5, 10)
            print(f"💤 Pause changement de club ({int(pause)}s)...")
            time.sleep(pause)

        browser.close()
    
    return data_globale

# --- LANCEMENT ---
if __name__ == "__main__":
    data_finale = run_ligue_1()

    output_file = "ligue1_complet.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data_finale, f, indent=4, ensure_ascii=False)

    print(f"\n🎉 TERMINE ! Données sauvegardées dans {output_file}")