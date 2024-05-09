import datetime
from functools import reduce
from typing import TypedDict, Optional, Dict, List

import openai.types.chat
from openai import OpenAI, DEFAULT_MAX_RETRIES, NOT_GIVEN
from openai.resources import Chat
from openai.resources.chat import Completions
from openai.types.chat import ChatCompletionChunk

from montelo.MonteloClient import MonteloClient
from montelo.client import LogInput
from montelo.types import OpenAIClientConfig
from montelo.utils import format_utc_date


class TimeInterval(TypedDict):
    start_time: str
    end_time: str
    duration: float


class MonteloLogExtend(TypedDict):
    name: Optional[str]
    extra: Optional[Dict]


def process_final_message(chunks):
    def reducer(acc, chunk_with_index):
        index, chunk = chunk_with_index

        if isinstance(chunk, ChatCompletionChunk):
            delta = chunk.choices[0].delta if chunk.choices else {}
            tool_calls = delta.tool_calls if delta else []
            function_call = delta.function_call if delta else None

            if tool_calls:
                if index == 0:
                    acc["tool_calls"] = [{
                        "id": tool.id,
                        "type": tool.type,
                        "function": {
                            "name": tool.function.name,
                            "arguments": tool.function.arguments
                        }
                    } for tool in tool_calls]
                else:
                    for i, tool in enumerate(acc.get("tool_calls", [])):
                        matching_tool_call = next((tc for tc in tool_calls if tc.index == i), None)
                        if matching_tool_call:
                            acc["tool_calls"][i]["function"]["arguments"] += matching_tool_call.function.arguments
            elif function_call:
                if index == 0:
                    acc["function_call"] = {
                        "name": function_call.name,
                        "arguments": function_call.arguments
                    }
                else:
                    acc["function_call"]["arguments"] += function_call.arguments
            elif delta and delta.content:
                if index == 0:
                    acc["content"] = delta.content
                else:
                    acc["content"] = (acc.get("content") or "") + delta.content
        else:
            print(f"Unexpected data type for chunk at index {index}: {type(chunk)}")

        return acc

    initial_value = {"role": "assistant"}
    final_message = reduce(reducer, enumerate(chunks), initial_value)
    return final_message


class ExtendedChatCompletions(Completions):
    def __init__(self, *, client, montelo_client: MonteloClient):
        super().__init__(client)
        self._montelo_client = montelo_client

    def create(self, *args, **kwargs):
        start_time = datetime.datetime.now(datetime.UTC)
        start_time_iso = format_utc_date(start_time)

        res = super().create(*args, **kwargs)

        name = kwargs.get("name", "Chat Completion")
        extra = kwargs.get("extra", None)
        stream = kwargs.get("stream", False)
        if stream:
            def gen():
                chunks: List[ChatCompletionChunk] = []
                for chunk in res:
                    chunks.append(chunk)
                    yield chunk

                end_time = datetime.datetime.now(datetime.UTC)
                end_time_iso = format_utc_date(end_time)

                duration = (end_time - start_time).total_seconds()

                data = openai.types.chat.ChatCompletion(
                    id=chunks[0].id,
                    model=chunks[0].model,
                    object="chat.completion",
                    created=chunks[0].created,
                    system_fingerprint=chunks[0].system_fingerprint,
                    usage=None,  # will be calculated on backend
                    choices=[
                        {
                            "index": chunks[0].choices[0].index,
                            "logprobs": chunks[0].choices[0].logprobs or None,
                            "finish_reason": chunks[0].choices[0].finish_reason or "stop",
                            "message": process_final_message(chunks),
                        }
                    ]
                )

                self._log_to_db(
                    base=kwargs,
                    extend={
                        "name": name,
                        "extra": extra
                    },
                    output=data,
                    time={
                        "start_time": start_time_iso,
                        "end_time": end_time_iso,
                        "duration": duration
                    }
                )
            gen()
        else:
            end_time = datetime.datetime.now(datetime.UTC)
            end_time_iso = format_utc_date(end_time)

            duration = (end_time - start_time).total_seconds()

            self._log_to_db(
                base=kwargs,
                extend={
                    "name": name,
                    "extra": extra
                },
                output=res,
                time={
                    "start_time": start_time_iso,
                    "end_time": end_time_iso,
                    "duration": duration
                },
            )

        return res

    def _log_to_db(
            self,
            *,
            base,
            extend: MonteloLogExtend,
            output: openai.types.chat.ChatCompletion,
            time: TimeInterval,
    ):
        payload = LogInput(
            **time,
            **extend,
            source="OPENAI",
            model=output.model,
            input=base,
            output=output.dict()
        )
        self._montelo_client.create_log(log=payload)


class ExtendedChat(Chat):
    def __init__(self, *, client, montelo_client: MonteloClient):
        super().__init__(client)
        self.completions = ExtendedChatCompletions(client=client, montelo_client=montelo_client)


class ExtendedOpenAI(OpenAI):
    def __init__(self, *, montelo_client: MonteloClient, config: Optional[OpenAIClientConfig] = None):
        config = config if config else {}
        super().__init__(
            api_key=config.api_key if config else None,
            organization=config.organization if config else None,
            project=config.project if config else None,
            base_url=config.base_url if config else None,
            timeout=config.timeout if config else NOT_GIVEN,
            max_retries=config.max_retries if config and config.max_retries else DEFAULT_MAX_RETRIES,
            default_headers=config.default_headers if config else None,
            default_query=config.default_query if config else None,
            http_client=config.http_client if config else None,
        )
        self.chat = ExtendedChat(client=self, montelo_client=montelo_client)
