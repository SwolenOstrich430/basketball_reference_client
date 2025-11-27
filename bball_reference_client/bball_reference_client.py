from types import ModuleType
from datetime import datetime

import pandas as pd 
from nba_api.stats.static import teams
from nba_api.stats.endpoints.commonteamroster import CommonTeamRoster
from nba_api.stats.endpoints.scheduleleaguev2 import ScheduleLeagueV2
from nba_api.stats.endpoints.boxscoretraditionalv3 import BoxScoreTraditionalV3

from bball_reference_client.mapper.bball_reference_mapper import BballReferenceMapper
from bball_reference_client.dto.roster_dto import RosterDto
from bball_reference_client.dto.box_score_dto import BoxScoreDto
from bball_reference_client.dto.game_dto import GameDto

# TODO: datetime.now().year into util method for get current season
# TODO: separate out teams, roster, etc. into their own data providers
# TODO: add and apply validator methods for team and season end year
class BballReferenceClient():
    
    def __init__(self):
        self._set_teams_client(teams)
        self.mapper = BballReferenceMapper()

    # get player information:
    #   * for a specific team 
    #   * for the entire league for a year 
    #   * for all players over a specific period of time
    
    def get_teams(self) -> list:
        raw_teams = self.get_teams_raw()

        return list(raw_teams.apply(
            lambda row: self.mapper.get_team_from_df(row), axis=1
        ))
    
    def get_teams_raw(self) -> pd.DataFrame:
        return pd.DataFrame(
            self._get_teams_client().get_teams()
        )
        
    def get_roster(self, team: str, year: int = None) -> RosterDto:
        return self.mapper.get_roster_from_df(
            team,
            year,
            self.get_roster_raw(team, year)
        )

    def get_roster_raw(
        self, 
        team_identifier: str, 
        season_start_year: int = None
    ) -> pd.DataFrame:
        season = self._get_formatted_season(season_start_year)
        team_id = self._get_team_id_from_identifier(team_identifier)

        raw_roster = CommonTeamRoster(
            team_id=team_id, season=season
        )
        
        return raw_roster.common_team_roster.get_data_frame()
    
    def get_season_schedule(self, year: int = None):
        return self.mapper.get_games_from_df(
            self.get_schedule_raw(year)
        )
    
    def get_game_from_dict(self, dict: dict) -> GameDto:
        return self.mapper.get_game_from_dict(dict)

    # TODO: currently, this won't include playoffs
    # TODO: also won't include advanced stats  
    def get_schedule_raw(
        self, 
        season_start_year: int = None
    ) -> pd.DataFrame:
        season = self._get_formatted_season(season_start_year)
        season_response = ScheduleLeagueV2(season=season)
        return season_response.season_games.get_data_frame()
    
    def get_box_score(
      self, 
      game_id: int     
    ) -> BoxScoreDto:
        return self.mapper.get_box_score_from_df(
            self.get_box_score_raw(game_id)
        )
        
    def get_box_score_raw(
        self,
        game_id: int
    ) -> pd.DataFrame:
        box_score = BoxScoreTraditionalV3(
            game_id=str(game_id).rjust(10, '0')
        )

        assert(box_score.nba_response._status_code == 200)
        
        return pd.DataFrame(
            box_score.player_stats.get_data_frame()
        )

    # private 
    
    def _get_team_id_from_identifier(self, team_identifier: str) -> int:
        teams = self.get_teams()
        
        for team in teams: 
            if team.identifier.lower() == team_identifier.lower():
                return team.external_id

        raise ValueError(
            f"No matching team found for identifier: {team_identifier}"
        )

    def _get_formatted_season(self, start_year: int = None) -> str:
        if start_year is None:
            start_year = datetime.now().year
        
        end_year = str(start_year)[-2:]
        return f"{start_year}-{end_year}"
    
    def _get_teams_client(self) -> ModuleType:
        return self.teams_client

    def _set_teams_client(self, teams) -> None:
        assert(hasattr(teams, ("get_teams")))
        self.teams_client = teams