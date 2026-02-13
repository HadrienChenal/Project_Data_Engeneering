import scrapy
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class SteamGamesSpider(scrapy.Spider):
    name = "steam_games"
    allowed_domains = ["store.steampowered.com"]

    def start_requests(self):
        url = (
            "https://store.steampowered.com/search/results/"
            "?query=&start=0&count=100&filter=topsellers&infinite=1"
        )

        yield scrapy.Request(
            url=url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json",
            },
            cookies={
                "birthtime": "568022401",
                "mature_content": "1",
            },
            callback=self.parse,
        )

    def parse(self, response):
        data = response.json()
        html = data.get("results_html", "")

        soup = BeautifulSoup(html, "html.parser")
        results = soup.find_all("a", class_="search_result_row")

        for index, r in enumerate(results, start=1):

            name = r.find("span", class_="title").text.strip()
            url_game = r.get("href")

            # Steam ID
            steam_id = None
            if "/app/" in url_game:
                steam_id = url_game.split("/app/")[1].split("/")[0]

            # Discount %
            discount_tag = r.find("div", class_="search_discount")
            discount_percent = None
            if discount_tag:
                discount_percent = (
                    discount_tag.text.strip()
                    .replace("-", "")
                    .replace("%", "")
                )

            # API enrichment
            api_data = self.fetch_api_data(steam_id) if steam_id else {}

            yield {
                "rank": index,
                "name": name,
                "url": url_game,
                "steam_id": steam_id,
                "price": api_data.get("price"),
                "discount_percent": discount_percent,
                "review_score": api_data.get("review_score"),
                "review_count": api_data.get("review_count"),
                "release_date": api_data.get("release_date"),
                "tags": api_data.get("tags"),
                "scraped_at": datetime.utcnow(),
            }

    def fetch_api_data(self, game_id):
        api_url = (
            f"https://store.steampowered.com/api/appdetails"
            f"?appids={game_id}&cc=fr&l=french"
        )

        try:
            r = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"})
            data = r.json().get(str(game_id), {}).get("data", {})

            price = None
            discount_percent = None

            if data.get("is_free"):
                price = "Gratuit"
            elif "price_overview" in data:
                price_data = data["price_overview"]
                price = price_data.get("final_formatted")
                discount_percent = price_data.get("discount_percent")

            return {
                "price": price,
                "discount_percent": discount_percent,
                "review_score": data.get("metacritic", {}).get("score"),
                "review_count": data.get("recommendations", {}).get("total"),
                "release_date": data.get("release_date", {}).get("date"),
                "tags": [g["description"] for g in data.get("genres", [])],
            }

        except Exception:
            return {}