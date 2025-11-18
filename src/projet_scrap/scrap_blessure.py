from playwright.sync_api import Page

class ScrapBlessure:
    @staticmethod
    def scrap_nombre_blessures(page: Page) -> int:
        selector = "tr:has(td.zentriert:has-text('25/26')), tr:has(td.zentriert:has-text('24/25')), tr:has(td.zentriert:has-text('23/24'))"
        lignes = page.locator(selector)
        if lignes.count() == 0:
            return 0  

        total_blessures = 0

        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator("td:nth-of-type(3)")
            if cellules.count() > 0:
                try:
                    nombre_blessures = int(cellules.first.inner_text().strip())
                    total_blessures += nombre_blessures
                except ValueError:
                    continue  

        return total_blessures
    
    @staticmethod
    def scrap_matchs_manques(page: Page) -> int:
        selector = "tr:has(td.zentriert:has-text('25/26')), tr:has(td.zentriert:has-text('24/25')), tr:has(td.zentriert:has-text('23/24'))"
        lignes = page.locator(selector)
        if lignes.count() == 0:
            return 0  

        total_matchs = 0

        for i in range(lignes.count()):
            cellules = lignes.nth(i).locator("td:nth-of-type(4)")
            if cellules.count() > 0:
                try:
                    nombre_matchs = int(cellules.first.inner_text().strip())
                    total_matchs += nombre_matchs
                except ValueError:
                    continue  

        return total_matchs