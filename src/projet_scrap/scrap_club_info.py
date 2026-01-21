from playwright.sync_api import Page
import re

class ScrapClubInfo:

    @staticmethod
    def scrap_valeur_totale_club(page: Page) -> float | None:
        selector = "a.data-header__market-value-wrapper"
        
        if page.locator(selector).is_visible(timeout=1000):
            try:

                texte_complet = page.locator(selector).inner_text().strip()
                match_valeur = re.search(r"([\d,]+)", texte_complet)
                
                if not match_valeur:
                    return "Valeur non trouvée"
                
                valeur_brute = match_valeur.group(1).replace(",", ".")
                
                texte_lower = texte_complet.lower()
                multiplicateur = 1
                
                if "mrd" in texte_lower or "bn" in texte_lower:
                    multiplicateur = 1_000_000_000
                elif "mio" in texte_lower or "m" in texte_lower: #
                    multiplicateur = 1_000_000
                elif "k" in texte_lower: 
                    multiplicateur = 1_000
                    
                return float(valeur_brute) * multiplicateur
                
            except Exception as e:
                print(f"Erreur parsing valeur club: {e}")
                return "Valeur non trouvée"
                
        return "Valeur non trouvée"

    @staticmethod
    def scrap_classement_ligue(page: Page) -> int | str:
        selector = "a[title='Classement du championnat']"
        
        if page.locator(selector).first.is_visible(timeout=1000):
            try:
                texte = page.locator(selector).first.inner_text().strip()
                if texte:
                    return int(texte)
            except Exception:
                return "Classement non trouvé"
        return "Classement non trouvé"