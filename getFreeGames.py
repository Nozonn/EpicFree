import requests
from datetime import datetime

def get_free_games():
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=fr-FR&country=FR&allowCountries=FR"
    response = requests.get(url)
    if response.status_code != 200:
        print("Erreur lors de la récupération des jeux gratuits.")
        return []

    data = response.json()
    free_games = []
    idGame = 0

    for game in data['data']['Catalog']['searchStore']['elements']:
        title = game['title']
        promotions = game.get('promotions')
        if promotions:
            for promo in promotions['promotionalOffers']:
                for offer in promo['promotionalOffers']:
                    start_date = datetime.fromisoformat(offer['startDate'][:-1])
                    end_date = datetime.fromisoformat(offer['endDate'][:-1])
                    if start_date <= datetime.now() <= end_date:
                        if game["catalogNs"]["mappings"] not in (None, []):
                            url = game["catalogNs"]["mappings"][0]["pageSlug"]
                        else:
                            continue
                        if game["offerMappings"] != []:
                            url = game["offerMappings"][0]["pageSlug"]

                        idGame += 1
                        free_games.append({
                            "title": title,
                            "description": game["description"],
                            "start_date": start_date.strftime('%A %d %B %Y'),
                            "end_date": end_date.strftime('%A %d %B %Y'),
                            "image": game["keyImages"][2]["url"],
                            "url": url,
                            "id": idGame
                        })
    return free_games

def display_free_games(games):
    if not games:
        print("Aucun jeu gratuit actuellement disponible.")
    else:
        print("Jeux gratuits disponibles cette semaine sur Epic Games:")
        for game in games:
            print(f"{game['title']} (Disponible du {game['start_date'].strftime('%Y-%m-%d')} au {game['end_date'].strftime('%Y-%m-%d')})")
