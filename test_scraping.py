import scrapy
import requests
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

class SteamGamesSpider(scrapy.Spider):
    name = "steam_games"
    allowed_domains = ["store.steampowered.com"]

    # Limite d'éléments à collecter
    MAX_GAMES = 20
    count = 0  # compteur interne

    start_urls = [
        "https://store.steampowered.com/search/?filter=topsellers"
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("a", class_="search_result_row")

        for r in results:

            if self.count >= self.MAX_GAMES:
                print(f"📌 Limite atteinte ({self.MAX_GAMES} jeux), arrêt du scraping.")
                return  # stop immédiatement

            name = r.find("span", class_="title").text.strip()
            url_game = r.get("href")

            game_id = None
            if "/app/" in url_game:
                game_id = url_game.split("/app/")[1].split("/")[0]

            # Prix HTML brut
            price_tag = r.find("div", class_="col search_price")
            price_html = price_tag.text.strip().replace("\n", " ") if price_tag else "N/A"

            # Récupération API si possible
            api_data = self.fetch_api_data(game_id) if game_id else {}

            self.count += 1  # compteur incrementé

            yield {
                "rank": self.count,
                "name": name,
                "url": url_game,
                "steam_id": game_id,
                "price_html": price_html,
                "price_api": api_data.get("price"),
                "review_score": api_data.get("review_score"),
                "release_date": api_data.get("release_date"),
                "tags": api_data.get("tags"),
            }

    def fetch_api_data(self, game_id):
        """Appel API interne Steam pour enrichir les infos."""
        api_url = f"https://store.steampowered.com/api/appdetails?appids={game_id}&cc=fr&l=french"

        try:
            res = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"})
            json_data = res.json()
            data = json_data[str(game_id)].get("data", {})

            price = None
            if "price_overview" in data:
                price = data["price_overview"].get("final_formatted")

            return {
                "price": price,
                "review_score": data.get("metacritic", {}).get("score"),
                "release_date": data.get("release_date", {}).get("date"),
                "tags": [g["description"] for g in data.get("genres", [])] if "genres" in data else None,
            }

        except Exception:
            return {}

# ---- Lancement ----
if __name__ == "__main__":
    process = CrawlerProcess({
        "USER_AGENT": "Mozilla/5.0",
        "ROBOTSTXT_OBEY": False,
        "FEED_FORMAT": "csv",
        "FEED_URI": "steam_data_limited.csv",

    })
    process.crawl(SteamGamesSpider)
    process.start()