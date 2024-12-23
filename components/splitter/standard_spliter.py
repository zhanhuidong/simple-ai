from _base import (
    AbsSpliter, BaseSplitParameter
)
from langchain_text_splitters import CharacterTextSplitter

class StandardSpliter(AbsSpliter):
    '''标准切割'''

    def __init__(self, parameter: BaseSplitParameter) -> None:
        self.spliter = CharacterTextSplitter(separator=parameter.separator,is_separator_regex=parameter.is_separator_regex,chunk_size=parameter.chunk_size, chunk_overlap=parameter.chunk_overlap)


    def split(self, text:str) -> list[str]:
        
        return self.spliter.split_text(text)
    
