# LangGraph x GPT Researcher

[LangGraph](https://python.langchain.com/docs/langgraph) 是一个用于构建带有 LLM 的有状态多代理应用程序的库。  
本示例使用 LangGraph 来自动化对任何给定主题进行深入研究的过程。

## 用例
通过使用 LangGraph，研究过程的深度和质量可以显著提升，利用多个具备专业技能的代理协作完成研究工作。  
受最近的 [STORM](https://arxiv.org/abs/2402.14207) 论文启发，本示例展示了一支 AI 代理团队如何协作，从规划到发布，进行全面的研究。

一次平均的运行会生成一份 5-6 页的研究报告，支持 PDF、Docx 和 Markdown 等多种格式。

请注意：多代理使用的模型配置与 GPT-Researcher 的配置相同。目前仅使用 SMART_LLM。详情请参考 [LLM 配置页面](https://docs.gptr.dev/docs/gpt-researcher/llms/llms)。

## 多代理团队介绍
研究团队由 8 个代理组成：  
- **Human（人类）** — 参与过程、监督代理工作并提供反馈的“人类监督者”。  
- **Chief Editor（主编）** — 监督研究过程并管理团队的“总指挥”，使用 LangGraph 协调其他代理。  
- **Researcher（研究员）** — 一个专门从事深入研究的自主代理，利用 gpt-researcher 进行资料收集和分析。  
- **Editor（编辑）** — 负责规划研究大纲和结构。  
- **Reviewer（审阅者）** — 根据一系列标准验证研究结果的正确性。  
- **Revisor（修订者）** — 根据审阅者的反馈修改研究结果，直到满足要求。  
- **Writer（撰写者）** — 负责整理和撰写最终的研究报告。  
- **Publisher（出版者）** — 负责将最终报告发布为多种格式（如 PDF、Docx、Markdown 等）。  

## 工作流程
整体流程分为以下几个阶段：  
1. 规划阶段  
2. 数据收集与分析  
3. 审核与修订  
4. 撰写与提交  
5. 发布  

### 架构图
<div align="center">
<img align="center" height="600" src="https://github.com/user-attachments/assets/ef561295-05f4-40a8-a57d-8178be687b18">
</div>
<br clear="all"/>

### 具体步骤  
1. **浏览器（Researcher）** — 根据给定的研究任务，在互联网上进行初步研究。  
2. **编辑（Editor）** — 根据初步研究，规划报告大纲和结构。  
3. **针对每个大纲主题（并行执行）：**  
   - **研究员（Researcher）** — 对各子主题进行深入研究并撰写初稿。  
   - **审阅者（Reviewer）** — 根据标准验证初稿的正确性并提供反馈。  
   - **修订者（Revisor）** — 根据审阅者的反馈进行修订，直到达到满意的结果。  
4. **撰写者（Writer）** — 整合研究成果，撰写最终报告，包括引言、结论和参考文献。  
5. **出版者（Publisher）** — 将最终报告发布为多种格式（如 PDF、Docx、Markdown 等）。  

## 如何运行  
1. 安装所需的包（位于根目录）：  
    ```bash
    pip install -r requirements.txt
    ```  
2. 更新环境变量，详细信息请参考 [GPT-Researcher 文档](https://docs.gptr.dev/docs/gpt-researcher/llms/llms)。  
3. 运行应用程序：  
    ```bash
    python main.py
    ```  

## 使用方法
要更改研究主题和自定义报告，请编辑主目录中的 `task.json` 文件。  

### `task.json` 包含以下字段：  
- **`query`** — 研究的主题或任务。  
- **`model`** — 用于代理的 OpenAI 模型。  
- **`max_sections`** — 报告的最大章节数。每个章节对应研究任务的一个子主题。  
- **`include_human_feedback`** — 若为 `true`，用户可以向代理提供反馈；若为 `false`，代理将自主工作。  
- **`publish_formats`** — 发布报告的格式。报告将写入 `output` 目录。  
- **`source`** — 研究来源，可选 `web` 或 `local`。若选择 `local`，请添加 `DOC_PATH` 环境变量。  
- **`follow_guidelines`** — 若为 `true`，研究报告将遵循特定指南（生成时间更长）；若为 `false`，报告生成速度更快，但可能不完全遵循指南。  
- **`guidelines`** — 报告必须遵循的指南列表。  
- **`verbose`** — 若为 `true`，应用程序将在控制台打印详细日志。  

#### 示例：  
```json
{
  "query": "人工智能是否处于炒作周期？",
  "model": "gpt-4o",
  "max_sections": 3, 
  "publish_formats": { 
    "markdown": true,
    "pdf": true,
    "docx": true
  },
  "include_human_feedback": false,
  "source": "web",
  "follow_guidelines": true,
  "guidelines": [
    "报告必须完整回答原始问题",
    "报告必须遵循 APA 格式",
    "报告必须用英文撰写"
  ],
  "verbose": true
}
```

## 部署方法
1. 安装 `langgraph-cli` 工具：  
    ```bash
    pip install langgraph-cli
    ```  
2. 启动应用程序：  
    ```bash
    langgraph up
    ```  

然后，请参考 [文档](https://github.com/langchain-ai/langgraph-example) 了解如何使用流式和异步端点，以及如何访问 Playground。