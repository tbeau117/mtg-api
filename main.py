from fastapi import FastAPI, Query
import requests
import urllib.parse

app = FastAPI()

SCRYFALL_SEARCH_URL = "https://api.scryfall.com/cards/search"

@app.get("/search-card")
def search_card(
    name: str = Query(None, description="Exact or partial name of the card"),
    colors: str = Query(None, description="Colors of the card (W, U, B, R, G, C for colorless)"),
    type_line: str = Query(None, description="Type of the card (Creature, Instant, Sorcery, etc.)"),
    set_code: str = Query(None, description="Set code (e.g., 'MID' for Midnight Hunt)"),
    power: str = Query(None, description="Creature power (e.g., '3', '>2', '<5')"),
    toughness: str = Query(None, description="Creature toughness (e.g., '3', '>2', '<5')")
):
    """
    Search for a Magic: The Gathering card with advanced filters.
    """
    query_parts = []

    if name:
        query_parts.append(f'name:"{name}"')
    if colors:
        query_parts.append(f'c:{colors}')
    if type_line:
        query_parts.append(f't:{type_line}')
    if set_code:
        query_parts.append(f's:{set_code}')
    if power:
        query_parts.append(f'power{power}')
    if toughness:
        query_parts.append(f'toughness{toughness}')
    
    query_string = " ".join(query_parts)
    encoded_query = urllib.parse.quote(query_string)

    response = requests.get(SCRYFALL_SEARCH_URL, params={"q": encoded_query})

    if response.status_code == 200:
        return response.json().get("data", [])
    return {"error": f"Scryfall API error {response.status_code}", "details": response.text}

@app.get("/search-keywords")
def search_keywords(
    keyword: str = Query(..., description="Keyword, mechanic, or theme"),
    colors: str = Query(None, description="Colors of the card (W, U, B, R, G, C for colorless)"),
    type_line: str = Query(None, description="Type of the card (Creature, Instant, Sorcery, etc.)")
):
    """
    Search for MTG cards based on mechanics, keywords, or strategy with optional filters.
    """
    query_parts = [f"o:{keyword}"]

    if colors:
        query_parts.append(f'c:{colors}')
    if type_line:
        query_parts.append(f't:{type_line}')
    
    query_string = " ".join(query_parts)
    encoded_query = urllib.parse.quote(query_string)

    response = requests.get(SCRYFALL_SEARCH_URL, params={"q": encoded_query})

    if response.status_code == 200:
        return response.json().get("data", [])
    return {"error": f"Scryfall API error {response.status_code}", "details": response.text}
