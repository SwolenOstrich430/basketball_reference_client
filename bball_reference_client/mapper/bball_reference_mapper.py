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
            raw_team['TEAM'],
            self.get_team_name_by_identifier(raw_team['TEAM'])
        )

    def get_roster_from_df(
        self, 
        team_identifier: str,
        season_end_year: int,
        raw_players: DataFrame
    ) -> RosterDto:
        return RosterDto(
            team_identifier, 
            season_end_year, 
            self.get_players_from_df(raw_players)
        )

    def get_players_from_df(self, raw_players: DataFrame) -> list[PlayerDto]:
        raw_players.columns = map(str.lower, raw_players.columns)

        return raw_players.apply(
            lambda row: PlayerDto(**row), axis=1
        ).tolist()

    def get_games_from_df(self, raw_schedule: DataFrame) -> list[GameDto]:
        team_map = {}
        games = []

        for _, row in raw_schedule.iterrows():
            if row['HOME'] not in team_map:
                team_map[row['HOME']] = self.get_team_identifier_from_name(row['HOME'])

            if row['VISITOR'] not in team_map:
                team_map[row['VISITOR']] = self.get_team_identifier_from_name(row['VISITOR'])

            games.append(GameDto(
                home_team_name=row['HOME'],
                home_team_identifier=team_map[row['HOME']],
                away_team_name=row['VISITOR'],
                away_team_identifier=team_map[row['VISITOR']],
                start_time=row['DATE']
            ))
            
        return games 
    
    def get_box_score_from_dict(self, raw_box_score: dict) -> BoxScoreDto:
        team_idents = list(raw_box_score.keys())
        
        assert(len(team_idents) == 2)
        assert isinstance(raw_box_score[team_idents[0]], DataFrame)
        assert isinstance(raw_box_score[team_idents[1]], DataFrame)

        game_stats_1 = raw_box_score[team_idents[0]].apply(
            lambda row: self.get_game_stats_from_series(row), axis=1
        ).tolist()

        game_stats_2 = raw_box_score[team_idents[1]].apply(
            lambda row: self.get_game_stats_from_series(row), axis=1
        ).tolist()
        
        return BoxScoreDto(
            team_1_identifier=team_idents[0], 
            team_2_identifier=team_idents[1], 
            team_1_stats=game_stats_1, 
            team_2_stats=game_stats_2
        )

    def get_game_stats_from_series(
        self, 
        raw_game_stats: Series
    ) -> GameStatsDto:
        dnp_filtered_stats = raw_game_stats.apply(
            lambda val: self._filter_dnp_values(val)
        )

        mp = dnp_filtered_stats['MP']
        if type(mp) == str and ":" in mp:
            mp = ".".join(dnp_filtered_stats['MP'].split(":"))

        return GameStatsDto(
            player=dnp_filtered_stats['PLAYER'],
            mp=mp,
            fgm_2p=int(dnp_filtered_stats['FG']) - int(dnp_filtered_stats['3P']),
            fga_2p=int(dnp_filtered_stats['FGA']) - int(dnp_filtered_stats['3PA']),
            fgm_3p=dnp_filtered_stats['3P'],
            fga_3p=dnp_filtered_stats['3PA'],
            ftm=dnp_filtered_stats['FT'],
            fta=dnp_filtered_stats['FTA'],
            orb=dnp_filtered_stats['ORB'],
            drb=dnp_filtered_stats['DRB'],
            ast=dnp_filtered_stats['AST'],
            stl=dnp_filtered_stats['STL'],
            blk=dnp_filtered_stats['BLK'],
            tov=dnp_filtered_stats['TOV'],
            pf=dnp_filtered_stats['PF'],
            plus_minus=dnp_filtered_stats['+/-']
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

    def _filter_dnp_values(self, val):
        new_val = val 
        
        if type(val) == str and val.lower() == 'did not play':
            new_val = 0 

        return new_val
    
    def _get_team_map(self) -> dict[str, str]:
        return self.team_map

    def _set_team_map(self):
        self.team_map = {
            value.lower(): key for key, value in TEAM_TO_TEAM_ABBR.items()
        }