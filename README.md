
4. 安装依赖并启动服务器：

    ```bash
    pip install -r requirements.txt
  python -m uvicorn main:app --reload  
    ```

访问 [http://localhost:8000](http://localhost:8000) 开始使用。

<div align="center" id="top">

<img src="https://github.com/assafelovic/gpt-researcher/assets/13554167/20af8286-b386-44a5-9a83-3be1365139c3" alt="Logo" width="80">

####

[![官方网站](https://img.shields.io/badge/官方网站-gptr.dev-teal?style=for-the-badge&logo=world&logoColor=white&color=0891b2)](https://gptr.dev)
[![文档](https://img.shields.io/badge/文档-DOCS-f472b6?logo=googledocs&logoColor=white&style=for-the-badge)](https://docs.gptr.dev)
[![Discord 关注](https://dcbadge.vercel.app/api/server/QgZXvJAccX?style=for-the-badge&theme=clean-inverted&?compact=true)](https://discord.gg/QgZXvJAccX)

[![PyPI 版本](https://img.shields.io/pypi/v/gpt-researcher?logo=pypi&logoColor=white&style=flat)](https://badge.fury.io/py/gpt-researcher)
![GitHub 发布](https://img.shields.io/github/v/release/assafelovic/gpt-researcher?style=flat&logo=github)
[![在 Colab 中打开](https://img.shields.io/static/v1?message=Open%20in%20Colab&logo=googlecolab&labelColor=grey&color=yellow&label=%20&style=flat&logoSize=40)](https://colab.research.google.com/github/assafelovic/gpt-researcher/blob/master/docs/docs/examples/pip-run.ipynb)
[![Docker 镜像版本](https://img.shields.io/docker/v/elestio/gpt-researcher/latest?arch=amd64&style=flat&logo=docker&logoColor=white&color=1D63ED)](https://hub.docker.com/r/gptresearcher/gpt-researcher)
[![Twitter 关注](https://img.shields.io/twitter/follow/assaf_elovic?style=social)](https://twitter.com/assaf_elovic)

[English](README.md) | [中文](README-zh_CN.md) | [日本語](README-ja_JP.md) | [한국어](README-ko_KR.md)

</div>

# 🔎 GPT Researcher

**GPT Researcher 是一个开放的深度研究代理，专为任何给定任务的网络和本地研究而设计。**

该代理生成详细、事实性和无偏见的研究报告，并附有引用。GPT Researcher 提供全套定制选项，以创建量身定制和特定领域的研究代理。受最近的 [Plan-and-Solve](https://arxiv.org/abs/2305.04091) 和 [RAG](https://arxiv.org/abs/2005.11401) 论文启发，GPT Researcher 通过并行代理工作提供稳定的性能和提高的速度，解决了错误信息、速度、确定性和可靠性问题。

**我们的使命是通过 AI 为个人和组织提供准确、无偏见和事实性的信息。**

## 为什么选择 GPT Researcher？

- 手动研究的客观结论可能需要数周时间，需要大量资源和时间。
- 在过时信息上训练的 LLM 可能会产生幻觉，对当前研究任务变得不相关。
- 当前的 LLM 有令牌限制，不足以生成长篇研究报告。
- 现有服务中有限的网络来源导致错误信息和浅层结果。
- 选择性网络来源可能会在研究任务中引入偏见。

## 演示
https://github.com/user-attachments/assets/2cc38f6a-9f66-4644-9e69-a46c40e296d4

## 架构

核心理念是利用"规划者"和"执行"代理。规划者生成研究问题，而执行代理收集相关信息。发布者然后将所有发现汇总成一份全面的报告。

<div align="center">
<img align="center" height="600" src="https://github.com/assafelovic/gpt-researcher/assets/13554167/4ac896fd-63ab-4b77-9688-ff62aafcc527">
</div>

步骤：
* 基于研究查询创建特定任务的代理。
* 生成共同形成对任务的客观意见的问题。
* 使用爬虫代理为每个问题收集信息。
* 总结并跟踪每个资源的来源。
* 过滤并汇总摘要成最终研究报告。

## 特点

- 📝 使用网络和本地文档生成详细的研究报告。
- 🖼️ 智能图像抓取和过滤用于报告。
- 📜 生成超过 2,000 字的详细报告。
- 🌐 汇总超过 20 个来源以得出客观结论。
- 🖥️ 前端有轻量级（HTML/CSS/JS）和生产就绪（NextJS + Tailwind）版本。
- 🔍 支持 JavaScript 的网页抓取。
- 📂 在整个研究过程中保持记忆和上下文。
- 📄 将报告导出为 PDF、Word 和其他格式。

## ✨ 深度研究

GPT Researcher 现在包括深度研究 - 一种高级递归研究工作流，通过代理深度和广度探索主题。此功能采用树状探索模式，深入研究子主题，同时保持对研究主题的全面视图。

- 🌳 可配置深度和广度的树状探索
- ⚡️ 并发处理以获得更快的结果
- 🤝 跨研究分支的智能上下文管理
- ⏱️ 每次深度研究约需 5 分钟
- 💰 每次研究成本约 $0.4（使用"高"推理努力的 `o3-mini`）


## 📖 文档

- 安装和设置指南
- 配置和定制选项
- 操作示例
- 完整 API 参考

## ⚙️ 入门

### 安装

1. 安装 Python 3.11 或更高版本。[指南](https://www.tutorialsteacher.com/python/install-python)。
2. 克隆项目并导航到目录：

    ```bash
    git clone https://github.com/luokunkirk/deepresearchagent.git
    ```

3. 通过导出或存储在 `.env` 文件中设置 API 密钥。

    ```bash
    export OPENAI_API_KEY={您的 OpenAI API 密钥}
    export TAVILY_API_KEY={您的 Tavily API 密钥}
    ```

4. 安装依赖并启动服务器：

    ```bash
    pip install -r requirements.txt
    python -m uvicorn main:app --reload
    ```

访问 [http://localhost:8000](http://localhost:8000) 开始使用。

## 作为 PIP 包运行
