from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Iterator,AsyncGenerator, Union
# from openai import OpenAI, AzureOpenAI
import httpx
import requests
import json
import os
from _base import (
    BaseLLMModel, 
    BaseMessage, 
    AIMessage,
    DEFAULT_MAX_RETRIES,
    DEFAULT_MAX_NEW_TOKENS,
    DEFAULT_TEMPERATURE,
    DEFAULT_MODEL,
    DEFAULT_COMPLETION_PATH
)

class RequestModel(BaseModel):
    model:str
    messages:list[dict]
    max_new_tokens:int = DEFAULT_MAX_NEW_TOKENS
    temperature:float = DEFAULT_TEMPERATURE
    stop:Optional[str] = Field(default="。")
    stream:bool = False

    @classmethod
    def from_messages(cls, model: str, messages: List[BaseMessage], max_new_tokens: int = DEFAULT_MAX_NEW_TOKENS, temperature: float = DEFAULT_TEMPERATURE, stop: Optional[List[str]] = None, stream: bool = False):
        messages_dict = [message.model_dump() for message in messages]
        return cls(model=model, messages=messages_dict, max_new_tokens=max_new_tokens, temperature=temperature, stop=stop, stream=stream)


class CompletionsChoice(BaseModel):
    message:Optional[AIMessage] = Field(default=None, description="非流式响应时候的消息")
    delta:Optional[AIMessage] = Field(default=None, description="流式响应时候的消息")
    index:int = Field(default=0, description="索引")
    logprobs:Optional[float] = Field(default=None, description="对数概率")
    finish_reason:Optional[str] = Field(default=None, description="结束原因")

class ModelResponse(BaseModel):
    id:str = Field(default=None, description="id")
    object:str = Field(default="chat.completions", description="object:chat.completions|chat.completions.chunk")
    created:int = Field(default=None, description="创建时间")
    choices:list[CompletionsChoice] = Field(default=[], description="消息列表")
    usage:Optional[dict] = Field(default=None, description="usage")
    model:str = Field(default="MIX", description="模型")
    system_fingerprint:str = Field(default="MIX", description="系统指纹")

# 一个类似与openai的模型类，但是可以定义自己的校验
class OpenAiStyleModel(BaseLLMModel):
    def __init__(
            self, 
            api_key:str = None,
            model:str = DEFAULT_MODEL,
            base_url:str = "https://api.openai.com",
            full_url:str = None,
            max_retry:int = 3,
            max_new_tokens:int = DEFAULT_MAX_NEW_TOKENS,
            temperature:float = DEFAULT_TEMPERATURE,
            top_p:float = 0.95,
            top_n:int = 50, 
            repetition_penalty:float = 1.1) -> None:
        
        super().__init__(api_key, base_url, max_retry)
        self.temperature = temperature
        self.top_p = top_p
        self.top_n = top_n
        self.repetition_penalty = repetition_penalty
        self.max_new_tokens = max_new_tokens
        self.full_url = full_url
        self.base_url = base_url
        self.model = model
    
        self.validate_custom_rules()


    def validate_custom_rules(self):
        # 实现自定义校验逻辑
        # api_key允许为空
        pass


    def completion(self, messages: List[BaseMessage], temperature: float = None, max_new_tokens: int = None, model: str = None, stream: bool = False) -> Iterator[ModelResponse]:
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

        if not stream:
             # 如果不使用流式返回
            data = response.json()  # 获取响应的 JSON 数据
            result = ModelResponse(**data)  # 将响应数据映射到模型
            
            yield result.choices[0].message.content
        # 使用流式返回
        for line in response.iter_lines():
            if line:
                # print(line.decode('utf-8'))
                if "DONE" in line.decode('utf-8'):
                    return
                # 去掉 'data:' 前缀并解析 JSON 数据
                data = json.loads(line.decode('utf-8').replace("data:", ""))
                result = ModelResponse(**data)
                yield result.choices[0].delta.content


    async def async_completion(self, messages: list[BaseMessage], temperature: float = None, max_new_tokens: int = None, model: str = None, stream: bool = False) -> AsyncGenerator[ModelResponse]: 
        # 创建请求模型
        requestModel = self.__build_request_model(messages, temperature, max_new_tokens, model, stream)

        async with httpx.AsyncClient() as client:
            response = await client.post(self.completion_url, json=requestModel.model_dump(), headers={"Authorization": f"Bearer {self.api_key}"})
            response.raise_for_status()
            
            if not stream:
                # 如果不使用流式返回
                data = response.json()  # 获取响应的 JSON 数据
                result = ModelResponse(**data)  # 将响应数据映射到模型
                yield result.choices[0].message.content
            else:
                # 使用流式返回
                async for line in response.aiter_lines():
                    if line:
                        if "DONE" in line.decode('utf-8'):
                            return
                        # 去掉 'data:' 前缀并解析 JSON 数据
                        data = json.loads(line.decode('utf-8').replace("data:", ""))
                        result = ModelResponse(**data)
                        yield result.choices[0].delta.content
    

    def __build_request_model(self, messages: list[BaseMessage], temperature: float = None, max_new_tokens: int = None, model: str = None, stream: bool = False) -> ModelResponse: # type: ignore
        # 创建请求模型
        return RequestModel.from_messages(
            model=model if model else self.model,
            messages=messages,
            max_new_tokens=max_new_tokens if max_new_tokens else self.max_new_tokens,
            temperature=temperature if temperature else self.temperature,
            stream=stream
        )