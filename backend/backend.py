from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

@app.route("/search")
def search_user():
    username = request.args.get("username")

    if not username:
        return jsonify({"error": "No username provided"}), 400

    url = "https://fortnite-api.com/v2/stats/br/v2"
    headers = {"Authorization": API_KEY}
    params = {"name": username, "timeWindow": "lifetime"}

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        return jsonify({"error": f"API error: {response.status_code}"}), response.status_code
    
    data = response.json()

    # Extract different stat types
    stats_all = data["data"]["stats"]["all"]

    # Get stats for overall, solos, and quads
    def extract_stats(stats):
        return {
            "deaths": stats.get("deaths", 0),
            "kd": stats.get("kd", 0),
            "kills": stats.get("kills", 0),
            "killsPerMatch": stats.get("killsPerMatch", 0),
            "killsPerMin": stats.get("killsPerMin", 0),
            "matches": stats.get("matches", 0),
            "minutesPlayed": stats.get("minutesPlayed", 0),
            "score": stats.get("score", 0),
            "scorePerMatch": stats.get("scorePerMatch", 0),
            "scorePerMin": stats.get("scorePerMin", 0),
            "winRate": stats.get("winRate", 0),
            "wins": stats.get("wins", 0)
        }

    # Organize the extracted data
    filtered_data = {
        "username": data["data"]["account"]["name"],
        "overall": extract_stats(stats_all["overall"]),
        "solos": extract_stats(stats_all["solo"]),
        "quads": extract_stats(stats_all["squad"])
    }

    return jsonify(filtered_data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True)
#python backend.py
