from types import ModuleType
from datetime import datetime
from datetime import date

import pandas as pd 
from basketball_reference_scraper import teams
from basketball_reference_scraper import seasons
from basketball_reference_scraper import box_scores

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
        self._set_roster_client(teams)
        self._set_season_client(seasons)
        self._set_stats_client(box_scores)
        self.mapper = BballReferenceMapper()

    # get player information:
    #   * for a specific team 
    #   * for the entire league for a year 
    #   * for all players over a specific period of time
    
    def get_teams(self, year: int = None) -> list:
        raw_teams = self.get_teams_raw(year)

        return list(raw_teams.apply(
            lambda row: self.mapper.get_team_from_df(row), axis=1
        ))
    
    def get_teams_raw(self, year: int = None) -> pd.DataFrame:
        if year is None:
            year = datetime.now().year

        return self._get_teams_client().get_team_ratings(year) 
        
    def get_roster(self, team: str, year: int = None) -> RosterDto:
        if year is None:
            year = datetime.now().year

        return self.mapper.get_roster_from_df(
            team,
            year,
            self.get_roster_raw(team, year)
        )

    def get_roster_raw(self, team: str, year: int = None) -> pd.DataFrame:
        if year is None:
            year = datetime.now().year

        return self._get_roster_client().get_roster(
            team, 
            year
        )
    
    def get_season_schedule(self, year: int = None):
        return self.mapper.get_games_from_df(
            self.get_schedule_raw(year)
        )

    # TODO: currently, this won't include playoffs
    # TODO: also won't include advanced stats  
    def get_schedule_raw(
        self, 
        year: int = None
    ) -> pd.DataFrame:
        if year is None:
            year = datetime.now().year
        
        return self._get_season_client().get_schedule(year)
    
    def get_box_score(
      self, 
      game: GameDto     
    ) -> BoxScoreDto:
        return self.mapper.get_box_score_from_dict(
            self.get_box_score_raw(
                game.start_time,
                game.matchup.home_team_identifier,
                game.matchup.away_team_identifier
            )
        )
        
    def get_box_score_raw(
        self,
        date: date,
        home_team_identifier: str,
        away_team_identifier: str 
    ):
        return self._get_stats_client().get_box_scores(
            date, home_team_identifier, away_team_identifier
        )
    
    # private 
    
    def _get_teams_client(self) -> ModuleType:
        return self.teams_client

    def _set_teams_client(self, teams) -> None:
        assert(hasattr(teams, ("get_team_ratings")))
        self.teams_client = teams

    def _get_roster_client(self) -> ModuleType:
        return self.roster_client

    def _set_roster_client(self, roster_client) -> None:
        assert(hasattr(roster_client, ("get_roster")))
        self.roster_client = roster_client

    def _get_season_client(self) -> ModuleType:
        return self.season_client
    
    def _set_season_client(self, season_client) -> None:
        assert(hasattr(season_client, "get_schedule"))
        self.season_client = season_client

    def _get_stats_client(self) -> ModuleType:
        return self.stats_client
    
    def _set_stats_client(self, stats_client) -> None:
        assert(hasattr(stats_client, "get_box_scores"))
        self.stats_client = stats_client