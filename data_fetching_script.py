import requests
import time
import sqlite3
import random

# Function to fetch statistics for a given event ID
def fetch_statistics(event_id):
    url = f'https://api.sofascore.com/api/v1/event/{event_id}/statistics'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403:
        print(f"Failed to fetch statistics for event ID {event_id}. Forbidden: You may be rate-limited or unauthorized.")
        return None
    else:
        print(f"Failed to fetch statistics for event ID {event_id}. Status code: {response.status_code}")
        return None

# Function to extract specific statistics from the provided data
def extract_statistics(statistics_data, group_name, statistic_name):
    for group in statistics_data.get('statistics', []):
        if group['period'] == 'ALL':
            for subgroup in group['groups']:
                if subgroup['groupName'] == group_name:
                    for statistic in subgroup['statisticsItems']:
                        if statistic['name'] == statistic_name:
                            return statistic['home'], statistic['away']
    return 'N/A', 'N/A'

# API headers (excluding API key)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}

# Connect to SQLite database
conn = sqlite3.connect('tennis_stats.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS tennis_matches
             (event_id INTEGER, tournament TEXT, round TEXT, home_team TEXT, away_team TEXT, match_progress TEXT, 
             period TEXT, home_score TEXT, away_score TEXT, statistic_group TEXT, statistic_name TEXT, 
             home_stat TEXT, away_stat TEXT)''')
conn.commit()

# Run the loop continuously
while True:
    # Make the request to fetch live events
    response = requests.get('https://api.sofascore.com/api/v1/sport/tennis/events/live', headers=headers)

    # Check response status
    if response.status_code == 200:
        # Get JSON data if request is successful
        live = response.json()

        # Truncate existing data in the table
        c.execute("DELETE FROM tennis_matches")
        conn.commit()

        # Process and display the updated data
        for event in live['events']:
            event_id = event['id']
            print(f"Tournament: {event['tournament']['name']}")
            print(f"Round: {event['roundInfo']['name']}")
            print(f"Match: {event['homeTeam']['name']} vs {event['awayTeam']['name']}")
            print(f"Match Progress: {event['status']['description']} ({event['status']['type']})")
            if 'periods' in event:
                print("Periods:")
                for period_key, period_value in event['periods'].items():
                    try:
                        print(f"{period_value}: {event['homeScore'][period_key]} - {event['awayScore'][period_key]}")
                    except KeyError:
                        print(f"{period_value}: Not available yet")
            print(f"Match Progress: {event['status']['description']} ({event['status']['type']})")
            print()
            # Fetch and display statistics if available
            statistics = fetch_statistics(event_id)
            if statistics:
                print("Statistics:")
                statistics_mapping = {
                    "Service": ["Aces", "Double faults", "First serve", "Second serve", 
                                "First serve points", "Second serve points", "Service games played", "Break points saved"],
                    "Points": ["Total", "Service points won", "Receiver points won", "Max points in a row"],
                    "Games": ["Total", "Service games won", "Max games in a row"],
                    "Return": ["First serve return points", "Second serve return points", "Return games played", "Break points converted"]
                }
                for group, stats in statistics_mapping.items():
                    print(f"\n{group}:")
                    for stat_name in stats:
                        home_stat, away_stat = extract_statistics(statistics, group, stat_name)
                        print(f"{stat_name}: {home_stat} - {away_stat}")
                        # Insert data into SQLite database
                        c.execute("INSERT INTO tennis_matches VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                  ( event['tournament']['name'], event['roundInfo']['name'], event['homeTeam']['name'],
                                   event['awayTeam']['name'], event['status']['description'], 'ALL',
                                   event['homeScore']['current'], event['awayScore']['current'], group, stat_name,
                                   home_stat, away_stat))
                        conn.commit()
            else:
                print("Statistics: Not available")
            print()
        
        # Generate a random delay before fetching data again (e.g., between 10 and 30 seconds)
        random_delay = random.randint(1, 5)
        print(f"Waiting for {random_delay} seconds before fetching data again...")
        time.sleep(random_delay)
    
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")