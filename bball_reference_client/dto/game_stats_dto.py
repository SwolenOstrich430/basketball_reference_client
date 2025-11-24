class GameStatsDto():
    def __init__(
        self, external_id: int, mp: str, fgm_2p: int, fga_2p: int, 
        fgm_3p: int, fga_3p: int, ftm: int, fta: int, 
        orb: int, drb: int, ast: int, stl: int, blk: int, 
        tov: int, pf: int, plus_minus: int
    ):
        self.external_id = int(external_id)
        self.mp = mp
        self.fgm_2p = int(fgm_2p)
        self.fga_2p = int(fga_2p)
        self.fgm_3p = int(fgm_3p)
        self.fga_3p = int(fga_3p)
        self.ftm = int(ftm)
        self.fta = int(fta)
        self.orb = int(orb)
        self.drb = int(drb)
        self.ast = int(ast)
        self.stl = int(stl)
        self.blk = int(blk)
        self.tov = int(tov)
        self.pf = int(pf)
        self.plus_minus = int(plus_minus)