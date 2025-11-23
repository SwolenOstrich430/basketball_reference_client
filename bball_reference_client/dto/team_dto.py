class TeamDto():
    def __init__(
        self, 
        identifier: str,
        name: str, 
        external_id: int
    ):
        self.identifier = identifier
        self.name = name
        self.external_id = external_id