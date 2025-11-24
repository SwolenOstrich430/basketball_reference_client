from pandas import DataFrame
from pandas import Series 
from bball_reference_client.constant.team import TEAM_TO_TEAM_ABBR
from bball_reference_client.dto.team_dto import TeamDto
from bball_reference_client.dto.roster_dto import RosterDto
from bball_reference_client.dto.player_dto import PlayerDto
from bball_reference_client.dto.game_dto import GameDto 
from bball_reference_client.dto.box_score_dto import BoxScoreDto 
from bball_reference_client.dto.game_stats_dto import GameStatsDto

class BballReferenceMapper:
    def __init__(self):
        self._set_team_map()

    def get_team_from_df(self, raw_team: DataFrame) -> TeamDto:
        return TeamDto(
            raw_team['abbreviation'],
            raw_team['full_name'],
            raw_team['id']
        )

    def get_roster_from_df(
        self, 
        team_identifier: str,
        season_start_year: int,
        raw_players: DataFrame
    ) -> RosterDto:
        return RosterDto(
            team_identifier, 
            season_start_year, 
            self.get_players_from_df(raw_players)
        )

    def get_players_from_df(self, raw_players: DataFrame) -> list[PlayerDto]:
        raw_players.columns = map(str.lower, raw_players.columns)

        return raw_players.apply(
            lambda row: PlayerDto(**row), axis=1
        ).tolist() 
    
    def get_box_score_from_df(self, raw_box_score: DataFrame) -> BoxScoreDto:
        dict = {}

        for _, row in raw_box_score.iterrows():
            game_stats = self.get_game_stats_from_series(row)
            
            if row['teamId'] not in dict:
                dict[row['teamId']] = []
                
            dict[row['teamId']].append(game_stats)

        # games can only take place between two teams
        assert len(dict) == 2
        team_one_id = list(dict.keys())[0]
        team_two_id = list(dict.keys())[1]

        return BoxScoreDto(
            team_one_external_id=team_one_id,
            team_two_external_id=team_two_id,
            team_one_stats=dict[team_one_id],
            team_two_stats=dict[team_two_id]
        )

    def get_game_stats_from_series(
        self, 
        raw_game_stats: Series
    ) -> GameStatsDto:
        return GameStatsDto(
            external_id=raw_game_stats['personId'],
            mp=raw_game_stats['minutes'],
            fgm_2p=int(raw_game_stats['fieldGoalsMade']) - int(raw_game_stats['threePointersMade']),
            fga_2p=int(raw_game_stats['fieldGoalsAttempted']) - int(raw_game_stats['threePointersAttempted']),
            fgm_3p=raw_game_stats['threePointersMade'],
            fga_3p=raw_game_stats['threePointersAttempted'],
            ftm=raw_game_stats['freeThrowsMade'],
            fta=raw_game_stats['freeThrowsAttempted'],
            orb=raw_game_stats['reboundsOffensive'],
            drb=raw_game_stats['reboundsDefensive'],
            ast=raw_game_stats['assists'],
            stl=raw_game_stats['steals'],
            blk=raw_game_stats['blocks'],
            tov=raw_game_stats['turnovers'],
            pf=raw_game_stats['foulsPersonal'],
            plus_minus=raw_game_stats['plusMinusPoints']
        )

    def get_team_name_by_identifier(self, identifier: str) -> str:
        if identifier is None:
            raise ValueError("Identifier cannot be None.")

        formatted_identifier = identifier.lower()

        if formatted_identifier not in self._get_team_map():
            raise ValueError(f"Team name: {identifier} not found.")

        return self._get_team_map()[formatted_identifier]
    
    # TODO: add unit tests
    def get_team_identifier_from_name(self, name: str) -> str:
        if name is None:
            raise ValueError("Name cannot be None.")

        formatted_name = name.lower()

        for key, value in self._get_team_map().items():
            if value.lower() == formatted_name:
                return key 
        
        raise ValueError(f"Team name: {name} not found.")
    
    def _get_team_map(self) -> dict[str, str]:
        return self.team_map

    def _set_team_map(self):
        self.team_map = {
            value.lower(): key for key, value in TEAM_TO_TEAM_ABBR.items()
        }