from pydantic import BaseModel, Field
from typing import Optional, List
from abc import ABC, abstractmethod

DEFAULT_EMBEDDING_PATH = "/v1/embeddings"
DEFAULT_MAX_RETRIES = 3

class BaseEmbedParameter(BaseModel):
    '''做embedding的入参'''
    embed_content:str = Field(..., description="做embed的内容")  # 必需字段
    embed_key:str = Field(..., description="一类向量数据，缩小匹配的范围。例如：自由知识库-DK-成人")  # 必需字段
    embed_source:str = Field(..., description="来源，如果一份知识有多个来源，用来区分。各自业务自行设置和使用")  # 必需字段
    source_id:str = Field(..., description="来源出的对应的唯一记录")  # 必需字段
    meta_data:dict = Field(default={}, description="元素据，以上字段无法覆盖的信息")  # 可选字段，默认值为空字典

class EmbedConfig(BaseModel):
    '''embedding的配置'''
    model:str

class EmbedUsage(BaseModel):
    prompt_tokens:int
    total_tokens:int

class EmbedData(BaseModel):
    object:str = Field("embedding")
    embedding:List[float]
    index:int = Field(0)

class EmbedResponse(BaseModel):
    object:str = Field("list")
    data:list[EmbedData]
    model:str 
    usage:EmbedUsage 

class BuildEmbedParameter(BaseModel):
    api_key:str = Field(None, description="需要apikey的接口，需要设置这个参数")
    base_url:str = Field(None, description="需要拼接/v1/embedding的url")
    full_url:Optional[str] = Field(None, description="直接使用的接口，有先使用这个")
    max_retry:int = Field(DEFAULT_MAX_RETRIES, description="如果接口调用失败,最大尝试次数")
    model:str = Field("text-embedding-ada-002", description="模型")


class AbsEmbedModel(ABC):
    '''基础的embed模型'''
    api_key:str = Field(None, description="需要apikey的接口，需要设置这个参数")
    base_url:str = Field(None, description="需要拼接/v1/embedding的url")
    full_url:Optional[str] = Field(None, description="直接使用的接口，有先使用这个")
    max_retry:int = Field(DEFAULT_MAX_RETRIES, description="如果接口调用失败,最大尝试次数")
    model:str = Field("text-embedding-ada-002", description="模型")


    def __init__(self, parameter:BuildEmbedParameter) -> None:
        self.api_key = parameter.api_key
        self.base_url = parameter.base_url
        self.full_url = parameter.full_url
        self.max_retry = parameter.max_retry
        self.model = parameter.model
    
    @property
    def embed_url(self):
        if self.full_url:
            return self.full_url
        return self.base_url + DEFAULT_EMBEDDING_PATH

    @abstractmethod
    def embed(self, content:str) -> EmbedResponse:
        pass

    @abstractmethod
    async def async_embed(self, content: str) -> EmbedResponse:
        pass
import httpx
import requests


class BaseEmbedModel(AbsEmbedModel):
    '''基础的embed模型'''

    def __init__(self, parameter:BuildEmbedParameter) -> None:
        super().__init__(parameter)

    def embed(self, content:str) -> EmbedResponse:
        embedding_address = self.embed_url  # OpenAI embedding API 地址
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,  # 使用的模型
            "input": content  # 要进行 embedding 的内容
        }
        count = 0
        while count < self.max_retry:
            try:
                response = requests.post(embedding_address, headers=headers, json=payload)  # 发送 POST 请求
                response.raise_for_status()  # 检查请求是否成功
                return EmbedResponse(**response.json())  # 返回 EmbedResponse 实例
            except Exception as e:
                print(f"请求失败: {e}")
                count = count + 1


    async def async_embed(self, content: str) -> EmbedResponse:
        '''调用 OpenAI 的 embedding API 进行 embedding（异步）'''
        embedding_address = self.embed_url
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "input": content
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(embedding_address, headers=headers, json=payload)  # 发送异步 POST 请求
            response.raise_for_status()  # 检查请求是否成功
            return EmbedResponse(**response.json())  # 返回 EmbedResponse 实例
        


if __name__ == "__main__":
    embed_model = BaseEmbedModel(BuildEmbedParameter(base_url="http://127.0.0.1:1234"))
    result = embed_model.embed("我是孙悟空")
    print(result.model_dump())