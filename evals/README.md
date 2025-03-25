# GPT-Researcher 评估工具

该目录包含用于评估 GPT-Researcher 在不同研究任务中表现的工具和框架。

## 简单评估（`simple_evals/`）

`simple_evals` 目录包含一个简化的评估框架，改编自 [OpenAI 的 simple-evals 系统](https://github.com/openai/simple-evals)，专门用于衡量大语言模型在短形式事实性方面的表现。我们的实现基于 OpenAI 的 [SimpleQA 评估方法](https://github.com/openai/simple-evals/blob/main/simpleqa_eval.py)，遵循零样本（zero-shot）和思维链（chain-of-thought）方法，并针对 GPT-Researcher 的特定用例进行了调整。

### 组件

- `simpleqa_eval.py`：用于对研究响应进行评分的核心评估逻辑  
- `run_eval.py`：执行评估的脚本  
- `requirements.txt`：运行评估所需的依赖项  

### 测试数据集

`problems/` 目录包含评估使用的数据集：

- `Simple QA Test Set.csv`：从 OpenAI 原始测试集中镜像的事实性问题集合及其正确答案。此数据集作为基准，用于评估 GPT-Researcher 在查找和报告准确信息方面的能力。该文件在本地维护，以确保评估基准一致，避免上游更改影响测试方法。  

### 评估日志

`logs/` 目录包含详细的评估运行历史，这些日志会保存在版本控制系统中：  

- 格式：`SimpleQA Eval {num_problems} Problems {date}.txt`  
- 示例：`SimpleQA Eval 100 Problems 2-22-25.txt`  

这些日志提供了历史性能数据，并对以下用途至关重要：  
- 跟踪性能随时间的变化  
- 调试评估问题  
- 比较不同版本的结果  
- 确保评估过程的透明性  

**注意：**与典型的日志目录不同，该文件夹及其内容会被刻意地纳入 git 版本控制，以保留评估运行的历史记录。

### 功能特点

- 衡量研究响应的事实准确性  
- 使用 GPT-4 作为评分模型（可配置）  

```python
# 在 run_eval.py 中，可以自定义评分模型：
grader_model = ChatOpenAI(
    temperature=0,                           # 较低的温度确保评分一致性
    model_name="gpt-4-turbo",               # 可更改为其他 OpenAI 模型
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
```

- 对响应进行三分制评分：  
  - `CORRECT`：答案完整地包含了重要信息，无矛盾  
  - `INCORRECT`：答案存在事实性矛盾  
  - `NOT_ATTEMPTED`：答案既未确认也未否认目标信息  

**关于评分配置的说明：**默认的评分器使用 GPT-4-turbo，但您可以修改模型和参数，以使用不同的 OpenAI 模型，或调整温度来实现不同的评分行为。此配置独立于 Researcher 的配置，可根据需要优化成本或性能。  

### 跟踪指标

- 准确率（Accuracy）  
- F1 值（F1 Score）  
- 每次查询的成本  
- 成功/失败率  
- 回答尝试率  
- 信息来源覆盖率  

### 运行评估

1. 安装依赖项：  
```bash
cd evals/simple_evals
pip install -r requirements.txt
```

2. 在 `.env` 文件中设置环境变量：  
```bash
# 使用项目根目录的 .env 文件
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
LANGCHAIN_API_KEY=your_langchain_key_here
```

3. 运行评估：  
```bash
python run_eval.py --num_examples <number>
```
`num_examples` 参数决定要评估的随机测试查询数量（默认值：1）。

### 自定义 Researcher 行为

评估默认使用 GPTResearcher 的配置，但您可以通过修改 `run_eval.py` 来自定义 Researcher 的行为：  

```python
researcher = GPTResearcher(
    query=query,
    report_type=ReportType.ResearchReport.value,  # 报告类型
    report_format="markdown",                    # 输出格式
    report_source=ReportSource.Web.value,         # 研究信息来源
    tone=Tone.Objective,                          # 写作语气
    verbose=True                                  # 启用详细日志记录
)
```

这些参数可以调整，以评估不同的研究配置或输出格式。有关完整的配置选项列表，请参阅[配置文档](https://docs.gptr.dev/docs/gpt-researcher/gptr/config)。

**配置独立性说明：**评估系统设计为独立于 Researcher 的配置。这意味着您可以使用不同的 LLM 和设置来进行评估和研究。例如：  
- 评估可以使用 GPT-4-turbo 进行评分，而 Researcher 使用 Claude 3.5 Sonnet 进行研究  
- 可以使用不同的检索器、嵌入模型或报告格式  
- Token 限制和其他参数可以单独自定义  

这种分离允许在不同的 Researcher 配置之间进行无偏评估。但请注意，此功能目前处于实验阶段，仍需进一步测试。

### 输出

评估提供详细的指标，包括：  
- 每条查询的结果、信息来源和成本  
- 汇总指标（准确率、F1 值）  
- 总成本和每次查询的平均成本  
- 成功/失败次数统计  
- 详细的评分分布  

### 示例输出

```
=== 评估总结 ===
=== 汇总指标 ===

调试计数：
总成功次数：100
CORRECT：92
INCORRECT：7
NOT_ATTEMPTED：1
{
  "correct_rate": 0.92,
  "incorrect_rate": 0.07,
  "not_attempted_rate": 0.01,
  "answer_rate": 0.99,
  "accuracy": 0.9292929292929293,
  "f1": 0.9246231155778895
}
========================
准确率：0.929
F1 值：0.925

总成本：$1.2345  
每次查询的平均成本：$0.1371  
```

这套评估工具确保 GPT-Researcher 的表现可以持续追踪和改进，使研究过程更加透明且数据驱动。