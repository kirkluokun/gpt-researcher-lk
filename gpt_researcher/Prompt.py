import warnings
from datetime import date, datetime, timezone

from .utils.enum import ReportSource, ReportType, Tone
from typing import List, Dict, Any


def generate_search_queries_prompt(
    question: str,
    parent_query: str,
    report_type: str,
    max_iterations: int = 3,
    context: List[Dict[str, Any]] = [],
):
    """生成给定问题的搜索查询提示。
    参数:
        question (str): 要生成搜索查询提示的问题
        parent_query (str): 主要问题（仅与详细报告相关）
        report_type (str): 报告类型
        max_iterations (int): 要生成的搜索查询的最大数量
        context (str): 通过实时网络信息更好地理解任务的上下文

    返回: str: 给定问题的搜索查询提示
    """

    if (
        report_type == ReportType.DetailedReport.value
        or report_type == ReportType.SubtopicReport.value
    ):
        task = f"{parent_query} - {question}"
    else:
        task = question

    context_prompt = f"""
你是一位经验丰富的研究助手，负责生成搜索查询以找到与以下任务相关的信息："{task}"。
上下文：{context}

使用此上下文来指导和完善你的搜索查询。上下文提供了实时网络信息，可以帮助你生成更具体和相关的查询。考虑上下文中提到的任何当前事件、最新发展或特定细节，这些都可以增强搜索查询。
""" if context else ""

    dynamic_example = ", ".join([f'"查询 {i+1}"' for i in range(max_iterations)])

    return f"""编写{max_iterations}个谷歌搜索查询，以便在线搜索，从以下任务中形成客观意见："{task}"

如果需要，假设当前日期是{datetime.now(timezone.utc).strftime('%B %d, %Y')}。

{context_prompt}
你必须以以下格式回复字符串列表：[{dynamic_example}]。
回复应该只包含列表。
"""


def generate_report_prompt(
    question: str,
    context,
    report_source: str,
    report_format="apa",
    total_words=1000,
    tone=None,
    language="english",
):
    """为给定问题和研究摘要生成报告提示。
    参数: question (str): 要生成报告提示的问题
            research_summary (str): 要生成报告提示的研究摘要
    返回: str: 给定问题和研究摘要的报告提示
    """

    reference_prompt = ""
    if report_source == ReportSource.Web.value:
        reference_prompt = f"""
你必须在报告末尾将所有使用的源URL作为参考列出，并确保不添加重复的来源，而只为每个来源添加一个引用。
每个URL应该是超链接：[网站URL](URL)
此外，你必须在报告中引用相关URL的地方包含超链接：

例如：作者，A. A.（年，月，日）。网页标题。网站名称。[网站URL](URL)
"""
    else:
        reference_prompt = f"""
你必须在报告末尾将所有使用的源文档名称作为参考列出，并确保不添加重复的来源，而只为每个来源添加一个引用。"
"""

    tone_prompt = f"以{tone.value}的语气撰写报告。" if tone else ""

    return f"""
信息："{context}"
---
使用上述信息，以详细报告的形式回答以下查询或任务："{question}" --
报告应该专注于回答查询，结构良好，信息丰富，
深入且全面，如果有可用的事实和数字，应包含这些内容，并且至少有{total_words}个字。
你应该努力使用所有提供的相关和必要信息，尽可能地写长报告。

请在你的报告中遵循以下所有指导方针：
- 你必须根据给定信息确定自己具体且有效的观点。不要推迟到一般和无意义的结论。
- 你必须使用markdown语法和{report_format}格式编写报告。
- 你必须优先考虑你使用的来源的相关性、可靠性和重要性。选择可信来源而非不太可靠的来源。
- 如果来源可信，你也必须优先考虑新文章而非旧文章。
- 使用{report_format}格式的文内引用参考，并在引用它们的句子或段落结尾处使用markdown超链接，如：([文内引用](url))。
- 不要忘记在报告末尾添加{report_format}格式的参考列表和完整的url链接，不带超链接。
- {reference_prompt}
- {tone_prompt}

你必须用以下语言撰写报告：{language}。
请尽力而为，这对我的职业生涯非常重要。
假设当前日期是{date.today()}。
"""

def curate_sources(query, sources, max_results=10):
    return f"""你的目标是评估和整理为研究任务提供的抓取内容："{query}"，
    同时优先包含相关和高质量的信息，特别是包含统计数据、数字或具体数据的来源。

最终整理的列表将用作创建研究报告的上下文，因此优先考虑：
- 尽可能保留原始信息，特别强调包含定量数据或独特见解的来源
- 包含广泛的观点和见解
- 仅过滤掉明显不相关或无法使用的内容

评估指南：
1. 根据以下标准评估每个来源：
   - 相关性：包括直接或部分与研究查询相关的来源。倾向于包含而非排除。
   - 可信度：优先考虑权威来源，但保留其他来源，除非明显不可信。
   - 时效性：优先考虑最新信息，除非旧数据是必要或有价值的。
   - 客观性：保留有偏见的来源，如果它们提供独特或互补的观点。
   - 定量价值：优先考虑包含统计数据、数字或其他具体数据的来源。
2. 来源选择：
   - 尽可能包含多个相关来源，最多{max_results}个，注重广泛覆盖和多样性。
   - 优先考虑包含统计数据、数值数据或可验证事实的来源。
   - 如果重叠内容增加深度，特别是涉及数据时，可以接受。
   - 仅当来源完全不相关、严重过时或由于内容质量差而无法使用时才排除。
3. 内容保留：
   - 不要重写、总结或压缩任何来源内容。
   - 保留所有可用信息，只清理明显的垃圾或格式问题。
   - 如果边缘相关或不完整的来源包含有价值的数据或见解，则保留它们。

要评估的来源列表：
{sources}

你必须以与原始来源完全相同的JSON列表格式返回你的响应。
响应不得包含任何markdown格式或额外文本（如```json），只有JSON列表！
"""




def generate_resource_report_prompt(
    question, context, report_source: str, report_format="apa", tone=None, total_words=1000, language="english"
):
    """为给定问题和研究摘要生成资源报告提示。

    参数:
        question (str): 要生成资源报告提示的问题。
        context (str): 要生成资源报告提示的研究摘要。

    返回:
        str: 给定问题和研究摘要的资源报告提示。
    """

    reference_prompt = ""
    if report_source == ReportSource.Web.value:
        reference_prompt = f"""
            你必须包含所有相关的源URL。
            每个URL应该是超链接：[网站URL](URL)
            """
    else:
        reference_prompt = f"""
            你必须在报告末尾将所有使用的源文档名称作为参考列出，并确保不添加重复的来源，而只为每个来源添加一个引用。"
        """

    return (
        f'"""{context}"""\n\n基于上述信息，为以下问题或主题生成一份参考书目推荐报告：'
        f'"{question}"。报告应提供每个推荐资源的详细分析，'
        "解释每个来源如何有助于找到研究问题的答案。\n"
        "关注每个来源的相关性、可靠性和重要性。\n"
        "确保报告结构良好、信息丰富、深入且遵循Markdown语法。\n"
        "在可用时包含相关事实、数据和数字。\n"
        f"报告应至少有{total_words}个字。\n"
        f"你必须用以下语言撰写报告：{language}。\n"
        "你必须包含所有相关的源URL。"
        "每个URL应该是超链接：[网站URL](URL)"
        f"{reference_prompt}"
    )


def generate_custom_report_prompt(
    query_prompt, context, report_source: str, report_format="apa", tone=None, total_words=1000, language: str = "english"
):
    return f'"{context}"\n\n{query_prompt}'


def generate_outline_report_prompt(
    question, context, report_source: str, report_format="apa", tone=None,  total_words=1000, language: str = "english"
):
    """为给定问题和研究摘要生成大纲报告提示。
    参数: question (str): 要生成大纲报告提示的问题
            research_summary (str): 要生成大纲报告提示的研究摘要
    返回: str: 给定问题和研究摘要的大纲报告提示
    """

    return (
        f'"""{context}""" 使用上述信息，为以下问题或主题生成一份Markdown语法的研究报告大纲：'
        f'"{question}"。大纲应为研究报告提供一个结构良好的框架，'
        "包括主要部分、子部分和要涵盖的关键点。"
        f"研究报告应详细、信息丰富、深入且至少有{total_words}个字。"
        "使用适当的Markdown语法格式化大纲并确保可读性。"
    )


def generate_deep_research_prompt(
    question: str,
    context: str,
    report_source: str,
    report_format="apa",
    tone=None,
    total_words=2000,
    language: str = "english"
):
    """生成深度研究报告提示，专门用于处理层次化研究结果。
    参数:
        question (str): 研究问题
        context (str): 包含带引用的学习内容的研究上下文
        report_source (str): 研究来源（网络等）
        report_format (str): 报告格式样式
        tone: 写作时使用的语气
        total_words (int): 最小字数
        language (str): 输出语言
    返回:
        str: 深度研究报告提示
    """
    reference_prompt = ""
    if report_source == ReportSource.Web.value:
        reference_prompt = f"""
你必须在报告末尾将所有使用的源URL作为参考列出，并确保不添加重复的来源，而只为每个来源添加一个引用。
每个URL应该是超链接：[网站URL](URL)
此外，你必须在报告中引用相关URL的地方包含超链接：

例如：作者，A. A.（年，月，日）。网页标题。网站名称。[网站URL](URL)
"""
    else:
        reference_prompt = f"""
你必须在报告末尾将所有使用的源文档名称作为参考列出，并确保不添加重复的来源，而只为每个来源添加一个引用。"
"""

    tone_prompt = f"以{tone.value}的语气撰写报告。" if tone else ""
    
    return f"""
使用以下层次化研究信息和引用：

"{context}"

撰写一份全面的研究报告，回答查询："{question}"

报告应：
1. 综合多层次研究深度的信息
2. 整合来自各种研究分支的发现
3. 呈现一个从基础到高级见解构建的连贯叙述
4. 在整个报告中保持适当的来源引用
5. 结构良好，有清晰的章节和小节
6. 至少有{total_words}个字
7. 遵循{report_format}格式，使用markdown语法

额外要求：
- 优先考虑从更深层次研究中出现的见解
- 突出不同研究分支之间的联系
- 包含相关统计数据、数据和具体例子
- 你必须根据给定信息确定自己具体且有效的观点。不要推迟到一般和无意义的结论。
- 你必须优先考虑你使用的来源的相关性、可靠性和重要性。选择可信来源而非不太可靠的来源。
- 如果来源可信，你也必须优先考虑新文章而非旧文章。
- 使用{report_format}格式的文内引用参考，并在引用它们的句子或段落结尾处使用markdown超链接，如：([文内引用](url))。
- {tone_prompt}
- 用{language}语言撰写

{reference_prompt}

请撰写一份彻底、研究充分的报告，将所有收集的信息综合成一个连贯的整体。
假设当前日期是{datetime.now(timezone.utc).strftime('%B %d, %Y')}。
"""


def auto_agent_instructions():
    return """
这项任务涉及研究给定主题，无论其复杂性或是否有明确答案。研究由特定服务器进行，由其类型和角色定义，每个服务器需要不同的指令。
代理
服务器由主题的领域和可用于研究所提供主题的特定服务器名称确定。代理按其专业领域分类，每种服务器类型都与相应的表情符号相关联。

例子：
任务："我应该投资苹果股票吗？"
回复：
{
    "server": "💰 金融代理",
    "agent_role_prompt: "你是一位经验丰富的金融分析师AI助手。你的主要目标是根据提供的数据和趋势，撰写全面、敏锐、公正且有条理的金融报告。"
}
任务："转售运动鞋能否盈利？"
回复：
{ 
    "server":  "📈 商业分析师代理",
    "agent_role_prompt": "你是一位经验丰富的AI商业分析师助手。你的主要目标是根据提供的商业数据、市场趋势和战略分析，生成全面、有见地、公正且系统结构化的商业报告。"
}
任务："特拉维夫最有趣的景点是什么？"
回复：
{
    "server":  "🌍 旅游代理",
    "agent_role_prompt": "你是一位环游世界的AI导游助手。你的主要目的是起草有关给定地点的引人入胜、有见地、公正且结构良好的旅行报告，包括历史、景点和文化见解。"
}
"""


def generate_summary_prompt(query, data):
    """为给定问题和文本生成摘要提示。
    参数: question (str): 要生成摘要提示的问题
            text (str): 要生成摘要提示的文本
    返回: str: 给定问题和文本的摘要提示
    """

    return (
        f'{data}\n 使用上述文本，根据以下任务或查询对其进行总结："{query}"。\n 如果'
        f"无法使用文本回答查询，你必须简短地总结文本。\n 如果有可用的，包括所有事实"
        f"信息，如数字、统计数据、引用等。"
    )


################################################################################################

# 详细报告提示


def generate_subtopics_prompt() -> str:
    return """
提供主要主题：

{task}

和研究数据：

{data}

- 构建一个子主题列表，这些子主题将作为要生成的关于任务的报告文档的标题。
- 这些是可能的子主题列表：{subtopics}。
- 不应有任何重复的子主题。
- 将子主题数量限制为最多{max_subtopics}个
- 最后按其任务对子主题进行排序，以相关且有意义的顺序，适合在详细报告中呈现

"重要！"：
- 每个子主题必须仅与主要主题和提供的研究数据相关！

{format_instructions}
"""


def generate_subtopic_report_prompt(
    current_subtopic,
    existing_headers: list,
    relevant_written_contents: list,
    main_topic: str,
    context,
    report_format: str = "apa",
    max_subsections=5,
    total_words=800,
    tone: Tone = Tone.Objective,
    language: str = "english",
) -> str:
    return f"""
上下文：
"{context}"

主题和子主题：
使用最新可用信息，在主题：{main_topic}下构建关于子主题：{current_subtopic}的详细报告。
你必须将子部分数量限制为最多{max_subsections}个。

内容重点：
- 报告应专注于回答问题，结构良好，信息丰富，深入，并包括事实和数字（如果有）。
- 使用markdown语法并遵循{report_format.upper()}格式。

重要：内容和部分的唯一性：
- 这部分指令对确保内容唯一且不与现有报告重叠至关重要。
- 在撰写任何新的子部分之前，请仔细审查下面提供的现有标题和现有书面内容。
- 防止任何已在现有书面内容中涵盖的内容。
- 不要使用任何现有标题作为新的子部分标题。
- 不要重复已在现有书面内容中涵盖的任何信息或密切相关的变体，以避免重复。
- 如果你有嵌套的子部分，确保它们是唯一的，且未在现有书面内容中涵盖。
- 确保你的内容完全是新的，不与先前子主题报告中已涵盖的任何信息重叠。

"现有子主题报告"：
- 现有子主题报告及其部分标题：

    {existing_headers}

- 来自先前子主题报告的现有书面内容：

    {relevant_written_contents}

"结构和格式"：
- 由于这个子报告将是更大报告的一部分，只包括分为适当子主题的主体部分，不包括任何介绍或结论部分。

- 你必须在报告中引用相关URL的地方包含markdown超链接，例如：

    ### 部分标题
    
    这是一个示例文本。([网站URL](url))

- 使用H2作为主要子主题标题（##）和H3作为子部分（###）。
- 使用较小的Markdown标题（例如，H2或H3）进行内容结构，避免使用最大的标题（H1），因为它将用于更大报告的标题。
- 将你的内容组织成不同的部分，这些部分补充但不与现有报告重叠。
- 当向你的报告添加类似或相同的子部分时，你应该清楚地指出新内容与来自先前子主题报告的现有书面内容之间的差异。例如：

    ### 新标题（类似于现有标题）

    虽然前一部分讨论了[主题A]，但本部分将探讨[主题B]。"

"日期"：
如果需要，假设当前日期是{datetime.now(timezone.utc).strftime('%B %d, %Y')}。

"重要！"：
- 你必须用以下语言撰写报告：{language}。
- 重点必须放在主题上！你必须省略任何与之无关的信息！
- 不得有任何介绍、结论、摘要或参考部分。
- 你必须在必要的地方使用markdown语法（[网站URL](url)）包含与句子相关的超链接。
- 如果你添加类似或相同的子部分，你必须在必要的地方在报告中提及现有内容和新内容之间的差异。
- 报告应至少有{total_words}个字。
- 在整个报告中使用{tone.value}的语气。

不要添加结论部分。
"""


def generate_draft_titles_prompt(
    current_subtopic: str,
    main_topic: str,
    context: str,
    max_subsections: int = 5
) -> str:
    return f"""
"上下文"：
"{context}"

"主题和子主题"：
使用最新可用信息，为主题：{main_topic}下的子主题：{current_subtopic}构建详细报告的草稿部分标题。

"任务"：
1. 为子主题报告创建草稿部分标题列表。
2. 每个标题应简洁且与子主题相关。
3. 标题不应太高级，但应足够详细以涵盖子主题的主要方面。
4. 使用markdown语法为标题，使用H3（###），因为H1和H2将用于更大报告的标题。
5. 确保标题涵盖子主题的主要方面。

"结构和格式"：
使用markdown语法以列表格式提供草稿标题，例如：

### 标题1
### 标题2
### 标题3

"重要！"：
- 重点必须放在主题上！你必须省略任何与之无关的信息！
- 不得有任何介绍、结论、摘要或参考部分。
- 仅专注于创建标题，而非内容。
"""


def generate_report_introduction(question: str, research_summary: str = "", language: str = "english") -> str:
    return f"""{research_summary}\n 
使用上述最新信息，准备一份关于主题的详细报告介绍 -- {question}。
- 介绍应简洁、结构良好、信息丰富，使用markdown语法。
- 由于这个介绍将是更大报告的一部分，不要包括通常存在于报告中的任何其他部分。
- 介绍前应有一个带有整个报告适当主题的H1标题。
- 你必须在必要的地方使用markdown语法（[网站URL](url)）包含与句子相关的超链接。
如果需要，假设当前日期是{datetime.now(timezone.utc).strftime('%B %d, %Y')}。
- 输出必须使用{language}语言。
"""


def generate_report_conclusion(query: str, report_content: str, language: str = "english") -> str:
    """
    生成一个简洁的结论，总结研究报告的主要发现和含义。

    参数:
        query (str): 研究任务或问题。
        report_content (str): 研究报告的内容。
        language (str): 结论应使用的语言。

    返回:
        str: 一个简洁的结论，总结报告的主要发现和含义。
    """
    prompt = f"""
    基于以下研究报告和研究任务，请写一个简洁的结论，总结主要发现及其含义：
    
    研究任务: {query}
    
    研究报告: {report_content}

    你的结论应该:
    1. 回顾研究的主要点
    2. 突出最重要的发现
    3. 讨论任何含义或下一步
    4. 长度约为2-3段

    如果报告末尾没有写"## 结论"部分标题，请将其添加到你的结论顶部。
    你必须在必要的地方使用markdown语法（[网站URL](url)）包含与句子相关的超链接。

    重要：整个结论必须用{language}语言撰写。

    写结论：
    """

    return prompt


report_type_mapping = {
    ReportType.ResearchReport.value: generate_report_prompt,
    ReportType.ResourceReport.value: generate_resource_report_prompt,
    ReportType.OutlineReport.value: generate_outline_report_prompt,
    ReportType.CustomReport.value: generate_custom_report_prompt,
    ReportType.SubtopicReport.value: generate_subtopic_report_prompt,
    ReportType.DeepResearch.value: generate_deep_research_prompt,
}


def get_prompt_by_report_type(report_type):
    prompt_by_type = report_type_mapping.get(report_type)
    default_report_type = ReportType.ResearchReport.value
    if not prompt_by_type:
        warnings.warn(
            f"无效的报告类型: {report_type}。\n"
            f"请使用以下之一: {', '.join([enum_value for enum_value in report_type_mapping.keys()])}\n"
            f"使用默认报告类型: {default_report_type} 提示。",
            UserWarning,
        )
        prompt_by_type = report_type_mapping.get(default_report_type)
    return prompt_by_type
