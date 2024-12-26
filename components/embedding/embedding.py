from .base import(
    BuildEmbedParameter,
    EmbedResponse,
    AbsEmbedModel,
    DEFAULT_EMBEDDING_PATH
)
import httpx
import requests


class BaseEmbedModel(AbsEmbedModel):
    '''基础的embed模型'''

    def __init__(self, parameter:BuildEmbedParameter) -> None:
        super.__init__(parameter)

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