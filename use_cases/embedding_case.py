from components.embedding.embedding import (
    BaseEmbedModel, BuildEmbedParameter
)
if __name__ == "__main__":
    embed_model = BaseEmbedModel(BuildEmbedParameter(base_url="http://127.0.0.1:1234"))
    result = embed_model.embed("我是孙悟空")
    print(result.model_dump())