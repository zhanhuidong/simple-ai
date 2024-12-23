
from components.resolver.document_resolver import DocumentResolver, PageContent


if "__main__" == __name__:
    result:list[PageContent] = DocumentResolver(file_path="/Users/zbc/Downloads").resolve()

    for page in result:
        print(page.model_dump())