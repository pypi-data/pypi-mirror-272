from .table import Table


BASE_URL = "http://localhost:3333"


class DataSpace:
    def __init__(self, space_id: str, eidos):
        self.space_id = space_id
        self.eidos = eidos

    def table(self, table_id):
        return Table(table_id, self)
