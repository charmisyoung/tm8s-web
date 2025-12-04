import requests
import json

TEAM_ID = "133704"
BASE_URL = "https://www.thesportsdb.com/api/v1/json/3"


def check_team_lookup():
    print(f"Checking Team Lookup for ID: {TEAM_ID}...")
    url = f"{BASE_URL}/lookupteam.php"
    resp = requests.get(url, params={"id": TEAM_ID})

    if resp.status_code != 200:
        print("❌ API Request Failed")
        return

    data = resp.json()
    teams = data.get("teams")

    if not teams:
        print("❌ No team found.")
        return

    team = teams[0]
    print("\n--- Keys found in Team Lookup ---")
    print(f"strTeamBadge: {team.get('strTeamBadge')}")  # This is likely None or missing
    print(f"strBadge:     {team.get('strBadge')}")  # This likely has the URL
    print(f"strTeamLogo:  {team.get('strTeamLogo')}")


if __name__ == "__main__":
    check_team_lookup()