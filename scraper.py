import requests
from bs4 import BeautifulSoup
import json
import time

# Dictionnaire complet des rosters du LEC 2026 (Format Versus).
# Inclut les 10 équipes partenaires + 2 équipes invitées (Los Ratones & KC Blue).
PLAYER_ROSTER = {
    "G2": [
        {"name": "BrokenBlade", "role": "Top"},
        {"name": "SkewMond", "role": "Jungle"},
        {"name": "Caps", "role": "Mid"},
        {"name": "Hans Sama", "role": "ADC"},
        {"name": "Labrov", "role": "Support"}
    ],
    "KC": [
        {"name": "Canna", "role": "Top"},
        {"name": "Yike", "role": "Jungle"},
        {"name": "Kyeahoo", "role": "Mid"},
        {"name": "Caliste", "role": "ADC"},
        {"name": "Busio", "role": "Support"}
    ],
    "MKOI": [ # MAD Lions KOI -> Movistar KOI
        {"name": "Myrwn", "role": "Top"},
        {"name": "Elyoya", "role": "Jungle"},
        {"name": "Jojopyun", "role": "Mid"},
        {"name": "Supa", "role": "ADC"},
        {"name": "Alvaro", "role": "Support", "url_name": "Alvaro_(Álvaro_Fernández)"}
    ],
    "VIT": [
        {"name": "Naak Nako", "role": "Top"},
        {"name": "Lyncas", "role": "Jungle"},
        {"name": "Humanoid", "role": "Mid"},
        {"name": "Carzzy", "role": "ADC"},
        {"name": "Fleshy", "role": "Support"}
    ],
    "SH": [ # Ex-BDS (Shifters)
        {"name": "Rooster", "role": "Top"},
        {"name": "Boukada", "role": "Jungle"},
        {"name": "nuc", "role": "Mid"},
        {"name": "Paduck", "role": "ADC"},
        {"name": "Trymbi", "role": "Support"}
    ],
    "TH": [
        {"name": "Tracyn", "role": "Top"},
        {"name": "Sheo", "role": "Jungle"},
        {"name": "Serin", "role": "Mid"},
        {"name": "Ice", "role": "ADC", "url_name": "Ice_(Yoon_Sang-hoon)"},
        {"name": "Stend", "role": "Support"}
    ],
    "SK": [
        {"name": "Wunder", "role": "Top"},
        {"name": "Skeanz", "role": "Jungle"},
        {"name": "LIDER", "role": "Mid"},
        {"name": "Jopa", "role": "ADC"},
        {"name": "Mikyx", "role": "Support"}
    ],
    "GX": [
        {"name": "Lot", "role": "Top"},
        {"name": "ISMA", "role": "Jungle"},
        {"name": "Jackies", "role": "Mid"},
        {"name": "Noah", "role": "ADC", "url_name": "Noah_(Oh_Hyeon-taek)"},
        {"name": "Jun", "role": "Support", "url_name": "Jun_(Yoon_Se-jun)"}
    ],
    "NAVI": [ # A pris le spot de Rogue
        {"name": "Maynter", "role": "Top"},
        {"name": "Rhilech", "role": "Jungle"},
        {"name": "Poby", "role": "Mid"},
        {"name": "SamD", "role": "ADC", "url_name": "Hans_SamD"},
        {"name": "Parus", "role": "Support"}
    ],
    "FNC": [
        {"name": "Oscarinin", "role": "Top"},
        {"name": "Razork", "role": "Jungle"},
        {"name": "Smolder", "role": "Mid"}, # Rumeur la plus probable/Placeholder si non confirmé
        {"name": "Upset", "role": "ADC"}, 
        {"name": "Empyros", "role": "Support"} # Nouveau support cité dans les leaks récents
    ],
    "LRA": [ # Los Ratones (Invité)
        {"name": "Thebausffs", "role": "Top", "url_name": "Baus"},
        {"name": "Velja", "role": "Jungle"},
        {"name": "Nemesis", "role": "Mid"},
        {"name": "Crownie", "role": "ADC"},
        {"name": "Rekkles", "role": "Support"}
    ],
    "KCB": [ # KC Blue (Invité)
        {"name": "Tao", "role": "Top"},
        {"name": "Yukino", "role": "Jungle"},
        {"name": "Kamiloo", "role": "Mid"},
        {"name": "Hazel", "role": "ADC"},
        {"name": "Prime", "role": "Support"}
    ]
}

def scrape_player_stats(player_info, team_tag):
    """
    Scrape les statistiques d'un joueur pour l'année 2026.
    """
    player_name = player_info['name']
    url_name = player_info.get('url_name', player_name)
    role = player_info['role']
    
    # URL ciblée pour 2026
    url = f"https://lol.fandom.com/wiki/{url_name}/Statistics/2026"
    print(f"  - Récupération des stats pour {player_name}...")

    try:
        response = requests.get(url)
        if response.status_code == 404:
            print(f"    -> Page non trouvée pour {player_name} (404).")
            return create_empty_stats(player_name, team_tag, role)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"    -> Erreur HTTP pour {player_name}: {e}")
        return create_empty_stats(player_name, team_tag, role)

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # On cherche en priorité le tableau "Versus Season" (Format Hiver 2026)
    target_seasons = ["LEC/2026 Season/Versus Season", "LEC/2026 Season/Winter Season"]
    
    table_title_link = None
    for season_name in target_seasons:
        found_link = soup.find('a', string=season_name)
        if found_link:
            table_title_link = found_link
            print(f"    -> Tableau trouvé : {season_name}")
            break
    
    if not table_title_link:
        print(f"    -> Avertissement : Pas de stats 'Versus/Winter 2026' pour {player_name}. (Utilisation de stats vides)")
        return create_empty_stats(player_name, team_tag, role)

    stats_table = table_title_link.find_parent('table')
    if not stats_table:
        return create_empty_stats(player_name, team_tag, role)

    total_kills, total_deaths, total_assists = 0, 0, 0
    total_dpm, total_games, total_csm, total_gpm = 0, 0, 0, 0
    total_kpar, total_ks_percent, total_gold_percent = 0, 0, 0
    champion_rows_count = 0
    
    tbody = stats_table.find('tbody')
    if not tbody:
        return create_empty_stats(player_name, team_tag, role)

    for row in tbody.find_all('tr'):
        if row.find('th'): continue
        
        cols = row.find_all('td')
        if not cols or len(cols) < 15: continue

        champion_rows_count += 1
        try:
            # Indices basés sur le format standard Leaguepedia 2025/2026
            # Games: col 1, K/D/A: 5,6,7, CSM: 10, GPM: 12, DPM: 14, KP%: 15
            games = int(cols[1].text.strip())
            if games == 0: continue

            def get_val(index, is_percent=False):
                txt = cols[index].text.strip()
                if is_percent: txt = txt.replace('%', '')
                try:
                    return float(txt) if txt and txt != '-' else 0.0
                except ValueError:
                    return 0.0

            # Extraction
            kills = get_val(5) * games
            deaths = get_val(6) * games
            assists = get_val(7) * games
            csm = get_val(10) * games
            gpm = get_val(12) * games
            dpm = get_val(14) * games
            kpar = get_val(15, True) * games
            ks_percent = get_val(16, True) * games
            gold_percent = get_val(17, True) * games

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

        except (ValueError, IndexError):
            continue

    if total_games == 0:
        return create_empty_stats(player_name, team_tag, role)

    final_kda = (total_kills + total_assists) / max(1, total_deaths)
    
    return {
        "id": player_name,
        "name": player_name,
        "team": team_tag,
        "role": role,
        "stats": {
            "dpm": int(total_dpm / total_games),
            "kda": round(final_kda, 2),
            "champPool": champion_rows_count,
            "csm": round(total_csm / total_games, 2),
            "gpm": int(total_gpm / total_games),
            "kpar": f"{round(total_kpar / total_games, 1)}%",
            "ks_percent": f"{round(total_ks_percent / total_games, 1)}%",
            "gold_percent": f"{round(total_gold_percent / total_games, 1)}%"
        }
    }

def create_empty_stats(name, team, role):
    """Génère des stats par défaut si le joueur n'a pas encore joué."""
    return {
        "id": name,
        "name": name,
        "team": team,
        "role": role,
        "stats": {
            "dpm": 0, "kda": 0, "champPool": 0, "csm": 0, "gpm": 0,
            "kpar": "0%", "ks_percent": "0%", "gold_percent": "0%"
        }
    }

def get_all_player_stats():
    all_players_data = []
    total_players = sum(len(players) for players in PLAYER_ROSTER.values())
    count = 0
    
    print(f"Début du scraping LEC 2026 ({total_players} joueurs attendus)...")

    for team_tag, players in PLAYER_ROSTER.items():
        for player_info in players:
            count += 1
            print(f"[{count}/{total_players}] {player_info['name']} ({team_tag})")
            player_data = scrape_player_stats(player_info, team_tag)
            all_players_data.append(player_data)
            time.sleep(0.5) 
            
    return all_players_data

if __name__ == "__main__":
    final_data = get_all_player_stats()
    if final_data:
        filename = 'player_stats_2026.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"\nTerminé ! Données sauvegardées dans '{filename}'.")
        print("Note : Importez ce fichier dans Firestore (collection 'lec-players') pour mettre à jour le site.")
    else:
        print("\nErreur critique : Aucune donnée générée.")