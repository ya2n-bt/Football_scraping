from playwright.sync_api import Page
import re

class ScrapProfil:
    @staticmethod
    def scrap_pied_fort(page: Page) -> str:
        selector = "span:has-text('Pied:') + span"
        page.wait_for_selector(selector, timeout=5000)
        pied_fort = page.locator(selector).inner_text().strip()
        if pied_fort is not None:
            return pied_fort
        else: "Pied fort non trouvé"