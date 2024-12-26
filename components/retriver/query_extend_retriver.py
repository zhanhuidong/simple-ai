from .dto import (
    RetriverParameter,
    RetriverResult,
    EmbedResults
)
from .base import AbsRetriver

class QueryExtendRetriver(AbsRetriver):
    '''
    问题扩增查询
    '''

    def __init__(self) -> None:
        super().__init__()

    def _doc_search(self, req: RetriverParameter) -> RetriverResult:
        # 先进行问题的衍生
        questions = self.query_extend(req.query)

        # 将每个问题的查询，提交给线程池
        futures = []
        baseRevalant = BaseRevalantSearch()
        for question in questions:
            newReq = DocumentSearchV2Req(query=question, documentKeys=req.documentKeys, score=req.score)
            futures.append(searchExcutor.submit(baseRevalant.doc_search, newReq))

        # 获取所有的搜索结果
        seahrcResults:list[RetriverResult] = [future.result() for future in futures]

        # 回复进行合并，只返回一个DocumentSearchV2Response
        matchKey2EmbedResults:dict[str,EmbedResults] = {}
        for result in seahrcResults:
            if not result:
                continue
            for embed in result.embedResult:
                embedResults = matchKey2EmbedResults.get(embed.matchKey, EmbedResults())
                embedResults.extend(embed.results)
                matchKey2EmbedResults[embed.matchKey] = embedResults
                
                
        
        # 再进行去重
        retResult = RetriverResult(query=req.query, diffuseQeuries = questions, embedResult=[], docResult=[])
        for matchKey, embeds in matchKey2EmbedResults.items():
            docEmbedResult = DocumentEmbedResult(matchKey=matchKey, results = embeds.results)
            retResult.embedResult.append(docEmbedResult)

        return retResult
    
    def _after_search(self, req:RetriverParameter, result:RetriverResult):
        record = KnowledgeSearchRecord(queryContent = req.query, documentKeys = json.dumps(req.documentKeys, ensure_ascii=False), score = str(req.score), diffuseQuery = json.dumps(result.diffuseQeuries, ensure_ascii=False), searchResult = result.model_dump_json())
        KnowledgeSearchRecordRepo.insert_record(record)

        # 根据分数进行过滤
        filteredResult = RetriverResult(query=req.query, embedResult = [], docResult=[])
        filteredEmbed = []
        for embed in result.embedResult:
            rs = [r for r in embed.results if r.score >= req.score]
            if not rs:
                continue
            filteredEmbed.append(DocumentEmbedResult(matchKey=embed.matchKey, results=rs))
        
        filteredResult.embedResult = filteredEmbed
        filteredResult.diffuseQeuries = result.diffuseQeuries if result.diffuseQeuries else []

        return filteredResult
    
    def query_extend(self, query:str) ->list[str]:
        # 通过模型理解，进行不同角度问题的扩散
        response = request_think_med.request_app_c(requestBody={"question":query}, tempNo="d3037536b76611ef939300163e2ab20c")
        questions = []
        try:
            questions = json.loads(response.data.replace("\n",""))
        except Exception as e:
            logger.error(f"问题衍生出错：{traceback.format_exc()}")
            questions = []
        
        questions.append(req.query)

        return questions