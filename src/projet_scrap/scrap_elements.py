import re
from playwright.sync_api import Page

def scrap_nom(page: Page) -> list[dict]:
    page.wait_for_selector(".data-header__headline-wrapper", timeout=5000)
    nom_joueur = page.locator(".data-header__headline-wrapper").inner_text().strip()
    nom_joueur_filtre = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', nom_joueur).strip()
    if nom_joueur_filtre:
        return [{"nom_joueur": nom_joueur_filtre}]
    else:
        return [{"nom_joueur": "Nom non trouvé"}]