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
    print(f"🔍 Found {len(results.get('organic_results', []))} listings.")
    listings = results.get("organic_results", [])
    for i, listing in enumerate(listings):
        title = listing.get("title", "No title")
        link = listing.get("link", "No link")
        print(f"{i + 1}. {title} - {link}")
    return listings

def decide_action(cars, budget=10000):
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

#if __name__ == "__main__":
#    city = input("Enter a city to search for used electric cars: ")
#    print(f"🔍 Searching for used electric cars in {city}...\n")
#    listings = query_cars(location=city)
#    decide_action(listings)

