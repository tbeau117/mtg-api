from fastapi import FastAPI, Query
import requests

app = FastAPI()

SCRYFALL_SEARCH_URL = "https://api.scryfall.com/cards/search"

@app.get("/search-card")
def search_card(name: str = Query(..., description="Exact or partial name of the card")):
    """
    Search for a Magic: The Gathering card using Scryfall's API.
    """
    response = requests.get(SCRYFALL_SEARCH_URL, params={"q": name})
    if response.status_code == 200:
        return response.json().get("data", [])
    return {"error": f"Scryfall API error {response.status_code}"}
