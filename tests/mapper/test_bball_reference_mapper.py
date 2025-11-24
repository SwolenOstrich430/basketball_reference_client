import pandas as pd 
import pytest 
from datetime import datetime 

from bball_reference_client.constant.team import TEAM_TO_TEAM_ABBR
from bball_reference_client.dto.player_dto import PlayerDto
from bball_reference_client.dto.game_stats_dto import GameStatsDto
from bball_reference_client.dto.box_score_dto import BoxScoreDto
from bball_reference_client.mapper.bball_reference_mapper import BballReferenceMapper

GET_ROSTER_RESP_FILE = "./tests/data/get_roster_response.json"
GET_SCHEDULE_RESPONSE = "./tests/data/get_schedule_response.json"
GET_TEAMS_RESPONSE_FILE = "./tests/data/get_teams_response.json"
GET_BOX_SCORE_RESPONSE_FILE = "./tests/data/get_box_score_response.json"
TEST_TEAM_IDENTIFIER = "CHI"
class TestBballReferenceMapper():
    
    def setup_method(self):
        self.mapper = BballReferenceMapper()
        self.team_name = TEST_TEAM_IDENTIFIER
        self.test_data = {
            "get_roster_response": pd.read_json(GET_ROSTER_RESP_FILE),
            "get_schedule_response": pd.read_json(GET_SCHEDULE_RESPONSE),
            "get_teams_response": pd.read_json(GET_TEAMS_RESPONSE_FILE),
            "get_box_score_response": {}
        }

        df1 = self.test_data["get_schedule_response"]
        self.date = df1.iloc[0]['gameDateTimeUTC']
        self.home_team = df1.iloc[0]['homeTeam_teamTricode'].upper()
        self.away_team = df1.iloc[0]['awayTeam_teamTricode'].upper()
        self.home_team_identifier = self.home_team
        self.away_team_identifier = self.away_team

        self.test_data["get_box_score_response"] = pd.read_json(GET_BOX_SCORE_RESPONSE_FILE)
        self.game_stats_series = self.test_data["get_box_score_response"].iloc[0]

    def test_get_team_from_df_returns_a_team_dto_when_given_valid_df(
        self
    ):
        assert len(self.test_data['get_teams_response']) == 30
        
        for _, row in self.test_data['get_teams_response'].iterrows():
            team = self.mapper.get_team_from_df(row)
            assert team.name.lower() == row['full_name'].lower()
            assert team.identifier.lower() == row['abbreviation'].lower()
            assert team.external_id == row['id']
    
    def test_get_roster_from_df_returns_a_roster_dto_given_valid_df(self):
        df = self.test_data['get_roster_response']
        year = datetime.now().year 

        roster = self.mapper.get_roster_from_df(
            self.team_name,
            year,
            df 
        )

        assert(roster.season_end_year == year + 1)
        assert(roster.season_start_year == year)
        assert(roster.team_identifier == self.team_name)
        self._assert_players_equal_df(roster.players, df)

    def test_get_players_from_df_returns_a_list_of_player_dtos(self):
        df = self.test_data['get_roster_response']
        players = self.mapper.get_players_from_df(df)

        self._assert_players_equal_df(players, df)

    def test_get_game_stats_from_series_returns_a_game_stats_dto(self):
        game_stats = self.mapper.get_game_stats_from_series(
            self.game_stats_series
        )

        assert isinstance(game_stats, GameStatsDto)


    def test_get_game_stats_raw_converts_string_version_of_mp_to_float(self):
        game_stats = self.mapper.get_game_stats_from_series(
            self.game_stats_series
        )

        assert isinstance(game_stats, GameStatsDto) 

    def test_game_stats_raw_maps_external_vals_to_internval_versions(self):
        game_stats = self.mapper.get_game_stats_from_series(
            self.game_stats_series
        )

        assert game_stats.fgm_2p == (
            int(self.game_stats_series['fieldGoalsMade']) - int(self.game_stats_series['threePointersMade'])
        )
        game_stats.fgm_2p is not None
        assert game_stats.fga_2p == (
            int(self.game_stats_series['fieldGoalsAttempted']) - int(self.game_stats_series['threePointersAttempted'])
        )
        assert game_stats.fga_2p is not None
        assert game_stats.ftm == int(self.game_stats_series['freeThrowsMade'])
        assert game_stats.ftm is not None
        assert game_stats.fta == int(self.game_stats_series['freeThrowsAttempted'])
        assert game_stats.fta is not None
        assert game_stats.orb == int(self.game_stats_series['reboundsOffensive'])
        assert game_stats.orb is not None
        assert game_stats.drb == int(self.game_stats_series['reboundsDefensive'])
        assert game_stats.drb is not None
        assert game_stats.ast == int(self.game_stats_series['assists'])
        assert game_stats.ast is not None
        assert game_stats.stl == int(self.game_stats_series['steals'])
        assert game_stats.stl is not None
        assert game_stats.blk == int(self.game_stats_series['blocks'])
        assert game_stats.blk is not None
        assert game_stats.tov == int(self.game_stats_series['turnovers'])
        assert game_stats.tov is not None
        assert game_stats.pf == int(self.game_stats_series['foulsPersonal'])
        assert game_stats.pf is not None
        assert game_stats.plus_minus == self.game_stats_series['plusMinusPoints']
        assert game_stats.plus_minus is not None

    def _assert_players_equal_df(
            self,
            players: list[PlayerDto], 
            df: pd.DataFrame
        ):
            assert(len(players) == len(df))

            for i in range(len(players)):
                assert players[i].first_name == df.iloc[i]['player'].split(" ")[0]
                assert players[i].last_name == df.iloc[i]['player'].split(" ")[1]
                assert players[i].number == df.iloc[i]['num']
                assert players[i].position == df.iloc[i]['position']
                assert players[i].height == df.iloc[i]['height']
                assert players[i].weight == df.iloc[i]['weight']
                assert players[i].birth_date == df.iloc[i]['birth_date']
                assert players[i].college == df.iloc[i]['school']
                assert players[i].external_id == df.iloc[i]['player_id']
