import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

def extract_price(text):
    match = re.search(r"\$(\d{1,3}(?:,\d{3})*)", text)
    if match:
        return int(match.group(1).replace(",", ""))
    return None

def query_cars(keywords="used electric car", location="Maryland"):
    params = {
        "engine": "google",
        "q": f"{keywords} for sale in {location}",
        "api_key": os.getenv("SERPAPI_API_KEY"),
    }
    response = requests.get("https://serpapi.com/search", params=params)
    results = response.json()
    listings = results.get("organic_results", [])
    return listings

def decide_action(cars, budget=20000):
    suitable = []
    for car in cars:
        title = car.get("title", "")
        price = extract_price(title)
        if price and price <= budget and "electric" in title.lower():
            suitable.append((title, price))

    if suitable:
        print("\nRecommended cars:")
        for title, price in suitable:
            print(f"- {title} (${price})")
        print("\n✅ ACTION: Recommend purchase.")
    else:
        print("\nNo suitable electric cars under budget found.")
        print("⏳ ACTION: Wait or expand budget.")

if __name__ == "__main__":
    print("🔍 Searching for used electric cars...\n")
    listings = query_cars()
    decide_action(listings)

