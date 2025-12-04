"""
Connection finder module for Tm8s
"""

from typing import Dict, List, Tuple, Any, Optional

class ConnectionFinder:
    """
    Finds connections for Tm8s

    Finds connection between two players based on clubs they played for in overlapping time periods
    """

    def find_player_connections(self, p1_clubs, p2_clubs):
        """
        Finds connections between two players based on their club histories
        :arg p1_clubs: List of (club, start_year, end_year) for player 1
        :arg p2_clubs: List of (club, start_year, end_year) for player 2
        """
        connections = []

        for p1_club, p1_start, p1_end, p1_crest in p1_clubs:
            for p2_club, p2_start, p2_end, p2_crest in p2_clubs:
                if p1_club == p2_club:
                    overlap_start = max(p1_start, p2_start)
                    overlap_end = min(p1_end, p2_end)

                    if overlap_start < overlap_end:
                        connections.append({
                            "club_name": p1_club,
                            "overlap_start": overlap_start,
                            "overlap_end": overlap_end,
                            "p1_period": f"{p1_start}-{p1_end}",
                            "p2_period": f"{p2_start}-{p2_end}",
                            "overlapped": True,
                            "crest_url": p1_crest,  # 👈 ADD THIS LINE
                        })

        return connections


    def calculate_overlap_years(self, overlap_start: int, overlap_end: int) -> int:
        return overlap_end - overlap_start


    def format_connection_result(self, connection: Dict, p1: str, p2: str) -> str:
        club = connection['club_name']
        overlap_start = connection['overlap_start']
        overlap_end = connection['overlap_end']
        p1_period = connection['p1_period']
        p2_period = connection['p2_period']

        result = f"{club}\n"
        result += f"✓ Played together: {overlap_start}-{overlap_end}\n"
        result += f"{p1} at club: {p1_period}\n"
        result += f"{p2} at club: {p2_period}\n"

        return result