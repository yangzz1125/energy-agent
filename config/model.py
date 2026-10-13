"""统一读取模型配置，供其他模块导入。

数据流：项目根目录的 .env → 当前 Python 进程的环境变量 → 三个配置常量。
实际的地址、密钥和模型名称填写在 .env 中，这个文件只负责读取。
"""

# os 用于访问当前进程的环境变量；Path 用于处理文件和目录路径。
import os
from pathlib import Path

# python-dotenv 是安装时的包名，dotenv 是 Python 中导入时使用的模块名。
from dotenv import load_dotenv

# __file__ 是当前 model.py 的路径，resolve() 将其转换为绝对路径。
# parents[0] 是 config/，parents[1] 是 energy-agent/，即项目根目录。
# Path 对象的 / 运算符用来拼接路径，因此这里能找到根目录的 .env。
# 路径相对于代码文件确定，不依赖你从哪个目录启动 Python。
# utf-8-sig 既能读取普通 UTF-8，也能处理带 BOM 的 UTF-8 文件。
# override=True 表示 .env 的值覆盖当前进程中已有的同名环境变量，
# 不会永久修改 Windows 的系统环境变量。
load_dotenv(
    Path(__file__).resolve().parents[1] / ".env", encoding="utf-8-sig", override=True
)

# os.environ 类似字典，通过变量名获取字符串值；缺少变量时直接报 KeyError。
# 全大写是常量的命名惯例，不代表 Python 禁止这些变量被重新赋值。
# 通常第一次导入本模块时执行这些代码；修改 .env 后重新运行程序即可读取新值。
MODEL_BASE_URL = os.environ["MODEL_BASE_URL"]  # 模型服务地址。
MODEL_API_KEY = os.environ["MODEL_API_KEY"]  # 身份验证密钥，不要打印或提交到 Git。
MODEL_NAME = os.environ["MODEL_NAME"]  # 请求中指定的模型名称。
