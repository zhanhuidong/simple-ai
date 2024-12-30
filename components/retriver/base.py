from abc import ABC,abstractmethod
from .dto import (
    RetriverParameter,
    RetriverResult
)
from ..embedding.base import AbsEmbedModel
import json
import traceback
import logging as logger 
'''
近似查询
'''
class AbsRetriver(ABC):
    '''
    近似查询抽象类
    '''
    
    def search(self, req:RetriverParameter) -> RetriverResult:
        result = self._doc_search(req)
        result = self._after_search(req, result)

        return result
    
    @abstractmethod
    def _doc_search(self, req:RetriverParameter) -> RetriverResult:
        pass
    
    def _after_search(self, req:RetriverParameter, result:RetriverResult):
        return result



class BaseRetriver(AbsRetriver):
    '''
     基础查询
     简单的根据query进行embedding查询
    '''
    embeddings:AbsEmbedModel

    def __init__(self, embeddings:AbsEmbedModel) -> None:
        self.embeddings = embeddings

    def _doc_search(self, req: RetriverParameter) -> RetriverResult:
        
        logger.info(f"开始根据搜索条件和documentKey进行文档搜索，搜索条件：{req.model_dump_json()}")

        # 因为做embedding的时候做到最细维度，查询的时候，也应该是最细维度
        allKeys = []
        for key in req.documentKeys:
            documents = KnowledgeDocumentInfoRepo.select_by_document_key_like(key)
            if documents:
                allKeys.extend([doc.documentKey for doc in documents])

        # 取Embedding数据
        req.documentKeys = list(set(allKeys))
        embedResults:list[EmbedResultWithMetaData] = EmbeddingService.query_segment_embedding_results(req)
        
        documentEmbedResults = [DocumentEmbedResult(matchKey=embedResult.metaData.documentKey, results=[EmbedResult(content=embedResult.content, score=embedResult.score)]) for embedResult in embedResults]

        # 取document文本数据

        # DocumentEmbedResult

        return RetriverResult(query=req.query, embedResult=documentEmbedResults, docResult=[])