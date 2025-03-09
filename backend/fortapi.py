from flask import Flask, request, jsonify, render_template
import asyncio
import aiohttp
import os
import nest_asyncio
from dotenv import load_dotenv  # Import dotenv

# Load environment variables from .env
load_dotenv()

# Use API key from .env
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY is not set in the .env file or environment variables.")

# Fix event loop issue in VS Code
nest_asyncio.apply()

# List of player usernames to fetch stats for
player_names = ["UhhMike"]

async def fetch_player_stats(session, player_name):
    """Fetch Fortnite BR stats for a given player using aiohttp."""
    url = "https://fortnite-api.com/v2/stats/br/v2"
    headers = {"Authorization": API_KEY}
    params = {"name": player_name, "timeWindow": "lifetime"}

    try:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return {player_name: data}
            else:
                return {player_name: f"Error: {response.status} - {await response.text()}"}
    except Exception as e:
        return {player_name: f"Error: {str(e)}"}

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_player_stats(session, player) for player in player_names]
        results = await asyncio.gather(*tasks)

        # Print results
        for res in results:
            print(res)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())


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
        return jsonify({"error": f"API error: {response.status_code}"})
    
    data = response.json()

    # Extract only the "overall" stats
    overall_stats = data["data"]["stats"]["all"]["overall"]
    filtered_data = {
        "username": data["data"]["account"]["name"],
        "deaths": overall_stats["deaths"],
        "kd": overall_stats["kd"],
        "kills": overall_stats["kills"],
        "killsPerMatch": overall_stats["killsPerMatch"],
        "killsPerMin": overall_stats["killsPerMin"],
        "matches": overall_stats["matches"],
        "minutesPlayed": overall_stats["minutesPlayed"],
        "score": overall_stats["score"],
        "scorePerMatch": overall_stats["scorePerMatch"],
        "scorePerMin": overall_stats["scorePerMin"],
        "winRate": overall_stats["winRate"],
        "wins": overall_stats["wins"]
    }

    return jsonify(filtered_data)

if __name__ == "__main__":
    app.run(debug=True)