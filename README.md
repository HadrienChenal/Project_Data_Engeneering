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

Nous utilisons Scrapy pour :

Collecter les données des jeux Steam

Extraire nom, prix, rating, etc.

Structurer les données via items.py

Envoyer les données vers MongoDB via pipelines.py

Le scraping est déclenché automatiquement au lancement du container .


## Base de données

Les données collectées sont stockées dans une base MongoDB.

Nous utilisons MongoDB car il y'a une facilité d’intégration avec Scrapy et que c'est compatible Docker

## Application Web

L’interface utilisateur a été développée avec Streamlit.

L’application permet :

D’afficher les jeux scrapés

De visualiser les données sous forme de tableaux et de graphiques

D’explorer dynamiquement les informations stockées

nous avons choisi Streamlit pour ca simplicité d'utilisatio et sa rapidité de developpement

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

Docker Compose

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

