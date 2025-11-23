from playwright.sync_api import Page
import re

class ScrapProfil:
    @staticmethod
    def scrap_pied_fort(page: Page) -> str:
        selector = "span:has-text('Pied:') + span"
        if page.locator(selector).first.is_visible(timeout=500):
            try:
                pied_fort =  page.locator(selector).inner_text().strip()
                return pied_fort
            except Exception:
                return "Pied fort non trouvé"
        else:
            return "Pied fort non trouvé"