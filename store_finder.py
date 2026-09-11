import os
import sys
import csv
import time
import argparse
import requests
from urllib.parse import urlsplit, urlunsplit
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SERPER_API_KEY")
HEADERS = {"X-API-KEY": API_KEY, "Content-Type": "application/json"}

def find_places(query, num_results=20):
    if not API_KEY:
        print("Error: SERPER_API_KEY not found. Check your .env file.")
        sys.exit(1)
    url = "https://google.serper.dev/places"
    payload = {"q": query, "gl": "ca", "num": num_results}
    try:
        response = requests.post(url, json=payload, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error contacting Serper API: {e}")
        sys.exit(1)
    return response.json().get("places", [])

def clean_url(url):
    if not url:
        return ""
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))

def find_website(name, address):
    url = "https://google.serper.dev/search"
    payload = {"q": f"{name} {address}", "gl": "ca", "num": 3}
    try:
        response = requests.post(url, json=payload, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return ""
    organic = response.json().get("organic", [])
    skip_domains = ["yelp.", "tripadvisor.", "facebook.", "instagram.", "google.", "mapquest."]
    for item in organic:
        link = item.get("link", "")
        if link and not any(d in link for d in skip_domains):
            return clean_url(link)
    return ""

def build_rows(places, enrich=True):
    rows = []
    for p in places:
        website = clean_url(p.get("website", ""))
        name = p.get("title", "")
        address = p.get("address", "")
        if enrich and not website:
            website = find_website(name, address)
            time.sleep(0.5)
        rows.append({
            "name": name,
            "address": address,
            "phone": p.get("phoneNumber", ""),
            "website": website,
            "rating": p.get("rating", ""),
            "reviews": p.get("ratingCount", ""),
            "category": p.get("category", ""),
        })
    return rows

def save_csv(rows, filename):
    fieldnames = ["name", "address", "phone", "website", "rating", "reviews", "category"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():
    parser = argparse.ArgumentParser(description="Find stores in an area and enrich with contact info.")
    parser.add_argument("query", nargs="?", default="boutique clothing store downtown Toronto", help="Search query")
    parser.add_argument("--num", type=int, default=20, help="Number of results to fetch (default: 20)")
    parser.add_argument("--out", default="stores.csv", help="Output CSV filename (default: stores.csv)")
    parser.add_argument("--no-enrich", action="store_true", help="Skip website enrichment lookup")
    args = parser.parse_args()

    places = find_places(args.query, num_results=args.num)
    if not places:
        print("No results found.")
        sys.exit(0)

    rows = build_rows(places, enrich=not args.no_enrich)
    save_csv(rows, args.out)
    print(f"Found {len(rows)} stores. Saved to {args.out}")

if __name__ == "__main__":
    main()
