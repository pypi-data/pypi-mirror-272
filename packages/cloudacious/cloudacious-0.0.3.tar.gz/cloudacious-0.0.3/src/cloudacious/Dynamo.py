class Tools:
    """
    Tooling to work with Dynamo
    """

    def __init__(
        self,
    ):
        """
        init
        """
        return

    def dict_to_item(self, raw) -> dict:
        """
        dict_to_item() converts a Python dict to a dynamo item and returns a dict in dynamo-itemized format.

        `raw` is just a dict.
        """
        if type(raw) is dict:
            resp = {}
            for k, v in raw.items():
                if type(v) is str:
                    resp[k] = {"S": v}
                elif type(v) is int:
                    resp[k] = {"N": str(v)}
                elif type(v) is dict:
                    resp[k] = {"M": self.dict_to_item(v)}
                elif type(v) is list:
                    resp[k] = []
                    for i in v:
                        resp[k].append(self.dict_to_item(i))
            return resp
        elif type(raw) is str:
            return {"S": raw}
        elif type(raw) is int:
            return {"N": str(raw)}
