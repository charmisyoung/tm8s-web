import requests
from typing import List, Tuple
from datetime import datetime

# 👇 RENAMED from FotMobAPI to TheSportsDBAPI
class TheSportsDBAPI:
    BASE_URL = "https://www.thesportsdb.com/api/v1/json/3"
    
    # Manual fixes for teams with broken API data
    MANUAL_BADGE_FIXES = {
        "Everton": "https://r2.thesportsdb.com/images/media/team/badge/eqayrf1523184794.png",
        "Fulham": "https://www.thesportsdb.com/images/media/team/badge/g105s01611616723.png" 
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "TM8S_App/1.0"})

    def _safe_get_year(self, date_string: str) -> int:
        if date_string and len(date_string) >= 4 and date_string[:4].isdigit():
            return int(date_string[:4])
        return 0

    def _fetch_team_badge(self, team_id: str) -> str:
        """Fallback: Fetch Team details directly."""
        if not team_id: return ""
        
        try:
            resp = self.session.get(f"{self.BASE_URL}/lookupteam.php", params={"id": team_id}, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                teams = data.get("teams") or []
                if teams:
                    t = teams[0]
                    # Anti-Arsenal Check
                    returned_id = str(t.get("idTeam"))
                    if returned_id == "133604" and str(team_id) != "133604":
                        return ""

                    return (t.get("strBadge") or 
                            t.get("strTeamBadge") or 
                            t.get("strTeamLogo") or 
                            "")
        except:
            pass
        return ""

    def _get_badge_url(self, team_id: str, provided_url: str, team_name: str) -> str:
        # 1. Check Manual Fixes
        if team_name:
            clean_name = team_name.strip()
            if clean_name in self.MANUAL_BADGE_FIXES:
                return self.MANUAL_BADGE_FIXES[clean_name]

        # 2. Use API URL if valid
        if provided_url: return provided_url
        
        # 3. Fallback to lookup
        if team_id and str(team_id).isdigit() and str(team_id) != "0":
            return self._fetch_team_badge(team_id)
        
        return ""

    def search_player(self, query: str) -> list:
        url = f"{self.BASE_URL}/searchplayers.php"
        params = {"p": query}
        try:
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                players = response.json().get("player", []) or []
                return [{"id": p["idPlayer"], "name": p["strPlayer"]} for p in players if p.get("strSport") == "Soccer"]
            return []
        except:
            return []

    def get_player_clubs(self, player_id: int) -> List[Tuple[str, int, int, str]]:
        history_url = f"{self.BASE_URL}/lookupformerteams.php"
        profile_url = f"{self.BASE_URL}/lookupplayer.php"
        params = {"id": player_id}
        
        all_clubs_tuples = []
        teams_seen = set()
        max_departure_year = 0
        birth_year = 0
        player_profile = None

        try:
            # 1. Fetch Profile
            prof_resp = self.session.get(profile_url, params=params, timeout=10)
            if prof_resp.status_code == 200:
                data = prof_resp.json()
                if data.get("players"):
                    player_profile = data["players"][0]
                    birth_year = self._safe_get_year(player_profile.get("dateBorn"))

            # 2. Fetch Former Teams
            hist_resp = self.session.get(history_url, params=params, timeout=10)
            if hist_resp.status_code == 200:
                data = hist_resp.json()
                former_teams = data.get("formerteams") or []
            
                for t in former_teams:
                    club_name = t.get("strFormerTeam")
                    start_year = self._safe_get_year(t.get("strJoined"))
                    end_year = self._safe_get_year(t.get("strDeparted"))
                    team_id = t.get("idFormerTeam")
                    
                    crest_url = self._get_badge_url(team_id, t.get("strBadge"), club_name)

                    if birth_year > 0 and start_year > 0:
                        if (start_year - birth_year) > 45: continue 

                    if club_name and start_year > 0:
                        final_end = end_year if end_year > 0 else 2025
                        if final_end >= start_year:
                            all_clubs_tuples.append((club_name, start_year, final_end, crest_url))
                            teams_seen.add(club_name)
                            if final_end > max_departure_year and final_end != 2025:
                                max_departure_year = final_end

            # 3. Process Current Team
            if player_profile:
                p = player_profile
                current_team = p.get("strTeam")
                status = p.get("strStatus")
                position = p.get("strPosition") or ""
                
                is_active = (status != "Retired" and "Manager" not in position)
                if "_Free Agent" in str(current_team): is_active = False

                if current_team and current_team != "_Retired" and is_active:
                    profile_start = self._safe_get_year(p.get("dateSigned"))
                    
                    if profile_start < max_departure_year: profile_start = max_departure_year
                    if profile_start == 0: profile_start = max_departure_year if max_departure_year > 0 else 2023

                    # Duplicate Check
                    is_duplicate = any(c[0] == current_team and c[1] == profile_start for c in all_clubs_tuples)
                    
                    if not is_duplicate:
                        team_id = p.get("idTeam")
                        api_badge = p.get("strTeamBadge") or p.get("strBadge")
                        current_crest = self._get_badge_url(team_id, api_badge, current_team)
                        all_clubs_tuples.append((current_team, profile_start, 2025, current_crest))

            return all_clubs_tuples

        except Exception as e:
            print(f"Error fetching clubs in API: {e}")
            return []