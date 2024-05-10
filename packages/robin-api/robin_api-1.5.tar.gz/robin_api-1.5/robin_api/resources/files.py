


from typing import TYPE_CHECKING
from ..types import Models, DeepLevel
from .._resource import SyncAPIResource
from .._models import construct_type_v2
from ..types import ApiResponse
from typing import TYPE_CHECKING, Dict, List, Union, Optional, overload, Iterator
from ..types import  ChatCompletionChunk, ChatCompletion
import validators
from typing_extensions import Literal


if TYPE_CHECKING:
    from .._client import RobinAIClient

__all__ = ["Files"]


def ensure_list(value, key):
    if key in value and not isinstance(value[key], list):
        value[key] = [value[key]]



class Files(SyncAPIResource):
    #from .._client import RobinAIClient
    def __init__(self, client) -> None:
        super().__init__(client)

    #def upload_web_page_information(self, args: DeepLevel):

    def _upload_file(self, args: DeepLevel):


        args = DeepLevel(args)    
        if not validators.url(args.url):
            raise ValueError("url is not valid")

        if args.folder_id == None:
            body_request= {
                            "fileUrl": args.url
                        }
        else:
            body_request= {
                            "fileUrl": args.url,
                            "apiFolderId": args.folder_id
                        }
        
        value : ApiResponse = self._post(
                end_point = "folders",
                body= body_request,
                ) 
        if value.status_code == 200:
            return value
        else:
            return value
    
    def upload_web_page_information(self, *, url: str, deep_level: Literal[1, 2, 3] = 1 , folder_id=None):
        args = DeepLevel(url=url, deep_level=deep_level, folder_id=folder_id)  
        #if not isinstance(deep_level, DeepLevel):
        #    raise ValueError("deep_level must have values between 1 and 3")

        if not validators.url(url):
            raise ValueError("url is not valid")
        
        if folder_id == None:
            body_request=  {
                            "webUrl": url,
                            "deep_level": deep_level
                            }
        else:
            body_request=  {
                            "webUrl": url,
                            "deep_level": deep_level,
                            "apiFolderId": folder_id
                            }

        value : ApiResponse = self._post(
                end_point = "folders/add-web-url",
                body= body_request,
                ) 
        if value.status_code == 200:
            return value
        else:
            return value
        
    def get_similar_sentences(self, *, query:str, api_folder_id:str, top: int = 10, similarity_threshold: float = 0.4):
        body_request= { 
            "query" : query,
            "top": top,
            "apiFolderId": api_folder_id,
            "similarityThreshold": similarity_threshold
        }

        value : ApiResponse = self._post(
                end_point = "folders/get-similar-sentences",
                body= body_request,
                ) 
        if value.status_code == 200:
            return value
        else:
            return value
        
    def get_response_similar_sentences(self, *,
                                       conversation:str, 
                                       api_folder_id:str, 
                                       model:Models,
                                       only_with_context: bool, 
                                       top: int = 10, 
                                       similarity_threshold: 
                                       float = 0.4, 
                                       max_new_tokens: 512,
                                       save_response: bool = False) -> ApiResponse:
        body_request= { 
            "max_new_tokens": max_new_tokens,
            "stream" : False,
            "model" : model,
            "conversation" : conversation,
            "top": top,
            "folder_id": api_folder_id,
            "similarity_threshold": similarity_threshold,
            "only_with_context": only_with_context,
            "save_response": save_response
        }

        value : ApiResponse = self._post(
                end_point = "get-response",
                body= body_request,
                ) 
        if value.status_code == 200:
            value.message = construct_type_v2(type_=ChatCompletion, value=value.message )
            return value
        else:
            return value
            
    def get_response_similar_sentences_stream(self, *,
                                       conversation:str, 
                                       api_folder_id:str, 
                                       model:Models,
                                       only_with_context: bool, 
                                       top: int = 10, 
                                       similarity_threshold: 
                                       float = 0.4, 
                                       max_new_tokens: 512,
                                       save_response: bool = False) -> Iterator[ChatCompletion]:
        body_request= { 
            "max_new_tokens": max_new_tokens,
            "stream" : True,
            "model" : model,
            "conversation" : conversation,
            "top": top,
            "folder_id": api_folder_id,
            "similarity_threshold": similarity_threshold,
            "only_with_context": only_with_context,
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

        





