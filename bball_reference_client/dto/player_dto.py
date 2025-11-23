class PlayerDto():
    def __init__(
        self, num: int, player: str, position: str, height: str,
        weight: int, birth_date: int, exp: str, school: str, 
        player_id: int, **kwargs
    ):
        self.number = num 
        names = player.split(" ")
        self.first_name = names[0]
        self.last_name = names[1]
        self.position = position
        self.height = height
        self.weight = weight
        self.birth_date = birth_date
        self.college = school
        self.external_id = player_id