from fastapi import FastAPI
import requests

app = FastAPI()

SCRYFALL_API = "https://api.scryfall.com/cards/search"

@app.get("/")
def home():
    return {"message": "MTG Data API is live!"}

@app.get("/search/")
def search_scryfall(query: str):
    """Searches for Magic: The Gathering cards on Scryfall."""
    response = requests.get(SCRYFALL_API, params={"q": query})
    return response.json()

@app.get("/meta/")
def fetch_meta():
    """Scrapes MTGGoldfish for meta deck data (example)."""
    response = requests.get("https://www.mtggoldfish.com/metagame/pioneer")
    return {"status": "MTGGoldfish scraping not implemented yet"}
