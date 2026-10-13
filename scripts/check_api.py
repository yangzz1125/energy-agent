"""通过 Responses API 发送一次最小请求，检查模型服务是否可用。

在项目根目录运行：uv run python -m scripts.check_api
流程：导入配置 → 创建客户端 → 发出请求 → 检查回答 → 打印测试结果。
本脚本会实际调用模型，产生少量 API 费用。
"""

import time  # 用于计算请求耗时。

# OpenAI 是 SDK 的客户端类。设置其他服务的 base_url 后，
# 也能访问支持相应 OpenAI API 格式的服务，这里使用 DeepSeek。
from openai import OpenAI

# 从 config 文件夹中的 model.py 导入配置。
# 第一次导入该模块时，它会先读取 .env，再提供这些常量。
from config.model import MODEL_API_KEY, MODEL_BASE_URL, MODEL_NAME

# monotonic() 是不会随系统时钟调整而倒退的计时器，适合测量持续时间。
# 记录开始值，结束时再读取一次，两者之差就是耗时，单位为秒。
start = time.monotonic()

# 创建客户端本身不会向模型提问；真正的请求发生在 responses.create()。
# with 在代码块结束时关闭客户端，释放其网络连接资源。
with OpenAI(
    base_url=MODEL_BASE_URL,  # 服务的基础地址，SDK 会拼接 Responses 接口路径。
    api_key=MODEL_API_KEY,  # SDK 会将密钥用于请求鉴权。
    timeout=30.0,  # 网络操作的超时设置，单位为秒，并非整个脚本的严格总时限。
    max_retries=0,  # 失败时不自动重试，便于观察这一次请求的实际结果。
) as client:
    # 这是同步、非流式请求：代码在这里等待，再取得完整的响应对象。
    # response 不只是回答文本，还包含状态、模型名称、Token 用量等信息。
    response = client.responses.create(
        model=MODEL_NAME,  # 指定调用哪个模型。
        input="Reply with exactly API_OK and nothing else.",  # 要求返回固定文字，便于验证。
        reasoning={"effort": "none"},  # 在当前 DeepSeek 接口中关闭思考模式。
        max_output_tokens=128,  # 限制输出 Token 数量，避免测试生成过长内容。
    )

# output_text 提取响应中的回答文本；strip() 去掉开头和结尾的空白。
# or 表示任一条件成立就判定失败：请求未完成，或者没有返回预期文字。
# raise 会抛出异常，终止脚本，并让命令以非零退出码结束。
# 网络或鉴权异常也会由 SDK 直接抛出，保留原始报错便于排查。
if response.status != "completed" or response.output_text.strip() != "API_OK":
    raise RuntimeError("API returned an incomplete or unexpected response.")

# 只有上面的检查通过，程序才会执行到这里。
# f"...{表达式}..." 是格式化字符串，将表达式的值嵌入文字。
# :.2f 表示把耗时显示为两位小数，不会改变原始计时结果。
print("API_OK")
print(f"Model: {response.model}")
print(f"Elapsed: {time.monotonic() - start:.2f}s")
# Token 是模型处理文本的计量单位，不等于字数；这里是输入与输出的总用量。
print(f"Tokens: {response.usage.total_tokens}")
