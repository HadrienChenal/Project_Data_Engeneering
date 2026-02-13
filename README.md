# Steam Data Engineering Project

## Présentation du projet

Ce projet a été réalisé dans le cadre de l’unité Data Engineering. Le principe du projet est de collecter des données depuis un site web en scrapant des données, on doit ensuite stocker ces données dans une base de données, puis les exploiter à travers une application web interactive et enfin on doit pouvoir le faire tourner sur Docker.

Dans notre cas, nous avons choisi de scraper des données issues du site Steam, de stocker ces données dans une base MongoDB et les afficher via une application web développée avec Streamlit

## Structure du projet

L’organisation du projet est la suivante :

```bash
PROJECT_DATA_ENGINEERING/
│
├── dashboard/               # Application web Streamlit
│   ├── app.py               # Interface principale
│   ├── db.py                # Connexion MongoDB
│   └── requirements.txt     # Dépendances Python
│
├── steam_scraper/           # Projet Scrapy
│   ├── spiders/             # Spiders de scraping
│   │   └── steam_games.py
│   │
│   ├── items.py             # Structure des données
│   ├── pipelines.py         # Envoi vers MongoDB
│   ├── settings.py          # Configuration Scrapy
│
├── docker-compose.yml       # Orchestration des services
├── Dockerfile.scraper       # Image Docker Scraper
├── Dockerfile.web           # Image Docker Web
├── scrapy.cfg               # Configuration Scrapy
└── README.md
```


## Scraping des données

Pour chaque jeu du Top 100 Steam :

Rang, Nom, URL, Steam ID, Prix, Pourcentage de réduction, Score Metacritic, Nombre d’avis, Date de sortie, Genres (tags), Date de scraping

### Fonctionnement

Scraping du HTML dynamique via l’endpoint search/results
Parsing avec BeautifulSoup
Récupération du Steam ID
Enrichissement via l’API officielle Steam (appdetails)
Envoi vers MongoDB via pipeline Scrapy
Le scraping est automatiquement exécuté au démarrage du conteneur Docker.

## Base de données

Les données collectées sont stockées dans une base MongoDB.
Nous utilisons MongoDB car il y'a une facilité d’intégration avec Scrapy et que c'est compatible Docker

## Application Web

L’interface utilisateur a été développée avec Streamlit.

L’application permet :

D’afficher les jeux scrapés

De visualiser les données sous forme de tableaux et de graphiques

D’explorer dynamiquement les informations stockées

nous avons choisi Streamlit pour ca simplicité d'utilisation et sa rapidité de developpement

## Architecture Docker

L’ensemble du projet repose sur une architecture conteneurisée avec Docker et Docker Compose.

Le système est composé de trois services :

MongoDB : base de données

Scraper : service chargé de collecter les données

Web : application Streamlit permettant de visualiser les données

L’orchestration est assurée via un fichier docker-compose.yml, permettant de lancer l’ensemble du projet en une seule commande.

# Lancement du projet

Prérequis

Docker

Étapes d’exécution
```bash
git clone https://github.com/HadrienChenal/Project_Data_Engeneering.git
cd Project_Data_Engeneering
docker compose up --build
```

Une fois les containers lancés, l’application est accessible à l’adresse :

http://localhost:8501

Pour  acceder a notre projet il faut attendre que le terminal affiche tout ceci : 

```bash
steam_dashboard  |   Local URL: http://localhost:8501         
steam_dashboard  |   Network URL: http://172.18.0.4:8501      
steam_dashboard  |   External URL: http://90.79.144.99:8501   
steam_dashboard  |                                      
steam_scraper exited with code 0
```

# Choix techniques

Les choix technologiques ont été faits dans une logique de cohérence et de mise en pratique des concepts vus en cours :

Scrapy pour le scraping structuré

MongoDB pour le stockage flexible des données

Streamlit pour la visualisation interactive

Docker & Docker Compose pour la gestion des services

## Difficultés rencontrées

Lors du développement du projet, plusieurs problématiques liées à la qualité et à l’hétérogénéité des données ont été rencontrées.

Tout d’abord, certaines informations récupérées via l’API Steam ne sont pas systématiquement disponibles pour tous les jeux. Par exemple :

Certains jeux ne possèdent pas de score Metacritic

Certains jeux n’ont pas encore de recommandations

Certains champs comme price_overview n’existent pas pour les jeux gratuits

Certaines dates de sortie peuvent être indiquées comme “Prochainement” ou “À déterminer”

Dans ces cas, l’API retourne soit des champs absents, soit des valeurs vides. Cela se traduit par des valeurs None dans la base MongoDB.

Par ailleurs, les dates de sortie sont parfois renvoyées sous forme de texte localisé (ex : format français abrégé), ce qui peut empêcher leur conversion automatique en format datetime lors de l’analyse avec Pandas. Les valeurs non interprétables sont alors converties en NaT (Not a Time), ce qui explique la présence de valeurs manquantes dans certaines visualisations temporelles.