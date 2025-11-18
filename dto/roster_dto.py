from bball_reference_client.dto.player_dto import PlayerDto

class RosterDto():
    def __init__(
        self, team_identifier: str, end_year: int,
        players: list[PlayerDto]
    ):
        self.team_identifier = team_identifier
        self.season_end_year = end_year
        self.season_start_year = end_year - 1
        self.players = players