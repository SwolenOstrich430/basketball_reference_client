class MatchupDto():
    def __init__(
        self, 
        home_team_id: str,
        home_team_identifier: str, 
        away_team_id: str,
        away_team_identifier: str
    ):
        self.home_team_id = home_team_id
        self.home_team_identifier = home_team_identifier
        self.away_team_id = away_team_id
        self.away_team_identifier = away_team_identifier