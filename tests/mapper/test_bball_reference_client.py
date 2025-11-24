from datetime import datetime 
import pandas as pd 

from nba_api.stats.static import teams as official_teams
from nba_api.stats.endpoints.commonteamroster import CommonTeamRoster
from nba_api.stats.endpoints.scheduleleaguev2 import ScheduleLeagueV2
from nba_api.stats.endpoints.boxscoretraditionalv3 import BoxScoreTraditionalV3

from bball_reference_client.constant.team import TEAM_TO_TEAM_ABBR
from bball_reference_client.dto.team_dto import TeamDto
from bball_reference_client.dto.roster_dto import RosterDto
from bball_reference_client.bball_reference_client import BballReferenceClient
from bball_reference_client.mapper.bball_reference_mapper import BballReferenceMapper
from bball_reference_client.dto.game_dto import GameDto
from bball_reference_client.dto.box_score_dto import BoxScoreDto

GET_ROSTER_RESP_FILE = "./tests/data/get_roster_response.json"
GET_SCHEDULE_RESPONSE = "./tests/data/get_schedule_response.json"
GET_BOX_SCORE_RESPONSE = "./tests/data/get_box_score_response.json"
GET_TEAMS_RESPONSE_FILE = "./tests/data/get_teams_response.json"
TEST_TEAM_IDENTIFIER = "CHI"
class TestBballReferenceClient():

    def refresh_test_data(self):
        teams_df = pd.DataFrame(official_teams.get_teams())
        teams_df.to_json(GET_TEAMS_RESPONSE_FILE)
        
        roster_df = CommonTeamRoster(team_id=teams_df.iloc[0]['id'], season=self.season)
        roster_df = roster_df.common_team_roster.get_data_frame()
        roster_df.to_json(GET_ROSTER_RESP_FILE, indent=4) 

        season_schedule = ScheduleLeagueV2(season=self.season).season_games.get_data_frame()
        season_schedule.to_json(GET_SCHEDULE_RESPONSE, indent=4)

        self.game_id = season_schedule.iloc[0]['gameId']
        assert int(self.game_id) > 0

        box_score = BoxScoreTraditionalV3(game_id=self.game_id)
        box_score_df = box_score.player_stats.get_data_frame()
        box_score_df.to_json(GET_BOX_SCORE_RESPONSE, indent=4)
        

    def setup_method(self):
        self.season = "2024-25"

        # self.refresh_test_data()

        self.client =  BballReferenceClient()
        self.team_name = "CHI"
        self.test_data = {
            "get_roster_response": pd.read_json(GET_ROSTER_RESP_FILE),
            "get_schedule_response": pd.read_json(GET_SCHEDULE_RESPONSE),
            "get_teams_response": pd.read_json(GET_TEAMS_RESPONSE_FILE),
            "get_box_score_response": pd.read_json(GET_BOX_SCORE_RESPONSE)
        }

        self.game_id = self.test_data['get_schedule_response'].iloc[0]['gameId']
        assert int(self.game_id) > 0

    def test_get_teams_returns_a_list_of_bball_ref_team_dto(self):
        teams = self.client.get_teams()

        assert (len(teams) > 0)

        for team in teams:
            assert isinstance(team, TeamDto)

    def test_get_teams_raw_returns_teams_for_the_current_year_if_year_is_null(self, mocker):
        ret_val = self.client.get_teams_raw()
        assert isinstance(ret_val, pd.DataFrame)

    def test_get_roster_returns_a_roster_dto(self, mocker):
        mocked_method = mocker.patch.object(
            self.client,
            'get_roster_raw',
            return_value=self.test_data['get_roster_response']
        )

        expected_roster = self.client.get_roster(
            self.team_name, 
            datetime.now().year
        )

        assert isinstance(expected_roster, RosterDto)
        mocked_method.assert_called_with(
            self.team_name, 
            datetime.now().year
        )
        
    def test_get_roster_raw_returns_a_data_frame(self, mocker): 
        df = self.client.get_roster_raw(self.team_name)

        assert(len(df) > 0)
        assert isinstance(df, pd.DataFrame)

    def test_get_season_returns_a_list_of_game_dtos(self, mocker):
        df = self.test_data['get_schedule_response']

        mocker.patch.object(
            self.client,
            'get_schedule_raw',
            return_value=df
        )

        game_dtos = self.client.get_season_schedule(self.season[0:4])

        assert(len(game_dtos) == len(df))

        for i in range(len(game_dtos)):
            assert(game_dtos[i].matchup.home_team_id == df.iloc[i]['homeTeam_teamId'])
            assert(game_dtos[i].matchup.home_team_identifier == df.iloc[i]['homeTeam_teamTricode'])
            assert(game_dtos[i].matchup.away_team_id == df.iloc[i]['awayTeam_teamId'])
            assert(game_dtos[i].matchup.away_team_identifier == df.iloc[i]['awayTeam_teamTricode'])
            assert(game_dtos[i].start_time == df.iloc[i]['gameDateTimeUTC'])
            
    def test_get_season_raw_returns_a_data_frame(self, mocker):
        df = self.client.get_schedule_raw()

        assert isinstance(df, pd.DataFrame)
        # assert df.equals(self.test_data['get_schedule_response'])

    def test_get_box_score_returns_a_box_score_dto(self, mocker):
        box_score = self.client.get_box_score(self.game_id)
        assert isinstance(box_score, BoxScoreDto)

    def test_get_box_score_raw_returns_a_data_frame(
        self, 
        mocker
    ):
        df = self.client.get_box_score_raw(self.game_id)
        assert isinstance(df, pd.DataFrame)