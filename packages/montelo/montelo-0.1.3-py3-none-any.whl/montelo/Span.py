from datetime import datetime
from typing import Optional, Dict

from pydantic import StrictStr

from montelo.Log import Log
from montelo.MonteloClient import MonteloClient
from montelo.client import LogInput, TokenInfo
from montelo.utils import cuid_generator, get_current_utc_time


class Span:
    def __init__(
            self,
            *,
            id: StrictStr,
            name: StrictStr,
            montelo_client: MonteloClient
    ):
        self._id = id
        self._name = name
        self._montelo_client = montelo_client

    def span(
            self,
            *,
            name: StrictStr,
            input: Optional[Dict] = None,
            output: Optional[Dict] = None,
            start_time: Optional[StrictStr] = None,
            end_time: Optional[StrictStr] = None,
            extra: Optional[Dict] = None,
    ):
        id = cuid_generator()
        now = get_current_utc_time()
        start_time = start_time or now
        end_time = end_time or now
        name = self._name + " / " + name

        self._montelo_client.create_log(
            log=LogInput(
                id=id,
                name=name,
                input=input,
                output=output,
                start_time=start_time,
                end_time=end_time,
                extra=extra,
                source="MANUAL"
            ),
        )

        return Span(
            id=id,
            name=name,
            montelo_client=self._montelo_client
        )

    def log(
            self,
            name: StrictStr,
            model: Optional[StrictStr] = None,
            input: Optional[Dict] = None,
            output: Optional[Dict] = None,
            start_time: Optional[StrictStr] = None,
            end_time: Optional[StrictStr] = None,
            duration: Optional[int] = None,
            token_info: Optional[TokenInfo] = None,
            extra: Optional[Dict] = None,
    ):
        id = cuid_generator()
        now = get_current_utc_time()
        start_time = start_time or now
        end_time = end_time or now
        name = self._name + " / " + name

        self._montelo_client.create_log(
            log=LogInput(
                id=id,
                model=model,
                name=name,
                input=input,
                output=output,
                start_time=start_time,
                end_time=end_time,
                extra=extra,
                source="MANUAL",
                duration=duration,
                token_info=token_info,
            ),
        )

        return Log(id=id, montelo_client=self._montelo_client)
