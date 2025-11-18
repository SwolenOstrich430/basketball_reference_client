from bball_reference_client.dto.game_stats_dto import GameStatsDto

class BoxScoreDto():
    def __init__(
        self,
        team_1_identifier: str,
        team_2_identifier: str,
        team_1_stats: list[GameStatsDto],
        team_2_stats: list[GameStatsDto]
    ):
        self.team_1_identifier = team_1_identifier
        self.team_2_identifier = team_2_identifier
        self.team_1_stats = team_1_stats
        self.team_2_stats = team_2_stats