from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Iterator,AsyncGenerator, Union
# from openai import OpenAI, AzureOpenAI
import httpx
import requests
import json
import os
from datetime import datetime
# from _base import BaseModel, DEFAULT_MAX_RETRIES, BaseMessage, AIMessage
from _base import (
    BaseLLMModel, 
    BaseMessage, 
    AIMessage,
    CompletionsChoice,
    SystemMessage,
    UserMessage,
    ModelResponse,
    DEFAULT_MAX_RETRIES,
    DEFAULT_MAX_NEW_TOKENS,
    DEFAULT_TEMPERATURE,
    DEFAULT_MODEL,
    DEFAULT_COMPLETION_PATH
)

DEFAULT_MAX_NEW_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.95
DEFAULT_TOP_N = 50
DEFAULT_REPETITION_PENALTY= 1.1


DEFAULT_MODEL = "llama3pro"
COMPLETION_PATH = "/v1/chat/completions"
MODEL_PATH = "/v1/models"
EMBEDDING_PATH = "/v1/embeddings"


class MixResponse(BaseModel):
    Response:str
    Response_wm:str
    prompt_tokens:float
    completion_tokens:float
    total_tokens:float

class MixParameter(BaseModel):
    max_new_tokens:int = DEFAULT_MAX_NEW_TOKENS,
    temperature:float = DEFAULT_TEMPERATURE,
    top_p:float = 0.95,
    top_n:int = 50,
    repetition_penalty:float = 1.1

class MixRequestModel(BaseModel):
    external_call_type:str
    messages:list[dict]
    parameter:MixParameter
    stream:bool = False

    @classmethod
    def from_messages(cls, model: str, messages: List[BaseMessage], parameter:MixParameter, stream: bool = False):
        messages_dict = [message.model_dump() for message in messages]
        return cls(external_call_type=model, messages=messages_dict, parameter = parameter)


# 一个类似与openai的模型类，但是可以定义自己的校验
class MIX(BaseLLMModel):
    parameter:MixParameter
    external_call_type:str = DEFAULT_MODEL
    def __init__(
            self, 
            api_key:str = None,
            model:str = DEFAULT_MODEL,
            base_url:str = "https://api.openai.com",
            full_url:str = None,
            max_retry:int = DEFAULT_MAX_RETRIES,
            max_new_tokens:int = DEFAULT_MAX_NEW_TOKENS,
            temperature:float = DEFAULT_TEMPERATURE,
            top_p:float = DEFAULT_TOP_P,
            top_n:int = DEFAULT_TOP_N, 
            repetition_penalty:float = DEFAULT_REPETITION_PENALTY) -> None:
        
        super().__init__(api_key, base_url, max_retry)
        self.parameter = MixParameter(max_new_tokens=max_new_tokens, temperature=temperature, top_p=top_p, top_n=top_n, repetition_penalty=repetition_penalty)
        self.full_url = full_url
        self.base_url = base_url
        self.external_call_type = model
    
        self.validate_custom_rules()

        

    def validate_custom_rules(self):
        # 实现自定义校验逻辑
        pass

    def completion(self, messages: List[BaseMessage], temperature: float = None, max_new_tokens: int = None, model: str = None, stream: bool = False) -> ModelResponse: # type: ignore
        # 创建请求模型
        requestModel = self.__build_request_model(messages, temperature, max_new_tokens, model, stream)

        # 发送 POST 请求，获取响应
        count = 0
        while count < self.max_retry:
            # print(f"count:{str(count)}")
            try:
                response = requests.post(self.completion_url, json=requestModel.model_dump(), headers={"Authorization":f"Bearer {self.api_key}"})
                response.raise_for_status()
                break
            except requests.RequestException as e:
                # 处理请求异常
                print(f"请求失败: {e}")
                count = count+1

        if stream:
            raise Exception("stream is not supported in mix")
            
        # 如果不使用流式返回
        data = response.json()  # 获取响应的 JSON 数据
        result = MixResponse(**data)  # 将响应数据映射到模型
        return ModelResponse(id="", object="chat.completions", created=int(datetime.now().timestamp()*1000), choices=[CompletionsChoice(message=AIMessage(content=result.Response), index=0, logprobs=None, finish_reason="stop")], usage=result.model_dump(), model="MIX", system_fingerprint="MIX")



    async def async_completion(self, messages: list[BaseMessage], temperature: float = None, max_new_tokens: int = None, model: str = None, stream: bool = False) -> ModelResponse: # type: ignore
        # 创建请求模型
        requestModel = self.__build_request_model(messages, temperature, max_new_tokens, model, stream)

        async with httpx.AsyncClient() as client:
            response = await client.post(self.completion_url, json=requestModel.model_dump(), headers={"Authorization": f"Bearer {self.api_key}"})
            response.raise_for_status()
            
            # 如果不使用流式返回
            data = response.json()  # 获取响应的 JSON 数据
            result = MixResponse(**data)  # 将响应数据映射到模型
            yield result.choices[0].message.content
    

    def __build_request_model(self, messages: list[BaseMessage], temperature: float = None, max_new_tokens: int = None, model: str = None, stream: bool = False) -> ModelResponse: # type: ignore
        # 创建请求模型
        # 创建请求模型
        parameter=self.parameter
        if temperature:
            parameter.temperature = temperature
        
        if max_new_tokens:
            parameter.max_new_tokens = max_new_tokens
        

        requestModel = MixRequestModel.from_messages(
            model=model if model else self.external_call_type,
            messages=messages,
            parameter=self.parameter,
            stream=stream
        )

        return requestModel


client = MIX(base_url="192.168.6.16:8070", api_key="1234", full_url="http://192.168.6.16:8070/generate/")
# 非流式
result = client.completion(messages=[SystemMessage(content="你是一个小助手，你的名字是小马。"),UserMessage(content="介绍一下你自己")], stream=False)
print(result.model_dump())