from components.model.openai_style import (
    OpenAiStyleModel, SystemMessage,UserMessage
)

client = OpenAiStyleModel(base_url="http://127.0.0.1:1234", model="qwen2.5-coder")
# 流式
result = client.completion(messages=[SystemMessage(content="你是一个小助手，你的名字是小马。"),UserMessage(content="帮我根据冬天，写一篇100字以上的文章。")], stream=True)
for s in result:
    print(s)

# 非流式
result = client.completion(messages=[SystemMessage(content="你是一个小助手，你的名字是小马。"),UserMessage(content="帮我根据冬天，写一篇100字以上的文章。")], stream=True)
print(result)