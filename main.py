import requests
from fastapi import FastAPI, Query
import logging

app = FastAPI()

# Enable detailed logging
logging.basicConfig(level=logging.INFO)

@app.get("/")
def read_root():
    return {"message": "MTG Scryfall API is running!"}

@app.get("/search-card/")
def search_card(card_name: str = Query(..., title="Card Name", description="Enter the card name")):
    """Search for a Magic: The Gathering card on Scryfall."""
    
    if not card_name.strip():
        return {"error": "Missing card name"}

    # ✅ Log the received card name
    logging.info(f"🟢 Received request for: {card_name}")

    # ✅ Encode the card name properly
    encoded_card_name = requests.utils.quote(card_name)

    # ✅ Build the Scryfall API request
    scryfall_url = f"https://api.scryfall.com/cards/named?fuzzy={encoded_card_name}"
    
    # ✅ Log the full request URL
    logging.info(f"🔍 Requesting Scryfall: {scryfall_url}")

    try:
        response = requests.get(scryfall_url)
        
        # ✅ Log Scryfall response
        logging.info(f"📝 Scryfall Response Code: {response.status_code}")
        logging.info(f"📜 Scryfall Response: {response.text}")

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"Scryfall API error {response.status_code}",
                "details": response.text
            }

    except Exception as e:
        logging.error(f"❌ Error contacting Scryfall: {str(e)}")
        return {"error": "Internal server error", "details": str(e)}

