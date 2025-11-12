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