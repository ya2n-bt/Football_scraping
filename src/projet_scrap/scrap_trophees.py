from playwright.sync_api import Page

class ScrapTrophees:
    @staticmethod
    def scrap_nombre_trophees(page: Page) -> int | str:
        periodes = ["25/26", "24/25", "23/24", "2023", "2024", "2025"]

        selector = "h2.content-box-headline:has-text('Tous les titres') ~ table tr:has(td.erfolg_table_saison.zentriert)"
        lignes = page.locator(selector)

        if lignes.count() == 0:
            return 0 

        total = 0
        for i in range(lignes.count()):
            ligne = lignes.nth(i)
            try:
                saison = ligne.locator("td.erfolg_table_saison.zentriert").inner_text().strip()
                if saison in periodes:
                    total += 1  
            except Exception as e:
                print(f"Erreur lors du traitement de la ligne {i}: {e}")
                return("Nombre de trophées non trouvé")

        return total

