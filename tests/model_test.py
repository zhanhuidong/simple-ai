from components.model.openai_style import (
    OpenAiStyleModel, SystemMessage,UserMessage
)

client = OpenAiStyleModel(base_url="http://127.0.0.1:1234", model="qwen2.5-coder")
result = client.completion(messages=[SystemMessage(content="你是一个小助手，你的名字是小马。"),UserMessage(content="帮我根据冬天，写一篇100字以上的文章。")], stream=True)
# print(result.model_dump())
for s in result:
    print(s)



# 调用异步方法
import asyncio

async def main():
    # 创建 OpenAiStyleModel 实例
    model = OpenAiStyleModel(api_key="1234", base_url="http://127.0.0.1:1234")

    # 准备消息
    messages = [
        SystemMessage(content="你可以回答任何问题。"),
        UserMessage(content="你好，今天的天气怎么样？"),
    ]

    # 调用 async_completion 方法
    async for response in model.async_completion(messages):
        print(response)

# 运行异步主函数
if __name__ == "__main__":
    asyncio.run(main())