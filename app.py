from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Function to fetch data from SQLite database
def fetch_data():
    conn = sqlite3.connect('tennis_stats.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tennis_matches")
    data = c.fetchall()
    conn.close()
    return data

# API endpoint to get all tennis match data
@app.route('/api/tennis/matches', methods=['GET'])
def get_tennis_matches():
    data = fetch_data()
    matches = []
    for row in data:
        match = {
            'tournament': row[0],
            'round': row[1],
            'home_team': row[2],
            'away_team': row[3],
            'match_progress': row[4],
            'period': row[5],
            'home_score': row[6],
            'away_score': row[7],
            'statistic_group': row[8],
            'statistic_name': row[9],
            'home_stat': row[10],
            'away_stat': row[11]
        }
        matches.append(match)
    return jsonify({'matches': matches})

# Route to render HTML template with tennis match data
@app.route('/tennis/matches', methods=['GET'])
def tennis_matches():
    data = fetch_data()
    return render_template('tennis_matches.html', matches=data)

if __name__ == '__main__':
    app.run(debug=True)
