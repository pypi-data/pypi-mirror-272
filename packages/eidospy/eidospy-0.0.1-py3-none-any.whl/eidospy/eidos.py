from .dataspace import DataSpace
from requests import Session


class Eidos:
    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint
        self.requests = Session()

    def space(self, space_id):
        return DataSpace(space_id, self)
