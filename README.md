# pga_data_scrapers
This repo was created and works as of May 25, 2025. 

This repo contains two scripts, one that scrapes individual year end statistics for a defined range, and one that scrapes all tournament leaderboards for a defined range.

To 

If you are unsure how to find your API key, follow these steps:
1) In Chrome or Firefox: right-click anywhere on the PGA Tour stats (https://www.pgatour.com/stats) page and choose Inspect, then switch to the Network tab.
2) Reload the page then in the Network list, type “graphql” to find the POST calls that drive the statDetails endpoint.
3) Click on one of the graphql entries. Under Headers ▶ Request Headers, look for the line: x-api-key: da2-XXXXXXXXXXXXXXXXXXXXXXXX
4) Copy and paste the da2-XXXXXXXXXXXXXXXXXXXXXXXX into the script.

Example usage for the statistic scraper could be as follows:

```{python}

from statistic_scraping import fetch_stat_details

#Example Usage for single statistic scraping

STAT_ID = "102"             # Scoring Average (codes can be found on the pga website above)
YEAR    = 2024              # seasonal stats
TOURNEY = None              # set to string to filter to a single event

# fetch the DataFrame
df = fetch_stat_details(STAT_ID, year=YEAR, tournament_id=TOURNEY)

print(f"\nTop 5 for stat {STAT_ID} / year {YEAR} / tourney {TOURNEY}:")
print(df.head())
```

Or for a dictionary of statistics and their codes

```{python}

stats = {
    #Strokes Gained
    'SG: Total': '02675', 
    'SG: Off the Tee' : '02567',
    'SG: Tee to Green' : '02674',
    'SG: Approach the Green' : '02568', 
    'SG: Around the Green' : '02569'}

# ─── choose your range of years ─────────────────────────────────────────
YEARS = range(2015, 2025) 

stat_dfs = {}

for year in YEARS:
    print(f"Fetching stats for {year} …")
    stat_dfs[year] = {}
    for stat_name, stat_code in stats.items():
        df = fetch_stat_details(stat_code,
                                year=year,
                                tournament_id=None)
        df['Year'] = year
        stat_dfs[year][stat_name] = df
    print(f"{year} complete")

```

From here, specific statistics for specific years can be subset as follows:

```{python}
#2024 SG Around the green
stat_dfs[2024]["SG: Around the Green"].sort_values(by='Measured Rounds',ascending = False).head()

```



The 'tournament_results_scraping' script is run in the command line, and is customized to fit your needs in the code itself. This script finds the full leaderboards for all of the tour events in a defined time period. Given the nature of the code, this takes some time to run on large time intervals. The data set spit out is saved to the path 'data/espn_full_leaderboards_2015_2025.csv' if nothing is changed, but change this to whatever name you'd like, or 

