# 🔎 GPT Researcher

[![官方网站](https://img.shields.io/badge/Official%20Website-gptr.dev-blue?style=for-the-badge&logo=world&logoColor=white)](https://gptr.dev)  
[![Discord 关注](https://dcbadge.vercel.app/api/server/QgZXvJAccX?style=for-the-badge)](https://discord.com/invite/QgZXvJAccX)  

[![GitHub Repo 星标](https://img.shields.io/github/stars/assafelovic/gpt-researcher?style=social)](https://github.com/assafelovic/gpt-researcher)  
[![Twitter 关注](https://img.shields.io/twitter/follow/tavilyai?style=social)](https://twitter.com/tavilyai)  
[![PyPI 版本](https://badge.fury.io/py/gpt-researcher.svg)](https://badge.fury.io/py/gpt-researcher)  

**GPT Researcher 是一个自主代理，旨在对各种任务进行全面的在线研究。**  

该代理可以生成详细、事实性且无偏见的研究报告，并提供自定义选项，以便专注于相关资源、大纲和要点。受近期 [Plan-and-Solve](https://arxiv.org/abs/2305.04091) 和 [RAG](https://arxiv.org/abs/2005.11401) 论文的启发，GPT Researcher 解决了速度、确定性和可靠性问题，通过代理并行工作提供更稳定的性能和更快的速度，而非同步操作。  

**我们的使命是利用 AI 的力量，为个人和组织提供准确、公正、事实性的信息。**  

---

### 📦 PIP 包安装

> **步骤 0**：安装 Python 3.11 或更高版本。可参考[安装指南](https://www.tutorialsteacher.com/python/install-python)。  

> **步骤 1**：安装 GPT Researcher 包：[PyPI 页面](https://pypi.org/project/gpt-researcher/)  

```bash
pip install gpt-researcher
```

> **步骤 2**：创建 `.env` 文件，添加你的 OpenAI Key 和 Tavily API Key，或直接导出环境变量：  

```bash
export OPENAI_API_KEY={你的 OpenAI API Key}
```

```bash
export TAVILY_API_KEY={你的 Tavily API Key}
```

> **步骤 3**：在代码中使用 GPT Researcher：  

```python
from gpt_researcher import GPTResearcher
import asyncio


async def get_report(query: str, report_type: str) -> str:
    researcher = GPTResearcher(query, report_type)
    report = await researcher.run()
    return report

if __name__ == "__main__":
    query = "哪支球队可能赢得 NBA 总决赛？"
    report_type = "research_report"

    report = asyncio.run(get_report(query, report_type))
    print(report)
```

---

### ⚙️ 自定义配置（可选）

你可以通过自定义配置文件来覆盖默认设置。所有配置选项可在 [GPT Researcher 文档](https://docs.gptr.dev/docs/gpt-researcher/gptr/config) 中找到。  

#### 使用自定义 JSON 配置  

如果你希望修改 GPT Researcher 的默认配置，可以创建一个自定义的 JSON 配置文件，以下是步骤：  

**a.** 创建一个 JSON 文件（例如：`your_config.json`），写入你想要的配置：  

```json
{
  "retrievers": ["google"],
  "fast_llm": "cohere:command",
  "smart_llm": "cohere:command-nightly",
  "max_iterations": 3,
  "max_subtopics": 1
}
```

**b.** 初始化 GPTResearcher 时，传递自定义配置文件路径：  

```python
researcher = GPTResearcher(query, report_type, config_path="your_config.json")
```

---

#### 使用环境变量  

你也可以通过环境变量来配置 GPT Researcher。创建 `.env` 文件，并添加以下内容：  

```
RETRIEVERS=google
FAST_LLM=cohere:command
SMART_LLM=cohere:command-nightly
MAX_ITERATIONS=3
MAX_SUBTOPICS=1
```

GPT Researcher 会自动读取环境变量，从而配置行为。这种方式让你在不同环境下部署时更具灵活性。