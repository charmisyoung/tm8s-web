from typing import Dict, List, Tuple, Any, Optional

class ConnectionFinder:
    """
    Finds connections for Tm8s
    """

    def find_player_connections(self, p1_clubs, p2_clubs):
        """
        Finds connections between two players based on their club histories.
        Expects tuples of: (club_name, start_year, end_year, crest_url)
        """
        connections = []

        # 👇 FIX: Correctly unpack all 4 items from the list of tuples
        for p1_club, p1_start, p1_end, p1_crest in p1_clubs:
            for p2_club, p2_start, p2_end, p2_crest in p2_clubs:
                
                # Check if club names match
                if p1_club == p2_club:
                    # Calculate the overlap period
                    overlap_start = max(p1_start, p2_start)
                    overlap_end = min(p1_end, p2_end)

                    # Valid overlap logic: Start must be BEFORE End
                    # We use < instead of <= to avoid single-year edge cases if needed, 
                    # but for full seasons < is standard. 
                    # If you want to catch "Joined Jan, Left Feb" same year, use <=
                    if overlap_start <= overlap_end: 
                        connections.append({
                            "club_name": p1_club,
                            "overlap_start": overlap_start,
                            "overlap_end": overlap_end,
                            "p1_period": f"{p1_start}-{p1_end}",
                            "p2_period": f"{p2_start}-{p2_end}",
                            "overlapped": True,
                            "crest_url": p1_crest # Pass the crest through to the result
                        })

        return connections