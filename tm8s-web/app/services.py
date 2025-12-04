from sqlmodel import Session, select
from datetime import datetime, timedelta
from .models import Player, CareerEntry
from .core.api import TheSportsDBAPI  # 👈 1. Updated Import


class PlayerService:
    def __init__(self, session: Session):
        self.session = session
        self.api = TheSportsDBAPI()  # 👈 2. Updated Class Instantiation
        self.CACHE_DURATION = timedelta(days=7)

    def get_player_data(self, player_name: str):
        # 1. Check Cache
        statement = select(Player).where(Player.name == player_name)
        player = self.session.exec(statement).first()

        if player and (datetime.utcnow() - player.last_updated) < self.CACHE_DURATION:
            print(f"✅ Cache Hit: Found {player.name} in database.")
            player.search_count += 1
            self.session.add(player)
            self.session.commit()
            return [(c.club_name, c.start_year, c.end_year, c.crest_url) for c in player.careers]

        print(f"🌍 Cache Miss: Fetching '{player_name}' from API...")
        return self._fetch_and_cache_player(player_name, player)

    def _fetch_and_cache_player(self, search_name: str, existing_player_by_name: Player = None):
        # A. Search API
        results = self.api.search_player(search_name)
        if not results:
            return []

        api_player_data = results[0]
        api_id_val = int(api_player_data['id'])  # Renamed var for clarity
        real_name = api_player_data['name']

        # B. Check DB for this ID
        # 3. 👇 Updated field name from 'fotmob_id' to 'api_id'
        statement = select(Player).where(Player.api_id == api_id_val)
        existing_player_by_id = self.session.exec(statement).first()

        if existing_player_by_id:
            print(f"   ↳ Found existing record for {real_name} (ID: {api_id_val}). Updating...")
            player = existing_player_by_id
            player.name = real_name
        elif existing_player_by_name:
            player = existing_player_by_name
            player.api_id = api_id_val  # 👈 Updated
            player.name = real_name
        else:
            print(f"   ↳ Creating new record for {real_name}")
            player = Player(name=real_name, api_id=api_id_val)  # 👈 Updated

        player.last_updated = datetime.utcnow()
        player.search_count += 1

        self.session.add(player)
        self.session.commit()
        self.session.refresh(player)

        # C. Get Career Details
        clubs_data = self.api.get_player_clubs(api_id_val) or []

        # D. Overwrite Career History
        for old_career in player.careers:
            self.session.delete(old_career)

        formatted_history = []

        for team in clubs_data:
            if isinstance(team, tuple) or isinstance(team, list):
                if len(team) == 4:
                    club_name, start_year, end_year, crest_url = team
                else:
                    club_name, start_year, end_year = team[:3]
                    crest_url = None
            else:
                continue

            career = CareerEntry(
                club_name=club_name,
                start_year=start_year,
                end_year=end_year,
                crest_url=crest_url,
                player_id=player.id
            )
            self.session.add(career)
            formatted_history.append((club_name, start_year, end_year, crest_url))

        self.session.commit()
        return formatted_history

    def search_players(self, query: str):
        raw_results = self.api.search_player(query)
        return [p['name'] for p in raw_results]