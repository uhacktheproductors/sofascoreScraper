from curl_cffi import requests
import json
import time




# --- Configuration for Brazilian Brasileirão Série A ---
TOURNAMENT_ID = "325"
TARGET_SEASON_YEAR = "2026"  # Brazil uses a single calendar year

HEADERS = {
    "Accept": "*/*",
    "Origin": "https://www.sofascore.com",
    "Referer": "https://www.sofascore.com/tournament/football/brazil/brasileirao-serie-a/325"
}


def get_json(url):
    response = requests.get(url, headers=HEADERS, impersonate="chrome")
    if response.status_code == 200:
        return response.json()
    return None


def get_ids_by_round():
    # 1. Get Season ID
    seasons_url = f"https://api.sofascore.com/api/v1/unique-tournament/{TOURNAMENT_ID}/seasons"
    seasons_data = get_json(seasons_url)

    season_id = next((s['id'] for s in seasons_data['seasons'] if s['year'] == TARGET_SEASON_YEAR), None)
    if not season_id:
        print("Season not found.")
        return

    # 2. Get all Rounds (e.g., Round 1, Round 2... Playoff Round 1...)
    rounds_url = f"https://api.sofascore.com/api/v1/unique-tournament/{TOURNAMENT_ID}/season/{season_id}/rounds"
    rounds_data = get_json(rounds_url)

    if not rounds_data or 'rounds' not in rounds_data:
        print("Could not find rounds.")
        return

    all_match_ids = []
    print(f"Found {len(rounds_data['rounds'])} rounds. Starting deep crawl...")

    # 3. Loop through every round to get matches
    for r in rounds_data['rounds']:
        round_num = r['round']
        # The URL structure for a specific round
        url = f"https://api.sofascore.com/api/v1/unique-tournament/{TOURNAMENT_ID}/season/{season_id}/events/round/{round_num}"
        data = get_json(url)

        if data and 'events' in data:
            for event in data['events']:
                all_match_ids.append(event['id'])
            print(f"Collected Round {round_num}...")

        time.sleep(1)  # Slow down to stay under the radar

    # 4. Save the full list
    if all_match_ids:
        # Remove duplicates just in case
        unique_ids = list(set(all_match_ids))
        with open("argentina.txt", "w") as f:
            f.write(json.dumps(unique_ids))
        print(f"\nSuccess! Total Unique Match IDs found: {len(unique_ids)}")
        print("IDs saved to 'africadesud.txt'")
    else:
        print("Still no matches found. The season might be archived differently.")


if __name__ == "__main__":
    get_ids_by_round()