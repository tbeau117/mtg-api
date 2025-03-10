from fastapi import FastAPI, Query
import requests

# Initialize FastAPI
app = FastAPI()

# Scryfall API URL
SCRYFALL_API_URL = "https://api.scryfall.com/cards/named"

@app.get("/")
def root():
    return {"message": "Welcome to the MTG Scryfall API Proxy!"}

@app.get("/search-card")
def search_card(name: str = Query(..., description="Name of the MTG card")):
    """
    Searches for an MTG card by name using Scryfall's API.
    Uses fuzzy search to find cards even if the name isn't exact.
    """
    response = requests.get(SCRYFALL_API_URL, params={"fuzzy": name})

    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": f"Scryfall API error {response.status_code}",
            "details": response.text
        }


