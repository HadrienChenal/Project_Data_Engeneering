import requests
from bs4 import BeautifulSoup

url = "https://store.steampowered.com/?l=french"
html = requests.get(url).text

soup = BeautifulSoup(html, "html.parser")
title = soup.find("title").text

print("Titre de la page :", title)