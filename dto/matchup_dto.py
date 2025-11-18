class MatchupDto():
    def __init__(
        self, 
        home_team_name: str,
        home_team_identifier: str, 
        away_team_name: str,
        away_team_identifier: str
    ):
        self.home_team_name = home_team_name
        self.home_team_identifier = home_team_identifier
        self.away_team_name = away_team_name
        self.away_team_identifier = away_team_identifier