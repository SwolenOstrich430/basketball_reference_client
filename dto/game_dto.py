from datetime import datetime 

from bball_reference_client.dto.matchup_dto import MatchupDto

class GameDto():
    def __init__(
        self, 
        home_team_name: str,
        home_team_identifier: str, 
        away_team_name: str,
        away_team_identifier: str,
        start_time: datetime 
    ):
        self.matchup = MatchupDto(
            home_team_name=home_team_name,
            home_team_identifier=home_team_identifier,
            away_team_name=away_team_name,
            away_team_identifier=away_team_identifier
        )
        self.start_time = start_time  