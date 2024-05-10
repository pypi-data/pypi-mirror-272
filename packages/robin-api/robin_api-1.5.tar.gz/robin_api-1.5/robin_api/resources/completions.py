


from typing import TYPE_CHECKING, List, Union, Optional, Iterator
from ..types import Completion, ChatCompletionChunk, ChatCompletion, ApiResponse, Models
from .._streaming import Stream
from typing_extensions import Literal
import httpx
from .._types import NOT_GIVEN, NotGiven
from .._resource import SyncAPIResource
from .._models import construct_type, construct_type_v2


if TYPE_CHECKING:
    from .._client import RobinAIClient

__all__ = ["Completions"]



def ensure_list(value, key):
    if key in value and not isinstance(value[key], list):
        value[key] = [value[key]]


class Completions(SyncAPIResource):
    #from .._client import RobinAIClient
    def __init__(self, client) -> None:
        super().__init__(client)

    

    def create_stream(
        self,
        *,
        model: Models,
        conversation: Union[str, List[str], List[int], List[List[int]], None],
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        save_response: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,

    ) -> Completion | Stream[Completion] | Iterator[Stream[Completion]]:

        body_request= {
                    "model": model,
                    "conversation": conversation,
                    "max_new_tokens": max_tokens,
                    "stream": True,
                    "temperature": temperature,
                    "save_response": save_response
                }
        response = self._stream(
            end_point = "get-response",
            body= body_request,
            )
        for data in response:
            ensure_list(data, 'choices')
            completion_obj = construct_type_v2(type_=ChatCompletionChunk, value=data)
            yield completion_obj

    def create(
        self,
        *,
        model: Models,
        conversation: Union[str, List[str], List[int], List[List[int]], None],
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        save_response: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,

    ) -> ChatCompletion | ApiResponse:
        body_request= {
                        "model": model,
                        "conversation": conversation,
                        "max_new_tokens": max_tokens,
                        "stream": False,
                        "temperature": temperature,
                        "save_response": save_response
                    }

        value : ApiResponse = self._post(
                end_point = "get-response",
                body= body_request,
                ) 
        if value.status_code == 200:
            value2 = {
            "choices": [
                {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": "The 2020 World Series was played in Texas at Globe Life Field in Arlington.",
                    "role": "assistant"
                },
                "logprobs": None
                }
            ],
            "created": 1677664795,
            "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
            "model": "Robin-4",
            "object": "chat.completion",
            "usage": {
                "completion_tokens": 17,
                "prompt_tokens": 57,
                "total_tokens": 74
            }
            }
            ensure_list(value.message, 'choices')

            completion_obj = construct_type_v2(type_=ChatCompletion, value=value.message)

            return completion_obj
        else:
            return value


            
        

        """return self.client.http_client._post(
            "/completions",
            body=maybe_transform(
                {
                    "model": model,
                    "conversation": conversation,
                    "best_of": best_of,
                    "echo": echo,
                    "frequency_penalty": frequency_penalty,
                    "logit_bias": logit_bias,
                    "logprobs": logprobs,
                    "max_tokens": max_tokens,
                    "n": n,
                    "presence_penalty": presence_penalty,
                    "seed": seed,
                    "stop": stop,
                    "stream": stream,
                    "suffix": suffix,
                    "temperature": temperature,
                    "top_p": top_p,
                    "user": user,
                },
                completion_create_params.CompletionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Completion,
            stream=stream or False,
            stream_cls=Stream[Completion],
        ) """




