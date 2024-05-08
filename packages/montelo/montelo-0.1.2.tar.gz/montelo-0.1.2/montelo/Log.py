from pydantic import StrictStr

from montelo.MonteloClient import MonteloClient
from montelo.client import EndLogInput


class Log:
    def __init__(self, *, id: StrictStr, montelo_client: MonteloClient):
        self._id = id
        self._montelo_client = montelo_client

    def end(
            self,
            *,
            id: StrictStr,
            log: EndLogInput
    ):
        self._montelo_client.end_log(id=id, log=log)
