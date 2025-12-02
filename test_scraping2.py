import requests

# --- 1. Récupérer les données de l'API Steam ---
url = "https://store.steampowered.com/api/featuredcategories/"

try:
    response = requests.get(url)
    data = response.json()
except Exception as e:
    print("Erreur lors de la récupération des données :", e)
    exit()

# --- 2. Vérifier que la section 'Populaires et recommandés' existe ---
if "featured_win" in data and "items" in data["featured_win"] and data["featured_win"]["items"]:
    first_game = data["featured_win"]["items"][0]

    # Nom du jeu
    name = first_game.get("name", "Nom inconnu")

    # Prix du jeu
    price_raw = first_game.get("final_price")
    if price_raw is None:
        price = "Gratuit ou non disponible"
    else:
        price = f"{price_raw / 100:.2f} €"

    # URL du jeu
    url_game = first_game.get("url", "URL non disponible")

    # --- 3. Affichage ---
    print("Premier jeu ‘Populaires et recommandés’ :")
    print("Nom :", name)
    print("Prix :", price)
    print("URL :", url_game)

else:
    print("Aucun jeu trouvé dans 'Populaires et recommandés'.")
