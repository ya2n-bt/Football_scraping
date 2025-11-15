import re
from playwright.sync_api import Page

class ScrapElements:
    @staticmethod
    def scrap_nom(page: Page) -> str:
        page.wait_for_selector(".data-header__headline-wrapper", timeout=5000)
        nom_joueur = page.locator(".data-header__headline-wrapper").inner_text().strip()
        nom_joueur_filtre = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', nom_joueur).strip()
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
    def scrap_age(page: Page) -> int:
        page.wait_for_selector("span[itemprop='birthDate'].data-header__content", timeout=5000)
        age_joueur = page.locator("span[itemprop='birthDate'].data-header__content").inner_text().strip()
        age_joueur_filtre = re.search(r'\((.*?)\)', age_joueur)
        if age_joueur_filtre is not None:
            return int(age_joueur_filtre.group(1).strip())
        else:
            return "Âge non trouvé"
        
    @staticmethod
    def scrap_taille(page: Page) -> float:
        page.wait_for_selector("span[itemprop='height'].data-header__content", timeout=5000)
        taille_joueur = page.locator("span[itemprop='height'].data-header__content").inner_text().strip()
        taille_joueur_filtre = taille_joueur.replace(' m', '').replace(',', '.').strip()
        if taille_joueur_filtre is not None:
            return float(taille_joueur_filtre)
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
    def scrap_valeur(page: Page) -> float:
        page.wait_for_selector("a.data-header__market-value-wrapper", timeout=5000)
        valeur_brute = page.locator("a.data-header__market-value-wrapper").inner_text().split()[0].strip()
        valeur_brute = valeur_brute.replace(',', '.') 
        unite = page.locator("a.data-header__market-value-wrapper span.waehrung").inner_text().strip()
        if "mio. €" in unite:
            multiplicateur = 1_000_000
        elif "K €" in unite:
            multiplicateur = 1_000
        else:
            multiplicateur = 1 
        valeur = float(valeur_brute) * multiplicateur

        try:
            return valeur
        except ValueError:
            return "Valeur non trouvée" 
        
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
    def scrap_nombre_penaltys_buts_encaisses_24_25(page: Page) -> int:
        position_joueur = page.locator("li.data-header__label:has-text('Position:') > span.data-header__content").inner_text().strip()
        if position_joueur != "Gardien de but":

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
            
            return {"Nombre de penaltys 24/25": total_penalty,
                    "Nombre de buts encaissés 24/25": 0}

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
            
            return {"Nombre de penaltys 24/25": 0,
                    "Nombre de buts encaissés 24/25": total_buts_encaisses}
        
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
            
        

