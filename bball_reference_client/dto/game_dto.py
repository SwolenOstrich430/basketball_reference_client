from datetime import datetime 

from bball_reference_client.dto.matchup_dto import MatchupDto

class GameDto():
    @classmethod
    def from_dict(cls, dict: dict):
        return cls(
            home_team_id=dict['home_team_id'],
            home_team_identifier=dict['home_team_identifier'],
            away_team_id=dict['away_team_id'],
            away_team_identifier=dict['away_team_identifier'],
            start_time=datetime.fromisoformat(dict['start_time'])
        )
    
    def __init__(
        self, 
        home_team_id: str,
        home_team_identifier: str, 
        away_team_id: str,
        away_team_identifier: str,
        start_time: datetime 
    ):
        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time)

        self.matchup = MatchupDto(
            home_team_id=home_team_id,
            home_team_identifier=home_team_identifier,
            away_team_id=away_team_id,
            away_team_identifier=away_team_identifier
        )
        self.start_time = start_time.isoformat()

    def to_dict(self) -> dict:
        return {
            "home_team_id": self.matchup.home_team_id,
            "home_team_identifier": self.matchup.home_team_identifier,
            "away_team_id": self.matchup.away_team_id,
            "away_team_identifier": self.matchup.away_team_identifier,
            "start_time": self.start_time
        }