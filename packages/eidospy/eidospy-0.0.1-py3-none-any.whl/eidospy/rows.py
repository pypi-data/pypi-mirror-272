class TableRowsManager:
    def __init__(self, table):
        self.table = table

    def _call(self, method, params):
        res = self.table.requests.post(
            self.table.api_endpoint,
            json={
                "space": self.table.space_id,
                "method": method,
                "params": params,
            },
        )
        data = res.json()
        return data["data"]["result"]

    def get(self, id: str):
        return self._call(
            f"table({self.table.table_id}).rows.get", [self.table.table_id, id]
        )

    def query(self, filter: dict = None, options: dict = None):
        return self._call(
            f"table({self.table.table_id}).rows.query", [filter or {}, options or {}]
        )

    def create(
        self,
        data: dict,
        options: dict = None,
    ):
        return self._call(
            f"table({self.table.table_id}).rows.create", [data, options or {}]
        )

    def delete(self, id: str):
        return self._call(f"table({self.table.table_id}).rows.delete", [id])

    def update(self, id: str, data: dict, options: dict = None):
        return self._call(
            f"table({self.table.table_id}).rows.update",
            [id, data, options or {}],
        )
