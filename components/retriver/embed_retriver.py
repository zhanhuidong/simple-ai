from .dto import (
    RetriverParameter,
    RetriverResult,
    EmbedResults
)
from ..embedding.base import AbsEmbedModel
from .base import AbsRetriver
import logging as logger
import json
import traceback

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