from pydantic import BaseModel, Field, field_validator
import os
from typing import Optional, List

class RetriverParameter(BaseModel):
    query:str = Field(description="消息/问题")
    documentKeys:Optional[list[str]] = Field(default=[], description="要查询的文档key列表，也可以直接是知识库Key")
    score:float = Field(default=0.5, description="匹配的分数")

    @field_validator('documentKeys')
    def docType_validator(cls, v):
        if not v:
           raise Exception("至少应该指定一个知识库/文档那个key")
        
        return v
    
class EmbedResult(BaseModel):
    content:str = Field(description="匹配内容")
    score:float = Field(description="匹配分数")

class DocumentEmbedResult(BaseModel):
    matchKey:str = Field(description="是因为哪个documentKey匹配到的")
    results:list[EmbedResult] = Field(description="embed匹配结果")

    def get_distinct_embed_result(self):
        # 内容去重，分数取最高的
        content2Score:dict = {}
        for result in self.results:
            score = content2Score.get(result.content, 0)
            if score <= result.score:
                content2Score[result.content] = result.score

        return list(EmbedResult(score=v,content=k) for k,v in content2Score.items())

class DocResult(BaseModel):
    content:str = Field(description="匹配内容")
    documentName:str = Field(description="文档名称")

class DocumentSearchResult(BaseModel):
    matchKey:str = Field(description="是因为哪个documentKey匹配到的")
    results:list[DocResult] = Field(description="匹配到的结果，根据文档名进行了合并")
    
class RetriverResult(BaseModel):
    query:str = Field(description="消息/问题")
    diffuseQeuries:Optional[list[str]] = Field(default=[], description="扩散的问题列表")
    embedResult:list[DocumentEmbedResult] = Field(description="embed匹配结果")
    docResult:list[DocumentSearchResult] = Field(description="页面匹配结果,根据documentKey进行了合并")

class EmbedResults(BaseModel):
    results:list[EmbedResult]=[]

    def append(self, result:EmbedResult):
        # 添加的时候，进行合并去重
        for resul in self.results:
            if resul.content == result.content:
                resul.score = max(resul.score, result.score)
                return
            
        self.results.append(result)
    
    def extend(self, results:list[EmbedResult]):
        for result in results:
            self.append(result)
