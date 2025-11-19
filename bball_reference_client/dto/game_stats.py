class GameStatsDto():
    def __init__(
        self, player: str, mp: int, fg: int, fga: int, 
        three_fg: int, three_pga: int, ft: int, fta: int, 
        orb: int, drb: int, ast: int, stl: int, blk: int, 
        tov: int, pf: int, plus_minus: int
    ):
        self.player_name = player 
        self.mp = mp
        self.fg = fg 
        self.fga = fg 
        self.orb = orb 
        self.drb = drb 
        self.ast = ast 
        self.stl = stl
        self.blk = blk 
        self.tov = tov 
        self.pf = pf 
        self.plus_minus = plus_minus