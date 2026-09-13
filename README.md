# Toronto Boutique Finder

Finds independent boutique/clothing stores in downtown Toronto and enriches each listing with contact info (phone, website), using the Serper API for both place lookup and website discovery.

## Why I built this
Practicing the kind of local business/market discovery and data-enrichment workflow useful for GTM, marketing, and analyst roles — combining a places search with a secondary lookup to fill in missing contact details, then exporting clean, structured data.

## How it works
1. Queries Serper's Places API for stores matching a search term (default: "boutique clothing store downtown Toronto")
2. For any store missing a website, runs a follow-up Serper search combining name + address and picks the most likely business site (filtering out Yelp, Facebook, Instagram, etc.)
3. Cleans tracking parameters off URLs
4. Exports everything to a CSV: name, address, phone, website, rating, review count, category

## How to run it
1. Get a free API key at serper.dev
2. Create a .env file with SERPER_API_KEY=your_key_here
3. Install dependencies: pip install requests python-dotenv
4. Run with defaults: python store_finder.py
   Or with a custom query: python store_finder.py "coffee shop downtown Toronto" --num 15 --out cafes.csv
5. Results are saved to a CSV file

## Known limitations
- Address precision varies. Google's Places data sometimes returns just "Toronto, ON" instead of a full street address.
- Website enrichment picks the top non-directory search result, so it's a best guess, not guaranteed to be the exact official site.

## Related projects
This is the second step in a small pipeline of tools:
1. [research-report-tool](https://github.com/ghazalmhr1-gif/research-report-tool) — topic-to-report research automation
2. **toronto-boutique-finder** (this repo) — finds and enriches local business leads
3. [boutique-lead-qualifier](https://github.com/ghazalmhr1-gif/boutique-lead-qualifier) — verifies and scores those leads for outreach readiness
