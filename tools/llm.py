import os
import asyncio
from openai import AsyncOpenAI
import platform

# 创建异步客户端实例
client = AsyncOpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 定义异步任务列表
async def get_answer(question):
    response = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant, able to abstract the main idea of a document and decide whether a document is useful to the user, according to their needs." },
            {"role": "user", "content": question}
        ],
        model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    )
    return response.choices[0].message.content