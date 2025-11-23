import re
import regex
import locale
locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
from playwright.sync_api import Page
from datetime import datetime

class ScrapPerformancesDetaillees:
    @staticmethod
    def scrap_nom(page: Page) -> str:
        page.wait_for_selector(".data-header__headline-wrapper", timeout=5000)
        nom_joueur = page.locator(".data-header__headline-wrapper").inner_text().strip()
        nom_joueur_filtre = regex.sub(r"[^\p{L}\s]", "", nom_joueur).strip()
        if nom_joueur_filtre is not None:
            return nom_joueur_filtre
        else:
            return "Nom non trouvé"
        
    @staticmethod
    def scrap_nationalite(page: Page) -> str:
        page.wait_for_selector("span[itemprop='nationality'].data-header__content", timeout=5000)
        nationalite_joueur = page.locator("span[itemprop='nationality'].data-header__content").inner_text().strip()
        if nationalite_joueur is not None:
            return nationalite_joueur
        else:
            "Nationalité non trouvée"

    @staticmethod
    def scrap_ligue(page: Page) -> str | None:
        ligue_locator = page.locator(".data-header__league-link")
        if ligue_locator.is_visible(timeout=1000):
            return ligue_locator.inner_text().strip()
        
        return "Ligue non trouvée"
        
    @staticmethod
    def scrap_club(page: Page) -> str:
        page.wait_for_selector(".data-header__club", timeout=5000)
        club_joueur = page.locator(".data-header__club").inner_text().strip()
        if club_joueur is not None:
            return club_joueur
        else:
            return "Club non trouvé"
        
    @staticmethod
    def scrap_age(page: Page) -> tuple[int, str]:
        page.wait_for_selector("span[itemprop='birthDate'].data-header__content", timeout=5000)
        age_joueur = page.locator("span[itemprop='birthDate'].data-header__content").inner_text().strip()
        age_joueur_filtre = re.search(r'\((.*?)\)', age_joueur)
        if age_joueur_filtre is not None:
            return int(age_joueur_filtre.group(1).strip())
        else:
            return "Âge non trouvé"
        
    @staticmethod
    def scrap_taille(page: Page) -> tuple[float, str]:
        selector = "span[itemprop='height'].data-header__content"
        if page.locator(selector).first.is_visible(timeout=500):
            try:
                taille_joueur = page.locator(selector).first.inner_text().strip()
                taille_clean = taille_joueur.replace("m", "").replace(",", ".").strip()
                return float(taille_clean)
            except ValueError:
                return "Taille non trouvé"
        else:   
            return "Taille non trouvé"
        
    @staticmethod
    def scrap_position(page: Page) -> str:
        page.wait_for_selector("li.data-header__label:has-text('Position:') > span.data-header__content", timeout=5000)
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()
        if position_joueur is not None:
            return position_joueur
        else:
            return "Position non trouvé"

    @staticmethod
    def scrap_fin_contrat(page: Page) -> tuple[int, str]:
        repere = page.get_by_text("Contrat jusqu'à:")
        fin_de_contrat = repere.locator("span.data-header__content").inner_text().strip()
        
        if fin_de_contrat:
            try:
                date_fin = datetime.strptime(fin_de_contrat, "%d %B %Y").date()
                
                date_actuelle = datetime.today().date()
                jours_restants = (date_fin - date_actuelle).days
                
                return jours_restants
            except ValueError:
                return "Format de date invalide"
        else:
            return "Fin de contrat non trouvée"

    @staticmethod
    def scrap_valeur(page: Page) -> float | str | None:
        selecteur_valeur = "a.data-header__market-value-wrapper"
        if page.locator(selecteur_valeur).is_visible(timeout=500):
            try:
                texte_complet = page.locator(selecteur_valeur).inner_text()
                valeur_brute = texte_complet.split()[0].strip().replace(',', '.')
                
                unite_locator = page.locator(f"{selecteur_valeur} span.waehrung")
                if unite_locator.is_visible():
                    unite = unite_locator.inner_text().strip()
                else:
                    unite = texte_complet 
                
                if "mio." in unite or "m" in unite.lower(): 
                    multiplicateur = 1_000_000
                elif "k" in unite.lower(): 
                    multiplicateur = 1_000
                else:
                    multiplicateur = 1 
                
                valeur = float(valeur_brute) * multiplicateur
                return valeur

            except (ValueError, IndexError):
                return "Valeur non trouvée"
            
        return "Valeur non trouvée" 
        
    @staticmethod
    def scrap_nombre_selections_internationales(page: Page) -> int | str | None:
        selecteur = "li.data-header__label:has-text('Sélections internationales/buts:') a.data-header__content--highlight"

        if page.locator(selecteur).first.is_visible(timeout=500):
            try:
                text_selections = page.locator(selecteur).first.inner_text().strip()
                return int(text_selections)
            except ValueError:
                return 0
                
        return 0

# --- STATS 25/26 ---


    @staticmethod
    def scrap_nombre_matchs_25_26(page: Page) -> int:
        selector = "tr:has(td.zentriert:has-text('25/26'))"
        lignes = page.locator(selector)
        if lignes.count() == 0:
            return 0  
        
        total_matchs = 0 
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator("td:nth-of-type(6)")
            if cellules.count() > 0: 
                try:
                    nombre_matchs = int(cellules.first.inner_text().strip())
                    total_matchs += nombre_matchs
                except ValueError:
                    continue 
        
        return total_matchs

    @staticmethod
    def scrap_entrees_en_jeu_25_26(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()

        if position_joueur == "Gardien de but":
            td_selector = "td:nth-of-type(10)"
        else:
            td_selector = "td:nth-of-type(11)"
        
        selector = "tr:has(td.zentriert:has-text('25/26'))"
        lignes = page.locator(selector)
        if lignes.count() == 0:
            return 0  
        
        total_entrees_jeu = 0
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator(td_selector)
            if cellules.count() > 0: 
                try:
                    nombre_entrees_jeu = int(cellules.first.inner_text().strip())
                    total_entrees_jeu += nombre_entrees_jeu
                except ValueError:
                    continue 
        
        return total_entrees_jeu
    
    @staticmethod
    def scrap_titularisations_25_26(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()
        
        if position_joueur == "Gardien de but":
            td_selector_entrees = "td:nth-of-type(10)"
        else:
            td_selector_entrees = "td:nth-of-type(11)"
        
        selector = "tr:has(td.zentriert:has-text('25/26'))"
        lignes = page.locator(selector)
        if lignes.count() == 0:
            return 0  
        
        total_entrees_jeu = 0
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator(td_selector_entrees)
            if cellules.count() > 0: 
                try:
                    nombre_entrees_jeu = int(cellules.first.inner_text().strip())
                    total_entrees_jeu += nombre_entrees_jeu
                except ValueError:
                    continue 
        
        total_matchs = 0
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator("td:nth-of-type(6)")
            if cellules.count() > 0: 
                try:
                    nombre_matchs = int(cellules.first.inner_text().strip())
                    total_matchs += nombre_matchs
                except ValueError:
                    continue 
        
        return total_matchs - total_entrees_jeu

    @staticmethod
    def scrap_nombre_buts_25_26(page: Page) -> int:
        selector = "tr:has(td.zentriert:has-text('25/26'))"
        lignes = page.locator(selector)
        if lignes.count() == 0:
            return 0  
        
        total_buts = 0 
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator("td:nth-of-type(8)")
            if cellules.count() > 0: 
                try:
                    nombre_buts = int(cellules.first.inner_text().strip())
                    total_buts += nombre_buts
                except ValueError:
                    continue 
        
        return total_buts

    @staticmethod
    def scrap_nombre_passes_d_25_26(page: Page) -> int:
        selector = "tr:has(td.zentriert:has-text('25/26'))"
        lignes = page.locator(selector)
        if lignes.count() == 0:
            return 0  
        
        total_passes_d = 0 
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator("td:nth-of-type(9)")
            if cellules.count() > 0: 
                try:
                    nombre_passes_d = int(cellules.first.inner_text().strip())
                    total_passes_d += nombre_passes_d
                except ValueError:
                    continue 
        
        return total_passes_d

    @staticmethod
    def scrap_nombre_penaltys_25_26(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()
        if position_joueur == "Gardien de but":
            return 0
        else: 
            selector = "tr:has(td.zentriert:has-text('25/26'))"
            lignes = page.locator(selector)
            if lignes.count() == 0:
                return 0  
            
            total_penalty = 0 
            for i in range(lignes.count()):
                cellules = lignes.nth(i).locator("td:nth-of-type(16)")
                if cellules.count() > 0: 
                    try:
                        nombre_penalty = int(cellules.first.inner_text().strip())
                        total_penalty += nombre_penalty
                    except ValueError:
                        continue 
            
            return total_penalty

    @staticmethod
    def scrap_nombre_buts_encaisses_25_26(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()
        if position_joueur != "Gardien de but":
            return 0
        else: 
            selector = "tr:has(td.zentriert:has-text('25/26'))"
            lignes = page.locator(selector)
            if lignes.count() == 0:
                return 0  
            
            total_buts_encaisses = 0 
            for i in range(lignes.count()):
                cellules = lignes.nth(i).locator("td:nth-of-type(15)")
                if cellules.count() > 0: 
                    try:
                        nombre_buts_encaisses = int(cellules.first.inner_text().strip())
                        total_buts_encaisses += nombre_buts_encaisses
                    except ValueError:
                        continue 
            
            return total_buts_encaisses

    @staticmethod
    def scrap_nombre_clean_sheets_25_26(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()
        if position_joueur == "Gardien de but":

            selector = "tr:has(td.zentriert:has-text('25/26'))"
            lignes = page.locator(selector)
            if lignes.count() == 0:
                return 0  
            
            total_clean_sheet = 0 
            for i in range(lignes.count()):
                cellules = lignes.nth(i).locator("td:nth-of-type(16)")
                if cellules.count() > 0: 
                    try:
                        nombre_clean_sheet = int(cellules.first.inner_text().strip())
                        total_clean_sheet += nombre_clean_sheet
                    except ValueError:
                        continue 
            
            return total_clean_sheet
        
        else:
            return 0

    @staticmethod
    def scrap_minutes_jouees_25_26(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()
        if position_joueur == "Gardien de but":

            selector = "tr:has(td.zentriert:has-text('25/26'))"
            lignes = page.locator(selector)
            if lignes.count() == 0:
                return 0  
            
            total_minutes_jouees = 0 
            for i in range(lignes.count()):
                cellules = lignes.nth(i).locator("td:nth-of-type(17)")
                if cellules.count() > 0: 
                    try:
                        texte_minutes = cellules.first.inner_text().strip()
                        texte_minutes = texte_minutes.replace("'","").replace(".","")
                        nombre_minutes_jouees = int(texte_minutes)
                        total_minutes_jouees += nombre_minutes_jouees
                    except ValueError:
                        continue 
            
            return total_minutes_jouees
        
        else:
            selector = "tr:has(td.zentriert:has-text('25/26'))"
            lignes = page.locator(selector)
            if lignes.count() == 0:
                return 0  
            
            total_minutes_jouees = 0 
            for i in range(lignes.count()):
                cellules = lignes.nth(i).locator("td:nth-of-type(18)")
                if cellules.count() > 0: 
                    try:
                        texte_minutes = cellules.first.inner_text().strip()
                        texte_minutes = texte_minutes.replace("'","").replace(".","")
                        nombre_minutes_jouees = int(texte_minutes)
                        total_minutes_jouees += nombre_minutes_jouees
                    except ValueError:
                        continue 
            
            return total_minutes_jouees

# --- STATS 24/25 ---

    @staticmethod
    def scrap_nombre_matchs_24_25(page: Page) -> int:
        selector = "tr:has(td.zentriert:has-text('24/25'))"
        lignes = page.locator(selector)
        if lignes.count() == 0:
            return 0  
        
        total_matchs = 0 
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator("td:nth-of-type(6)")
            if cellules.count() > 0: 
                try:
                    nombre_matchs = int(cellules.first.inner_text().strip())
                    total_matchs += nombre_matchs
                except ValueError:
                    continue 
        
        return total_matchs
    
    @staticmethod
    def scrap_entrees_en_jeu_24_25(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()

        if position_joueur == "Gardien de but":
            td_selector = "td:nth-of-type(10)"
        else:
            td_selector = "td:nth-of-type(11)"
        
        selector = "tr:has(td.zentriert:has-text('24/25'))"
        lignes = page.locator(selector)
        if lignes.count() == 0:
            return 0  
        
        total_entrees_jeu = 0
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator(td_selector)
            if cellules.count() > 0: 
                try:
                    nombre_entrees_jeu = int(cellules.first.inner_text().strip())
                    total_entrees_jeu += nombre_entrees_jeu
                except ValueError:
                    continue 
        
        return total_entrees_jeu
    
    @staticmethod
    def scrap_titularisations_24_25(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()
        
        if position_joueur == "Gardien de but":
            td_selector_entrees = "td:nth-of-type(10)"
        else:
            td_selector_entrees = "td:nth-of-type(11)"
        
        selector = "tr:has(td.zentriert:has-text('24/25'))"
        lignes = page.locator(selector)
        if lignes.count() == 0:
            return 0  
        
        total_entrees_jeu = 0
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator(td_selector_entrees)
            if cellules.count() > 0: 
                try:
                    nombre_entrees_jeu = int(cellules.first.inner_text().strip())
                    total_entrees_jeu += nombre_entrees_jeu
                except ValueError:
                    continue 
        
        total_matchs = 0
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator("td:nth-of-type(6)")
            if cellules.count() > 0: 
                try:
                    nombre_matchs = int(cellules.first.inner_text().strip())
                    total_matchs += nombre_matchs
                except ValueError:
                    continue 
        
        return total_matchs - total_entrees_jeu

    @staticmethod
    def scrap_nombre_buts_24_25(page: Page) -> int:
        selector = "tr:has(td.zentriert:has-text('24/25'))"
        lignes = page.locator(selector)
        if lignes.count() == 0:
            return 0  
        
        total_buts = 0 
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator("td:nth-of-type(8)")
            if cellules.count() > 0: 
                try:
                    nombre_buts = int(cellules.first.inner_text().strip())
                    total_buts += nombre_buts
                except ValueError:
                    continue 
        
        return total_buts
    
    @staticmethod
    def scrap_nombre_passes_d_24_25(page: Page) -> int:
        selector = "tr:has(td.zentriert:has-text('24/25'))"
        lignes = page.locator(selector)
        if lignes.count() == 0:
            return 0  
        
        total_passes_d = 0 
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator("td:nth-of-type(9)")
            if cellules.count() > 0: 
                try:
                    nombre_passes_d = int(cellules.first.inner_text().strip())
                    total_passes_d += nombre_passes_d
                except ValueError:
                    continue 
        
        return total_passes_d
    
    @staticmethod
    def scrap_nombre_passes_d_24_25(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()
        if position_joueur == "Gardien de but":
            return 0
        
        selector = "tr:has(td.zentriert:has-text('24/25'))"
        lignes = page.locator(selector)
        if lignes.count() == 0:
            return 0  
        
        total_passes_d = 0 
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator("td:nth-of-type(9)")
            if cellules.count() > 0: 
                try:
                    nombre_passes_d = int(cellules.first.inner_text().strip())
                    total_passes_d += nombre_passes_d
                except ValueError:
                    continue 
        
        return total_passes_d
    
    @staticmethod
    def scrap_nombre_penaltys_24_25(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()
        if position_joueur == "Gardien de but":
            return 0
        else: 
            selector = "tr:has(td.zentriert:has-text('24/25'))"
            lignes = page.locator(selector)
            if lignes.count() == 0:
                return 0  
            
            total_penalty = 0 
            for i in range(lignes.count()):
                cellules = lignes.nth(i).locator("td:nth-of-type(16)")
                if cellules.count() > 0: 
                    try:
                        nombre_penalty = int(cellules.first.inner_text().strip())
                        total_penalty += nombre_penalty
                    except ValueError:
                        continue 
            
            return total_penalty
        
    @staticmethod
    def scrap_nombre_buts_encaisses_24_25(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()
        if position_joueur != "Gardien de but":
            return 0
        else: 
            selector = "tr:has(td.zentriert:has-text('24/25'))"
            lignes = page.locator(selector)
            if lignes.count() == 0:
                return 0  
            
            total_buts_encaisses = 0 
            for i in range(lignes.count()):
                cellules = lignes.nth(i).locator("td:nth-of-type(15)")
                if cellules.count() > 0: 
                    try:
                        nombre_buts_encaisses = int(cellules.first.inner_text().strip())
                        total_buts_encaisses += nombre_buts_encaisses
                    except ValueError:
                        continue 
            
            return total_buts_encaisses
        
    @staticmethod
    def scrap_nombre_clean_sheets_24_25(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()
        if position_joueur == "Gardien de but":

            selector = "tr:has(td.zentriert:has-text('24/25'))"
            lignes = page.locator(selector)
            if lignes.count() == 0:
                return 0  
            
            total_clean_sheet = 0 
            for i in range(lignes.count()):
                cellules = lignes.nth(i).locator("td:nth-of-type(16)")
                if cellules.count() > 0: 
                    try:
                        nombre_clean_sheet = int(cellules.first.inner_text().strip())
                        total_clean_sheet += nombre_clean_sheet
                    except ValueError:
                        continue 
            
            return total_clean_sheet
        
        else:
            return 0

    @staticmethod
    def scrap_minutes_jouees_24_25(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()
        if position_joueur == "Gardien de but":

            selector = "tr:has(td.zentriert:has-text('24/25'))"
            lignes = page.locator(selector)
            if lignes.count() == 0:
                return 0  
            
            total_minutes_jouees = 0 
            for i in range(lignes.count()):
                cellules = lignes.nth(i).locator("td:nth-of-type(17)")
                if cellules.count() > 0: 
                    try:
                        texte_minutes = cellules.first.inner_text().strip()
                        texte_minutes = texte_minutes.replace("'","").replace(".","")
                        nombre_minutes_jouees = int(texte_minutes)
                        total_minutes_jouees += nombre_minutes_jouees
                    except ValueError:
                        continue 
            
            return total_minutes_jouees
        
        else:
            selector = "tr:has(td.zentriert:has-text('24/25'))"
            lignes = page.locator(selector)
            if lignes.count() == 0:
                return 0  
            
            total_minutes_jouees = 0 
            for i in range(lignes.count()):
                cellules = lignes.nth(i).locator("td:nth-of-type(18)")
                if cellules.count() > 0: 
                    try:
                        texte_minutes = cellules.first.inner_text().strip()
                        texte_minutes = texte_minutes.replace("'","").replace(".","")
                        nombre_minutes_jouees = int(texte_minutes)
                        total_minutes_jouees += nombre_minutes_jouees
                    except ValueError:
                        continue 
            
            return total_minutes_jouees

# --- STATS 23/24 ---

    @staticmethod
    def scrap_nombre_matchs_23_24(page: Page) -> int:
        selector = "tr:has(td.zentriert:has-text('23/24'))"
        lignes = page.locator(selector)
        if lignes.count() == 0:
            return 0  
        
        total_matchs = 0 
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator("td:nth-of-type(6)")
            if cellules.count() > 0: 
                try:
                    nombre_matchs = int(cellules.first.inner_text().strip())
                    total_matchs += nombre_matchs
                except ValueError:
                    continue 
        
        return total_matchs

    @staticmethod
    def scrap_entrees_en_jeu_23_24(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()

        if position_joueur == "Gardien de but":
            td_selector = "td:nth-of-type(10)"
        else:
            td_selector = "td:nth-of-type(11)"
        
        selector = "tr:has(td.zentriert:has-text('23/24'))"
        lignes = page.locator(selector)
        if lignes.count() == 0:
            return 0  
        
        total_entrees_jeu = 0
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator(td_selector)
            if cellules.count() > 0: 
                try:
                    nombre_entrees_jeu = int(cellules.first.inner_text().strip())
                    total_entrees_jeu += nombre_entrees_jeu
                except ValueError:
                    continue 
        
        return total_entrees_jeu
    
    @staticmethod
    def scrap_titularisations_23_24(page: Page) -> tuple[int, str]:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()
        
        if position_joueur == "Gardien de but":
            td_selector_entrees = "td:nth-of-type(10)"
        else:
            td_selector_entrees = "td:nth-of-type(11)"
        
        selector = "tr:has(td.zentriert:has-text('23/24'))"
        lignes = page.locator(selector)
        if lignes.count() == 0:
            return 0  
        
        total_entrees_jeu = 0
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator(td_selector_entrees)
            if cellules.count() > 0: 
                try:
                    nombre_entrees_jeu = int(cellules.first.inner_text().strip())
                    total_entrees_jeu += nombre_entrees_jeu
                except ValueError:
                    continue 
        
        total_matchs = 0
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator("td:nth-of-type(6)")
            if cellules.count() > 0: 
                try:
                    nombre_matchs = int(cellules.first.inner_text().strip())
                    total_matchs += nombre_matchs
                except ValueError:
                    continue 
        
        return total_matchs - total_entrees_jeu

    @staticmethod
    def scrap_nombre_buts_23_24(page: Page) -> int:
        selector = "tr:has(td.zentriert:has-text('23/24'))"
        lignes = page.locator(selector)
        if lignes.count() == 0:
            return 0  
        
        total_buts = 0 
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator("td:nth-of-type(8)")
            if cellules.count() > 0: 
                try:
                    nombre_buts = int(cellules.first.inner_text().strip())
                    total_buts += nombre_buts
                except ValueError:
                    continue 
        
        return total_buts

    @staticmethod
    def scrap_nombre_passes_d_23_24(page: Page) -> int:
        selector = "tr:has(td.zentriert:has-text('23/24'))"
        lignes = page.locator(selector)
        if lignes.count() == 0:
            return 0  
        
        total_passes_d = 0 
        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator("td:nth-of-type(9)")
            if cellules.count() > 0: 
                try:
                    nombre_passes_d = int(cellules.first.inner_text().strip())
                    total_passes_d += nombre_passes_d
                except ValueError:
                    continue 
        
        return total_passes_d

    @staticmethod
    def scrap_nombre_penaltys_23_24(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()
        if position_joueur == "Gardien de but":
            return 0
        else: 
            selector = "tr:has(td.zentriert:has-text('23/24'))"
            lignes = page.locator(selector)
            if lignes.count() == 0:
                return 0  
            
            total_penalty = 0 
            for i in range(lignes.count()):
                cellules = lignes.nth(i).locator("td:nth-of-type(16)")
                if cellules.count() > 0: 
                    try:
                        nombre_penalty = int(cellules.first.inner_text().strip())
                        total_penalty += nombre_penalty
                    except ValueError:
                        continue 
            
            return total_penalty

    @staticmethod
    def scrap_nombre_buts_encaisses_23_24(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()
        if position_joueur != "Gardien de but":
            return 0
        else: 
            selector = "tr:has(td.zentriert:has-text('23/24'))"
            lignes = page.locator(selector)
            if lignes.count() == 0:
                return 0  
            
            total_buts_encaisses = 0 
            for i in range(lignes.count()):
                cellules = lignes.nth(i).locator("td:nth-of-type(15)")
                if cellules.count() > 0: 
                    try:
                        nombre_buts_encaisses = int(cellules.first.inner_text().strip())
                        total_buts_encaisses += nombre_buts_encaisses
                    except ValueError:
                        continue 
            
            return total_buts_encaisses

    @staticmethod
    def scrap_nombre_clean_sheets_23_24(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()
        if position_joueur == "Gardien de but":

            selector = "tr:has(td.zentriert:has-text('23/24'))"
            lignes = page.locator(selector)
            if lignes.count() == 0:
                return 0  
            
            total_clean_sheet = 0 
            for i in range(lignes.count()):
                cellules = lignes.nth(i).locator("td:nth-of-type(16)")
                if cellules.count() > 0: 
                    try:
                        nombre_clean_sheet = int(cellules.first.inner_text().strip())
                        total_clean_sheet += nombre_clean_sheet
                    except ValueError:
                        continue 
            
            return total_clean_sheet
        
        else:
            return 0

    @staticmethod
    def scrap_minutes_jouees_23_24(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()
        if position_joueur == "Gardien de but":

            selector = "tr:has(td.zentriert:has-text('23/24'))"
            lignes = page.locator(selector)
            if lignes.count() == 0:
                return 0  
            
            total_minutes_jouees = 0 
            for i in range(lignes.count()):
                cellules = lignes.nth(i).locator("td:nth-of-type(17)")
                if cellules.count() > 0: 
                    try:
                        texte_minutes = cellules.first.inner_text().strip()
                        texte_minutes = texte_minutes.replace("'","").replace(".","")
                        nombre_minutes_jouees = int(texte_minutes)
                        total_minutes_jouees += nombre_minutes_jouees
                    except ValueError:
                        continue 
            
            return total_minutes_jouees
        
        else:
            selector = "tr:has(td.zentriert:has-text('23/24'))"
            lignes = page.locator(selector)
            if lignes.count() == 0:
                return 0  
            
            total_minutes_jouees = 0 
            for i in range(lignes.count()):
                cellules = lignes.nth(i).locator("td:nth-of-type(18)")
                if cellules.count() > 0: 
                    try:
                        texte_minutes = cellules.first.inner_text().strip()
                        texte_minutes = texte_minutes.replace("'","").replace(".","")
                        nombre_minutes_jouees = int(texte_minutes)
                        total_minutes_jouees += nombre_minutes_jouees
                    except ValueError:
                        continue 
            
            return total_minutes_jouees
        





