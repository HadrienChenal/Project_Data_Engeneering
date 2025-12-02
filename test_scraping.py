import scrapy
import requests
from bs4 import BeautifulSoup

class SteamGamesSpider(scrapy.Spider):
    name = "steam_games"
    allowed_domains = ["store.steampowered.com"]
    
    # URL de base (ici page de recherche pour tous les jeux populaires)
    start_urls = [
        "https://store.steampowered.com/search/?filter=topsellers"
    ]

    def parse(self, response):
        """
        Scraping des jeux sur la page de recherche Steam.
        """
        # On récupère le HTML
        html = response.text

        # On parse avec BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # Chaque jeu est dans <a class="search_result_row">
        results = soup.find_all("a", class_="search_result_row")

        for r in results:
            # Nom
            title_tag = r.find("span", class_="title")
            name = title_tag.text.strip() if title_tag else "Nom inconnu"

            # Prix
            price_tag = r.find("div", class_="col search_price")
            if price_tag:
                price_text = price_tag.text.strip()
                # Nettoyage du texte (prix normal ou réduit)
                price = price_text.split("\n")[0].strip()
                if not price:
                    price = "Gratuit ou non disponible"
            else:
                price = "Prix non disponible"

            # URL du jeu
            url_game = r.get("href", "URL non disponible")

            # Yield un dictionnaire pour Scrapy (ou pour export CSV)
            yield {
                "name": name,
                "price": price,
                "url": url_game
            }

        # Pagination (si tu veux scrapper plusieurs pages)
        next_page = soup.find("a", class_="pagebtn", text=">")
        if next_page:
            next_url = next_page.get("href")
            if next_url:
                yield scrapy.Request(url=next_url, callback=self.parse)