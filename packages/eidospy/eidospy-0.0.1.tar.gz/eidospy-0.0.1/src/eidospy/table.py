import uuid

from eidospy.rows import TableRowsManager


class Table:
    def __init__(self, table_id, space):
        self.space = space
        self.eidos = space.eidos
        self.requests = space.eidos.requests
        self.api_endpoint = space.eidos.api_endpoint
        self.space_id = space.space_id
        self.table_id = table_id

    @property
    def rows(self):
        return TableRowsManager(self)


if __name__ == "__main__":
    pass
