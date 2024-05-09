from typing import Optional, Dict

from pydantic import StrictStr

from montelo.Log import Log
from montelo.MonteloClient import MonteloClient
from montelo.Span import Span
from montelo.client import LogInput, TokenInfo
from montelo.core.MonteloDatapoints import MonteloDatapoints
from montelo.core.MonteloDatasets import MonteloDatasets
from montelo.core.MonteloExperiments import MonteloExperiments
from montelo.extended.ExtendedOpenAI import ExtendedOpenAI
from montelo.types import MonteloClientOptions, OpenAIClientConfig
from montelo.utils import cuid_generator, get_current_utc_time


class Montelo:
    def __init__(
            self,
            *,
            montelo: Optional[MonteloClientOptions] = None,
            openai_config: Optional[OpenAIClientConfig] = None,
    ):
        self._constructor_options = dict(
            montelo=montelo,
            openai_config=openai_config
        )
        self._montelo_client = MonteloClient(options=montelo)
        self.openai = ExtendedOpenAI(montelo_client=self._montelo_client, config=openai_config)
        self.datasets = MonteloDatasets(montelo_client=self._montelo_client)
        self.datapoints = MonteloDatapoints(montelo_client=self._montelo_client)
        self.experiments = MonteloExperiments(montelo_client=self._montelo_client)

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

    def trace(
            self,
            *,
            name: StrictStr,
            user_id: Optional[StrictStr] = None,
            extra: Optional[Dict] = None,
    ):
        trace = self._montelo_client.get_trace()
        if trace:
            raise Exception("Trace already set on this Montelo instance.")

        new_montelo_instance = Montelo(**self._constructor_options)
        new_montelo_instance._montelo_client.set_trace(
            trace=dict(
                id=cuid_generator(),
                name=name,
                user_id=user_id,
                extra=extra,
            )
        )
        return new_montelo_instance
