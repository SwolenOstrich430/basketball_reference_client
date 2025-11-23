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
GET_BOX_SCORE_RESPONSE_HOME = "./tests/data/get_box_score_response_home.json"
GET_BOX_SCORE_RESPONSE_AWAY = "./tests/data/get_box_score_response_away.json"
GET_TEAMS_RESPONSE_FILE = "./tests/data/get_teams_response.json"
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
        self.date = df1.iloc[0]['DATE']
        self.home_team = df1.iloc[0]['HOME'].upper()
        self.away_team = df1.iloc[0]['VISITOR'].upper()
        self.home_team_identifier = TEAM_TO_TEAM_ABBR[self.home_team]
        self.away_team_identifier = TEAM_TO_TEAM_ABBR[self.away_team]

        self.test_data["get_box_score_response"][self.home_team_identifier] = pd.read_json(
            GET_BOX_SCORE_RESPONSE_HOME
        )
        self.test_data["get_box_score_response"][self.away_team_identifier] = pd.read_json(
            GET_BOX_SCORE_RESPONSE_AWAY
        )

        self.game_stats_series = self.test_data["get_box_score_response"][self.home_team_identifier].iloc[0]

        df = self.test_data["get_box_score_response"][self.home_team_identifier]
        self.dnp_stats = df[df['MP'] == 'Did Not Play'].iloc[0]
        assert(self.dnp_stats is not None)

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

        assert(roster.season_end_year == year)
        assert(roster.season_start_year == year - 1)
        assert(roster.team_identifier == self.team_name)
        self._assert_players_equal_df(roster.players, df)

    def test_get_players_from_df_returns_a_list_of_player_dtos(self):
        df = self.test_data['get_roster_response']
        players = self.mapper.get_players_from_df(df)

        self._assert_players_equal_df(players, df)

    def test_get_box_score_from_dict_returns_a_box_score_dto(self):
        box_score = self.mapper.get_box_score_from_dict(
            self.test_data['get_box_score_response']
        )

        assert isinstance(box_score, BoxScoreDto)
        assert isinstance(box_score.team_1_stats, list)
        assert isinstance(box_score.team_2_stats, list)

        for game_stats in box_score.team_1_stats:
            assert isinstance(game_stats, GameStatsDto)

        for game_stats in box_score.team_2_stats:
            assert isinstance(game_stats, GameStatsDto)

    def test_get_box_score_from_dict_throws_if_provided_dict_isnt_of_length_2(self):
        with pytest.raises(AssertionError) as exc_info:   
            self.mapper.get_box_score_from_dict(
                {}
            )

    def test_get_box_score_from_dict_throws_if_provided_dict_isnt_of_length_2(self):
        with pytest.raises(AssertionError) as exc_info:   
            self.mapper.get_box_score_from_dict(
                {
                    'one': [],
                    'two': pd.DataFrame()
                }
            )

    def test_get_box_score_from_dict_throws_if_dict_values_arent_data_frames(self):
        pass
    
    def test_get_game_stats_from_series_returns_a_game_stats_dto(self, mapper):
        game_stats = self.mapper.get_game_stats_from_series(
            self.game_stats_series
        )

        assert isinstance(game_stats, GameStatsDto)


    def test_get_game_stats_raw_converts_string_version_of_mp_to_float(self, mapper):
        game_stats = self.mapper.get_game_stats_from_series(
            self.game_stats_series
        )

        assert isinstance(game_stats, GameStatsDto) 

    def test_game_stats_raw_maps_external_vals_to_internval_versions(self):
        game_stats = self.mapper.get_game_stats_from_series(
            self.game_stats_series
        )

        assert game_stats.fgm_2p == (
            int(self.game_stats_series['FG']) - int(self.game_stats_series['3P'])
        )
        game_stats.fgm_2p is not None
        assert game_stats.fga_2p == (
            int(self.game_stats_series['FGA']) - int(self.game_stats_series['3PA'])
        )
        assert game_stats.fga_2p is not None
        assert game_stats.ftm == int(self.game_stats_series['FT'])
        assert game_stats.ftm is not None
        assert game_stats.fta == int(self.game_stats_series['FTA'])
        assert game_stats.fta is not None
        assert game_stats.orb == int(self.game_stats_series['ORB'])
        assert game_stats.orb is not None
        assert game_stats.drb == int(self.game_stats_series['DRB'])
        assert game_stats.drb is not None
        assert game_stats.ast == int(self.game_stats_series['AST'])
        assert game_stats.ast is not None
        assert game_stats.stl == int(self.game_stats_series['STL'])
        assert game_stats.stl is not None
        assert game_stats.blk == int(self.game_stats_series['BLK'])
        assert game_stats.blk is not None
        assert game_stats.tov == int(self.game_stats_series['TOV'])
        assert game_stats.tov is not None
        assert game_stats.pf == int(self.game_stats_series['PF'])
        assert game_stats.pf is not None
        assert game_stats.plus_minus == self.game_stats_series['+/-']
        assert game_stats.plus_minus is not None

    def test_filter_dnp_values_sets_values_to_zero_if_value_is_do_not_play(self):
        game_stats = self.mapper.get_game_stats_from_series(
            self.dnp_stats
        )

        assert game_stats.mp == 0
        assert self.dnp_stats['MP'].lower() == 'did not play'

    def test_get_team_name_by_identifier_raises_value_error_if_identifier_null(
        self,
        mapper
    ):
        with pytest.raises(
            ValueError, 
            match="Identifier cannot be None"
        ):
            mapper.get_team_name_by_identifier(None)

    def test_get_team_name_by_identifier_raises_value_error_if_identifier_is_not_valid(
        self,
        mapper
    ):
        invalid_name = "NOTANID"

        with pytest.raises(
            ValueError, 
            match=f"Team name: {invalid_name} not found."
        ):
            mapper.get_team_name_by_identifier(invalid_name)

    def test_get_team_name_by_identifier_returns_the_name_of_a_valid_team(
        self,
        mapper,
        valid_df
    ):
        mapper = BballReferenceMapper()

        for _, row in valid_df.iterrows():
            team_name = mapper.get_team_name_by_identifier(row['TEAM'])
            assert team_name == row['EXPECTED_NAME']

            team_name = mapper.get_team_name_by_identifier(row['TEAM'].lower())
            assert team_name == row['EXPECTED_NAME']


    def _assert_players_equal_df(
            self,
            players: list[PlayerDto], 
            df: pd.DataFrame
        ):
            assert(len(players) == len(df))

            for i in range(len(players)):
                assert players[i].first_name == df.iloc[i]['player'].split(" ")[0]
                assert players[i].last_name == df.iloc[i]['player'].split(" ")[1]
                assert players[i].number == df.iloc[i]['number']
                assert players[i].pos == df.iloc[i]['pos']
                assert players[i].height == df.iloc[i]['height']
                assert players[i].weight == df.iloc[i]['weight']
                assert players[i].birth_date == df.iloc[i]['birth_date']
                assert players[i].nationality == df.iloc[i]['nationality']
                assert players[i].college == df.iloc[i]['college']
