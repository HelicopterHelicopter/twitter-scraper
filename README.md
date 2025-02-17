# Twitter Brand Engagement Scraper

A Python-based tool to scrape and analyze Twitter/X engagement data for brands.

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Update Twitter credentials in `config.py`:
   - Replace the following fields with your own Twitter session data:
     - `authorization`
     - `cookie`
     - `x-csrf-token`
     - Other headers as needed

2. Configure brands in `brands.json`:
   - Add or modify brand entries following the format:
   ```json
   {
     "BrandName": {
       "handle": "@TwitterHandle",
       "is_scraped": false,
       "last_scraped": null,
       "tweets_scraped": 0,
       "is_indian": true/false
     }
   }
   ```

## Usage

1. Run the main scraper:
```bash
python main.py
```

The script will:
- Process each brand sequentially
- Scrape up to 100 tweets per brand
- Store tweets with engagement data in `tweets.json`
- Track scraping progress in `brands.json`

## Error Handling

Common error codes and solutions:
- 401: Unauthorized - Update Twitter credentials in `config.py`
- 429: Rate limit - Script will automatically retry with exponential backoff
- IndentationError: Check code formatting in `main.py`

## Analysis

Run the analysis script to generate insights:
```bash
python analyze_tweets.py
```

This will:
- Generate engagement statistics
- Create visualizations
- Output a comprehensive report

## Files

- `main.py`: Main scraping script
- `config.py`: Configuration and constants
- `brands.json`: Brand data and scraping status
- `analyze_tweets.py`: Analysis tools
- `test.py`: Credential testing utility
- `tweets.json`: Scraped data storage (gitignored)

## Note

Remember to:
1. Never commit `tweets.json` (contains scraped data)
2. Update credentials before running
3. Monitor rate limits and API responses 