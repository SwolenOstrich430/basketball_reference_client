from bball_reference_client.dto.game_stats_dto import GameStatsDto

class BoxScoreDto():
    def __init__(
        self,
        team_one_external_id: str,
        team_two_external_id: str,
        team_one_stats: list[GameStatsDto],
        team_two_stats: list[GameStatsDto]
    ):
        self.team_one_external_id = team_one_external_id
        self.team_two_external_id = team_two_external_id
        self.team_one_stats = team_one_stats
        self.team_two_stats = team_two_stats