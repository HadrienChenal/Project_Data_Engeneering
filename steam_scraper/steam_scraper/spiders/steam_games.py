import scrapy


class SteamGamesSpider(scrapy.Spider):
    name = "steam_games"
    allowed_domains = ["store.steampowered.com"]
    start_urls = ["https://store.steampowered.com"]

    def parse(self, response):
        pass
