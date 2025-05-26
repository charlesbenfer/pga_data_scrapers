import requests
import pandas as pd

from numpy import nan
from datetime import datetime
from requests_html import HTMLSession

# ─── CONFIG ───────────────────────────────────────────────────────────────────

API_URL = "https://orchestrator.pgatour.com/graphql"
API_KEY = "Insert your API Key here"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

GRAPHQL_QUERY = """
query StatDetails($tourCode: TourCode!, $statId: String!, $year: Int, $eventQuery: StatDetailEventQuery) {
  statDetails(
    tourCode: $tourCode
    statId: $statId
    year: $year
    eventQuery: $eventQuery
  ) {
    # metadata you can use to drive your dropdowns
    tournamentPills { tournamentId displayName }  
    yearPills       { year displaySeason    }

    # the actual table rows
    rows {
      __typename
      ... on StatDetailsPlayer {
        rank
        playerId
        playerName
        country
        stats { statName statValue }
      }
      # there’s also a “TourAvg” row you can handle if you like
    }
  }
}
"""

# ─── FUNCTION TO FETCH AND FLATTEN ──────────────────────────────────────────

def fetch_stat_details(stat_id: str,
                       year: int = None,
                       tournament_id: str = None) -> pd.DataFrame:
    """
    Fetches the stat-detail table for a given stat_id,
    optional season (year), and optional tournament_id
    
    If tournament_id is None, you get the season‐to‐date numbers.
    """
    variables = {
        "tourCode": "R", 
        "statId": stat_id,
        "year": year,
        "eventQuery": None if tournament_id is None else {"tournamentId": tournament_id}
    }

    payload = {
        "operationName": "StatDetails",
        "query": GRAPHQL_QUERY,
        "variables": variables
    }

    resp = requests.post(API_URL, json=payload, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()["data"]["statDetails"]

    raw_rows = data["rows"]

    records = []
    for row in raw_rows:
        if row["__typename"] != "StatDetailsPlayer":
            continue
        rec = {
            "rank": row["rank"],
            "playerId": row["playerId"],
            "playerName": row["playerName"],
        }
        for stat in row.get("stats", []):
            rec[stat["statName"]] = stat["statValue"]
        records.append(rec)

    df = pd.DataFrame(records)
    return df
