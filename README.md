# 简单 AI 组件库

## 项目简介

本项目旨在创建一个简单易用的 AI 组件库。每个组件都可以独立使用，也可以与其他组件任意组合，以满足不同的需求。该库提供灵活的接口，方便开发者快速集成和扩展 AI 功能。

## 特性

- **模块化设计**：每个组件都是独立的，可以根据需要进行组合。
- **易于使用**：简单的 API 接口，快速上手。
- **灵活性**：支持多种 AI 模型和算法，适应不同的应用场景。
- **异步支持**：提供异步接口，提升性能和响应速度。

## 组件列表

- **Embedding 组件**：用于文本嵌入，支持多种嵌入模型。
- **文档解析器**：支持多种文件格式的解析，包括 PDF、Word 和 PowerPoint。
- **记忆管理**：提供消息的存储和检索功能，支持本地和数据库存储。
- **数据处理**：提供数据预处理和后处理功能，提升模型的输入输出质量。

## 安装

使用以下命令安装项目依赖：

```bash
pip install -r requirements.txt
```

## 使用示例

### 嵌入模型示例

以下是如何使用 Embedding 组件的示例：

```python
from components.embedding.embedding import BaseEmbedModel
from components.embedding._base import BuildEmbedParameter

# 创建嵌入模型参数
parameter = BuildEmbedParameter(api_key="YOUR_API_KEY", model="text-embedding-model")

# 初始化嵌入模型
embed_model = BaseEmbedModel(parameter)

# 使用嵌入模型进行文本嵌入
response = embed_model.embed("这是一个示例文本。")
print(response)
```

### 文档解析器示例

以下是如何使用文档解析器的示例：

```python
from components.resolver.document_resolver import DocumentResolver

# 初始化文档解析器
resolver = DocumentResolver(file_path="/path/to/your/document")

# 解析文档
page_contents = resolver.resolve()

# 打印解析结果
for page in page_contents:
    print(page.page_content)
```
