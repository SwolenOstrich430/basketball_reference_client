class PlayerDto():
    def __init__(
        self, number: int, player: str, pos: str, height: str,
        weight: int, birth_date: int, nationality: str, 
        experience: str, college: str
    ):
        self.number = number 
        names = player.split(" ")
        self.first_name = names[0]
        self.last_name = names[1]
        self.pos = pos
        self.height = height
        self.weight = weight
        self.birth_date = birth_date
        self.nationality = nationality
        self.college = college