import requests
from bs4 import BeautifulSoup
import json
import time
import re

# Dictionnaire complet des rosters du LEC.
PLAYER_ROSTER = {
    "KC": [{"name": "Canna", "role": "Top"}, {"name": "Yike", "role": "Jungle"}, {"name": "Vladi", "role": "Mid"}, {"name": "Caliste", "role": "ADC"}, {"name": "Targamas", "role": "Support"}],
    "G2": [{"name": "BrokenBlade", "role": "Top"}, {"name": "SkewMond", "role": "Jungle"}, {"name": "Caps", "role": "Mid"}, {"name": "Hans Sama", "role": "ADC"}, {"name": "Labrov", "role": "Support"}],
    "MKOI": [{"name": "Myrwn", "role": "Top"}, {"name": "Elyoya", "role": "Jungle"}, {"name": "Jojopyun", "role": "Mid"}, {"name": "Supa", "role": "ADC"}, {"name": "Alvaro", "role": "Support", "url_name": "Alvaro_(Álvaro_Fernández)"}],
    "FNC": [{"name": "Oscarinin", "role": "Top"}, {"name": "Razork", "role": "Jungle"}, {"name": "Poby", "role": "Mid"}, {"name": "Upset", "role": "ADC"}, {"name": "Mikyx", "role": "Support"}],
    "VIT": [{"name": "Naak Nako", "role": "Top"}, {"name": "Lyncas", "role": "Jungle"}, {"name": "Czajek", "role": "Mid"}, {"name": "Carzzy", "role": "ADC"}, {"name": "Fleshy", "role": "Support"}],
    "BDS": [{"name": "Rooster", "role": "Top"}, {"name": "Boukada", "role": "Jungle"}, {"name": "nuc", "role": "Mid"}, {"name": "Ice", "role": "ADC", "url_name": "Ice_(Yoon_Sang-hoon)"}, {"name": "Parus", "role": "Support"}],
    "TH": [{"name": "Carlsen", "role": "Top"}, {"name": "Sheo", "role": "Jungle"}, {"name": "Kamiloo", "role": "Mid"}, {"name": "Flakked", "role": "ADC"}, {"name": "Stend", "role": "Support"}],
    "GX": [{"name": "Lot", "role": "Top"}, {"name": "Isma", "role": "Jungle", "url_name": "ISMA"}, {"name": "Jackies", "role": "Mid"}, {"name": "Noah", "role": "ADC", "url_name": "Noah_(Oh_Hyeon-taek)"}, {"name": "Jun", "role": "Support", "url_name": "Jun_(Yoon_Se-jun)"}],
    "SK": [{"name": "DnDn", "role": "Top"}, {"name": "Skeanz", "role": "Jungle"}, {"name": "Abbedagge", "role": "Mid"}, {"name": "Keduii", "role": "ADC"}, {"name": "Loopy", "role": "Support"}],
    "NAVI": [{"name": "Adam", "role": "Top", "url_name": "Adam_(Adam_Maanane)"}, {"name": "Thayger", "role": "Jungle"}, {"name": "Larssen", "role": "Mid"}, {"name": "Hans SamD", "role": "ADC"}, {"name": "Malrang", "role": "Support"}]
}

def scrape_player_stats(player_info, team_tag):
    """
    Scrape les statistiques d'un joueur en lisant toutes les lignes de champion
    et en calculant les moyennes nous-mêmes.
    """
    player_name = player_info['name']
    url_name = player_info.get('url_name', player_name)
    role = player_info['role']
    
    url = f"https://lol.fandom.com/wiki/{url_name}/Statistics/2025"
    print(f"  - Récupération des stats pour {player_name}...")

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"    -> Erreur HTTP pour {player_name}: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    
    table_title_link = soup.find('a', string="LEC/2025 Season/Summer Season")
    if not table_title_link:
        print(f"    -> Avertissement : Tableau pour 'Summer Season' non trouvé pour {player_name}.")
        return None

    stats_table = table_title_link.find_parent('table')
    if not stats_table:
        print(f"    -> Avertissement : Impossible de trouver le tableau parent pour {player_name}.")
        return None

    total_kills, total_deaths, total_assists = 0, 0, 0
    total_dpm, total_games, total_csm, total_gpm = 0, 0, 0, 0
    total_kpar, total_ks_percent, total_gold_percent = 0, 0, 0
    champion_rows_count = 0
    
    tbody = stats_table.find('tbody')
    if not tbody:
        print(f"    -> Erreur : Corps du tableau (tbody) non trouvé pour {player_name}.")
        return None

    for row in tbody.find_all('tr'):
        if row.find('th'):
            continue
        
        champion_rows_count += 1
        cols = row.find_all('td')
        try:
            # Utilisation d'indices de colonnes fixes pour plus de fiabilité
            games = int(cols[1].text.strip())
            kills = float(cols[5].text.strip()) * games
            deaths = float(cols[6].text.strip()) * games
            assists = float(cols[7].text.strip()) * games
            csm = float(cols[10].text.strip()) * games
            gpm = float(cols[12].text.strip()) * games
            dpm = float(cols[14].text.strip()) * games
            kpar = float(cols[15].text.strip().replace('%','')) * games
            ks_percent = float(cols[16].text.strip().replace('%','')) * games
            gold_percent = float(cols[17].text.strip().replace('%','')) * games

            total_kills += kills
            total_deaths += deaths
            total_assists += assists
            total_dpm += dpm
            total_games += games
            total_csm += csm
            total_gpm += gpm
            total_kpar += kpar
            total_ks_percent += ks_percent
            total_gold_percent += gold_percent

        except (ValueError, IndexError) as e:
            print(f"    -> Avertissement : Impossible de traiter une ligne pour {player_name}. Erreur : {e}")
            continue

    if total_games == 0:
        print(f"    -> Avertissement : Aucune partie jouée trouvée pour {player_name}.")
        return None

    final_kda = (total_kills + total_assists) / max(1, total_deaths)
    final_dpm = total_dpm / total_games
    final_csm = total_csm / total_games
    final_gpm = total_gpm / total_games
    final_kpar = total_kpar / total_games
    final_ks_percent = total_ks_percent / total_games
    final_gold_percent = total_gold_percent / total_games

    return {
        "id": player_name,
        "name": player_name,
        "team": team_tag,
        "role": role,
        "stats": {
            "dpm": int(final_dpm),
            "kda": round(final_kda, 2),
            "champPool": champion_rows_count,
            "csm": round(final_csm, 2),
            "gpm": int(final_gpm),
            "kpar": f"{round(final_kpar, 1)}%",
            "ks_percent": f"{round(final_ks_percent, 1)}%",
            "gold_percent": f"{round(final_gold_percent, 1)}%"
        }
    }

def get_all_player_stats():
    """
    Itère sur tous les joueurs du roster et récupère leurs statistiques.
    """
    all_players_data = []
    total_players = sum(len(players) for players in PLAYER_ROSTER.values())
    count = 0
    
    print(f"Début du scraping pour {total_players} joueurs...")

    for team_tag, players in PLAYER_ROSTER.items():
        for player_info in players:
            count += 1
            print(f"Traitement du joueur {count}/{total_players} : {player_info['name']} ({team_tag})")
            player_data = scrape_player_stats(player_info, team_tag)
            if player_data:
                all_players_data.append(player_data)
            time.sleep(0.5)
            
    return all_players_data

if __name__ == "__main__":
    final_data = get_all_player_stats()
    if final_data:
        with open('player_stats.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"\nOpération terminée. {len(final_data)} profils de joueurs ont été enregistrés dans 'player_stats.json'")
    else:
        print("\nAucune donnée n'a pu être récupérée. Le fichier n'a pas été créé.")

