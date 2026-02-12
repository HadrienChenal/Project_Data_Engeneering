import scrapy
import requests
from bs4 import BeautifulSoup


class SteamGamesSpider(scrapy.Spider):
    name = "steam_games"
    allowed_domains = ["store.steampowered.com"]
    start_urls = [
        "https://store.steampowered.com/search/?filter=topsellers"
    ]

    MAX_GAMES = 20
    count = 0

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("a", class_="search_result_row")

        for r in results:
            if self.count >= self.MAX_GAMES:
                self.logger.info(f"Limite atteinte ({self.MAX_GAMES} jeux)")
                return

            name = r.find("span", class_="title").text.strip()
            url_game = r.get("href")

            steam_id = None
            if "/app/" in url_game:
                steam_id = url_game.split("/app/")[1].split("/")[0]

            price_tag = r.find("div", class_="col search_price")
            price_html = price_tag.text.strip().replace("\n", " ") if price_tag else "N/A"

            api_data = self.fetch_api_data(steam_id) if steam_id else {}

            self.count += 1

            yield {
                "rank": self.count,
                "name": name,
                "url": url_game,
                "steam_id": steam_id,
                "price_html": price_html,
                "price_api": api_data.get("price"),
                "review_score": api_data.get("review_score"),
                "release_date": api_data.get("release_date"),
                "tags": api_data.get("tags"),
            }

    def fetch_api_data(self, steam_id):
        api_url = f"https://store.steampowered.com/api/appdetails?appids={steam_id}&cc=fr&l=french"

        try:
            res = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"})
            data = res.json().get(str(steam_id), {}).get("data", {})

            price = None
            if "price_overview" in data:
                price = data["price_overview"].get("final_formatted")

            return {
                "price": price,
                "review_score": data.get("metacritic", {}).get("score"),
                "release_date": data.get("release_date", {}).get("date"),
                "tags": [g["description"] for g in data.get("genres", [])],
            }

        except Exception:
            return {}
