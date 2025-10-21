# Chapter 7: Multi-Agent Collaboration | <mark>第七章：多智能体协作</mark>

While a monolithic agent architecture can be effective for well-defined problems, its capabilities are often constrained when faced with complex, multi-domain tasks. The Multi-Agent Collaboration pattern addresses these limitations by structuring a system as a cooperative ensemble of distinct, specialized agents. This approach is predicated on the principle of task decomposition, where a high-level objective is broken down into discrete sub-problems. Each sub-problem is then assigned to an agent possessing the specific tools, data access, or reasoning capabilities best suited for that task.

<mark>单体智能体架构虽然在处理定义明确的问题时可能有效,但在面对复杂的跨领域任务时,其能力往往受到限制。多智能体协作模式通过将系统构建为由不同专业化智能体组成的协作集合来解决这些局限性。这种方法基于任务分解原则,将高层次目标拆解为若干离散的子问题,然后将每个子问题分配给拥有最适合该任务的特定工具、数据访问权限或推理能力的智能体。</mark>

For example, a complex research query might be decomposed and assigned to a Research Agent for information retrieval, a Data Analysis Agent for statistical processing, and a Synthesis Agent for generating the final report. The efficacy of such a system is not merely due to the division of labor but is critically dependent on the mechanisms for inter-agent communication. This requires a standardized communication protocol and a shared ontology, allowing agents to exchange data, delegate sub-tasks, and coordinate their actions to ensure the final output is coherent.

<mark>例如,一个复杂的研究查询可能被分解并分配给研究智能体负责信息检索、数据分析智能体负责统计处理、综合智能体负责生成最终报告。这类系统的效能不仅源于分工,更关键的是取决于智能体之间的通信机制。这需要标准化的通信协议和共享的本体,使智能体能够交换数据、委派子任务并协调行动,以确保最终输出的连贯性。</mark>

This distributed architecture offers several advantages, including enhanced modularity, scalability, and robustness, as the failure of a single agent does not necessarily cause a total system failure. The collaboration allows for a synergistic outcome where the collective performance of the multi-agent system surpasses the potential capabilities of any single agent within the ensemble.

<mark>这种分布式架构提供了多种优势,包括增强的模块化、可扩展性和鲁棒性,因为单个智能体的故障不一定会导致整个系统失效。协作产生了协同效应,使多智能体系统的整体性能超越了集合中任何单个智能体的潜在能力。</mark>

---

## Multi-Agent Collaboration Pattern Overview | <mark>多智能体协作模式概览</mark>

The Multi-Agent Collaboration pattern involves designing systems where multiple independent or semi-independent agents work together to achieve a common goal. Each agent typically has a defined role, specific goals aligned with the overall objective, and potentially access to different tools or knowledge bases. The power of this pattern lies in the interaction and synergy between these agents.

<mark>多智能体协作模式涉及设计由多个独立或半独立智能体协同工作以实现共同目标的系统。每个智能体通常具有明确的角色、与整体目标一致的具体目标,并可能访问不同的工具或知识库。这种模式的力量在于智能体之间的交互和协同作用。</mark>

Collaboration can take various forms:

<mark>协作可以采取多种形式:</mark>

- **Sequential Handoffs:** One agent completes a task and passes its output to another agent for the next step in a pipeline (similar to the Planning pattern, but explicitly involving different agents).

   <mark><strong>顺序交接:</strong>一个智能体完成任务后将其输出传递给另一个智能体以进行流程中的下一步(类似于规划模式,但明确涉及不同的智能体)。</mark>

- **Parallel Processing:** Multiple agents work on different parts of a problem simultaneously, and their results are later combined.

   <mark><strong>并行处理:</strong>多个智能体同时处理问题的不同部分,之后将其结果合并。</mark>

- **Debate and Consensus:** Multi-Agent Collaboration where Agents with varied perspectives and information sources engage in discussions to evaluate options, ultimately reaching a consensus or a more informed decision.

   <mark><strong>辩论与共识:</strong>具有不同视角和信息来源的智能体进行讨论以评估选项,最终达成共识或做出更明智的决策。</mark>

- **Hierarchical Structures:** A manager agent might delegate tasks to worker agents dynamically based on their tool access or plugin capabilities and synthesize their results. Each agent can also handle relevant groups of tools, rather than a single agent handling all the tools.

   <mark><strong>层级结构:</strong>管理者智能体可能根据工作智能体的工具访问权限或插件能力动态委派任务,并综合其结果。每个智能体还可以处理相关的工具组,而不是由单个智能体处理所有工具。</mark>

- **Expert Teams:** Agents with specialized knowledge in different domains (e.g., a researcher, a writer, an editor) collaborate to produce a complex output.

   <mark><strong>专家团队:</strong>具有不同领域专业知识的智能体(如研究员、作家、编辑)协作产生复杂输出。</mark>

- **Critic-Reviewer:** Agents create initial outputs such as plans, drafts, or answers. A second group of agents then critically assesses this output for adherence to policies, security, compliance, correctness, quality, and alignment with organizational objectives. The original creator or a final agent revises the output based on this feedback. This pattern is particularly effective for code generation, research writing, logic checking, and ensuring ethical alignment. The advantages of this approach include increased robustness, improved quality, and a reduced likelihood of hallucinations or errors.

   <mark><strong>评审者模式:</strong>智能体创建初始输出,如计划、草稿或答案。第二组智能体随后严格评估该输出是否符合政策、安全性、合规性、正确性、质量以及与组织目标的一致性。原始创建者或最终智能体根据此反馈修订输出。这种模式对于代码生成、研究写作、逻辑检查和确保伦理一致性特别有效。这种方法的优势包括增强鲁棒性、提高质量以及减少幻觉或错误的可能性。</mark>

A multi-agent system (see Fig.1) fundamentally comprises the delineation of agent roles and responsibilities, the establishment of communication channels through which agents exchange information, and the formulation of a task flow or interaction protocol that directs their collaborative endeavors.

<mark>多智能体系统(见图 1)从根本上包括划分智能体角色和职责、建立智能体交换信息的通信渠道,以及制定指导其协作努力的任务流或交互协议。</mark>

![Multi-Agent System Example](/images/chapter07_fig1.png)

Fig.1: Example of multi-agent system

<mark>图 1:多智能体系统示例</mark>

Frameworks such as Crew AI and Google ADK are engineered to facilitate this paradigm by providing structures for the specification of agents, tasks, and their interactive procedures. This approach is particularly effective for challenges necessitating a variety of specialized knowledge, encompassing multiple discrete phases, or leveraging the advantages of concurrent processing and the corroboration of information across agents.

<mark>CrewAI 和 Google ADK 等框架旨在通过提供用于指定智能体、任务及其交互程序的结构来促进这种范式。这种方法对于需要各种专业知识、包含多个离散阶段或利用并发处理优势以及智能体之间信息互证的挑战特别有效。</mark>

---

## Practical Applications & Use Cases | <mark>实际应用场景</mark>

Multi-Agent Collaboration is a powerful pattern applicable across numerous domains:

<mark>多智能体协作是一种适用于众多领域的强大模式:</mark>

- **Complex Research and Analysis:** A team of agents could collaborate on a research project. One agent might specialize in searching academic databases, another in summarizing findings, a third in identifying trends, and a fourth in synthesizing the information into a report. This mirrors how a human research team might operate.

   <mark><strong>复杂研究与分析:</strong>智能体团队可以协作完成研究项目。一个智能体可能专门搜索学术数据库,另一个负责总结发现,第三个识别趋势,第四个将信息综合成报告。这反映了人类研究团队的运作方式。</mark>

- **Software Development:** Imagine agents collaborating on building software. One agent could be a requirements analyst, another a code generator, a third a tester, and a fourth a documentation writer. They could pass outputs between each other to build and verify components.

   <mark><strong>软件开发:</strong>可以想象智能体协作构建软件。一个智能体可能是需求分析师,另一个是代码生成器,第三个是测试人员,第四个是文档编写者。它们可以相互传递输出以构建和验证组件。</mark>

- **Creative Content Generation:** Creating a marketing campaign could involve a market research agent, a copywriter agent, a graphic design agent (using image generation tools), and a social media scheduling agent, all working together.

   <mark><strong>创意内容生成:</strong>创建营销活动可能涉及市场研究智能体、文案撰写智能体、图形设计智能体(使用图像生成工具)和社交媒体排期智能体,所有这些智能体协同工作。</mark>

- **Financial Analysis:** A multi-agent system could analyze financial markets. Agents might specialize in fetching stock data, analyzing news sentiment, performing technical analysis, and generating investment recommendations.

   <mark><strong>财务分析:</strong>多智能体系统可以分析金融市场。智能体可能专门获取股票数据、分析新闻情绪、执行技术分析并生成投资建议。</mark>

- **Customer Support Escalation:** A front-line support agent could handle initial queries, escalating complex issues to a specialist agent (e.g., a technical expert or a billing specialist) when needed, demonstrating a sequential handoff based on problem complexity.

   <mark><strong>客户支持升级:</strong>一线支持智能体可以处理初始查询,在需要时将复杂问题升级到专业智能体(如技术专家或计费专家),展示了基于问题复杂性的顺序交接。</mark>

- **Supply Chain Optimization:** Agents could represent different nodes in a supply chain (suppliers, manufacturers, distributors) and collaborate to optimize inventory levels, logistics, and scheduling in response to changing demand or disruptions.

   <mark><strong>供应链优化:</strong>智能体可以代表供应链中的不同节点(供应商、制造商、分销商),并协作优化库存水平、物流和排期,以应对不断变化的需求或中断。</mark>

- **Network Analysis & Remediation:** Autonomous operations benefit greatly from an agentic architecture, particularly in failure pinpointing. Multiple agents can collaborate to triage and remediate issues, suggesting optimal actions. These agents can also integrate with traditional machine learning models and tooling, leveraging existing systems while simultaneously offering the advantages of Generative AI.

   <mark><strong>网络分析与修复:</strong>自主运营从智能体架构中受益匪浅,特别是在故障定位方面。多个智能体可以协作进行问题分类和修复,建议最佳操作。这些智能体还可以与传统机器学习模型和工具集成,在利用现有系统的同时提供生成式 AI 的优势。</mark>

The capacity to delineate specialized agents and meticulously orchestrate their interrelationships empowers developers to construct systems exhibiting enhanced modularity, scalability, and the ability to address complexities that would prove insurmountable for a singular, integrated agent.

<mark>划分专业化智能体并精心编排其相互关系的能力,使开发者能够构建具有增强模块化、可扩展性以及能够解决单一集成智能体无法克服的复杂性的系统。</mark>

---

## Multi-Agent Collaboration: Exploring Interrelationships and Communication Structures | <mark>多智能体协作:探索相互关系和通信结构</mark>

Understanding the intricate ways in which agents interact and communicate is fundamental to designing effective multi-agent systems. As depicted in Fig. 2, a spectrum of interrelationship and communication models exists, ranging from the simplest single-agent scenario to complex, custom-designed collaborative frameworks. Each model presents unique advantages and challenges, influencing the overall efficiency, robustness, and adaptability of the multi-agent system.

<mark>理解智能体交互和通信的复杂方式对于设计有效的多智能体系统至关重要。如图 2 所示,存在从最简单的单智能体场景到复杂的定制协作框架的一系列相互关系和通信模型。每种模型都具有独特的优势和挑战,影响多智能体系统的整体效率、鲁棒性和适应性。</mark>

### 1. Single Agent | <mark>单智能体</mark>

At the most basic level, a "Single Agent" operates autonomously without direct interaction or communication with other entities. While this model is straightforward to implement and manage, its capabilities are inherently limited by the individual agent's scope and resources. It is suitable for tasks that are decomposable into independent sub-problems, each solvable by a single, self-sufficient agent.

<mark>在最基本的层面上,「单智能体」自主运行,不与其他实体进行直接交互或通信。虽然这种模型易于实现和管理,但其能力本质上受到单个智能体范围和资源的限制。它适用于可分解为独立子问题的任务,每个子问题都可由单个自给自足的智能体解决。</mark>

### 2. Network | <mark>网络</mark>

The "Network" model represents a significant step towards collaboration, where multiple agents interact directly with each other in a decentralized fashion. Communication typically occurs peer-to-peer, allowing for the sharing of information, resources, and even tasks. This model fosters resilience, as the failure of one agent does not necessarily cripple the entire system. However, managing communication overhead and ensuring coherent decision-making in a large, unstructured network can be challenging.

<mark>「网络」模型代表了向协作迈出的重要一步,多个智能体以去中心化的方式直接相互交互。通信通常以点对点方式进行,允许共享信息、资源甚至任务。这种模型增强了弹性,因为一个智能体的故障不一定会使整个系统瘫痪。然而,在大型非结构化网络中管理通信开销和确保连贯的决策可能具有挑战性。</mark>

### 3. Supervisor | <mark>监督者</mark>

In the "Supervisor" model, a dedicated agent, the "supervisor," oversees and coordinates the activities of a group of subordinate agents. The supervisor acts as a central hub for communication, task allocation, and conflict resolution. This hierarchical structure offers clear lines of authority and can simplify management and control. However, it introduces a single point of failure (the supervisor) and can become a bottleneck if the supervisor is overwhelmed by a large number of subordinates or complex tasks.

<mark>在「监督者」模型中,专门的智能体即「监督者」负责监督和协调一组下属智能体的活动。监督者充当通信、任务分配和冲突解决的中心枢纽。这种层级结构提供了明确的权力线,可以简化管理和控制。然而,它引入了单点故障(监督者),如果监督者被大量下属或复杂任务所淹没,可能会成为瓶颈。</mark>

### 4. Supervisor as a Tool | <mark>监督者作为工具</mark>

This model is a nuanced extension of the "Supervisor" concept, where the supervisor's role is less about direct command and control and more about providing resources, guidance, or analytical support to other agents. The supervisor might offer tools, data, or computational services that enable other agents to perform their tasks more effectively, without necessarily dictating their every action. This approach aims to leverage the supervisor's capabilities without imposing rigid top-down control.

<mark>这种模型是「监督者」概念的细微扩展,监督者的角色不太关注直接命令和控制,而更多关注为其他智能体提供资源、指导或分析支持。监督者可能提供工具、数据或计算服务,使其他智能体能够更有效地执行任务,而不必指示其每个操作。这种方法旨在利用监督者的能力,而不强加严格的自上而下控制。</mark>

### 5. Hierarchical | <mark>层级</mark>

The "Hierarchical" model expands upon the supervisor concept to create a multi-layered organizational structure. This involves multiple levels of supervisors, with higher-level supervisors overseeing lower-level ones, and ultimately, a collection of operational agents at the lowest tier. This structure is well-suited for complex problems that can be decomposed into sub-problems, each managed by a specific layer of the hierarchy. It provides a structured approach to scalability and complexity management, allowing for distributed decision-making within defined boundaries.

<mark>「层级」模型扩展了监督者概念,创建了多层组织结构。这涉及多个级别的监督者,高级监督者监督低级监督者,最终在最低层有一组操作智能体。这种结构非常适合可以分解为子问题的复杂问题,每个子问题由层级结构的特定层管理。它提供了一种结构化的可扩展性和复杂性管理方法,允许在定义的边界内进行分布式决策。</mark>

![Agent Communication Models](/images/chapter07_fig2.png)

Fig. 2: Agents communicate and interact in various ways.

<mark>图 2:智能体以各种方式进行通信和交互。</mark>

### 6. Custom | <mark>自定义</mark>

The "Custom" model represents the ultimate flexibility in multi-agent system design. It allows for the creation of unique interrelationship and communication structures tailored precisely to the specific requirements of a given problem or application. This can involve hybrid approaches that combine elements from the previously mentioned models, or entirely novel designs that emerge from the unique constraints and opportunities of the environment. Custom models often arise from the need to optimize for specific performance metrics, handle highly dynamic environments, or incorporate domain-specific knowledge into the system's architecture. Designing and implementing custom models typically requires a deep understanding of multi-agent systems principles and careful consideration of communication protocols, coordination mechanisms, and emergent behaviors.

<mark>「自定义」模型代表了多智能体系统设计的终极灵活性。它允许创建独特的相互关系和通信结构,精确地针对给定问题或应用的特定要求进行定制。这可能涉及结合前述模型元素的混合方法,或从环境的独特约束和机会中产生的全新设计。自定义模型通常源于优化特定性能指标、处理高度动态环境或将领域特定知识纳入系统架构的需求。设计和实现自定义模型通常需要对多智能体系统原理有深刻理解,并仔细考虑通信协议、协调机制和涌现行为。</mark>

In summary, the choice of interrelationship and communication model for a multi-agent system is a critical design decision. Each model offers distinct advantages and disadvantages, and the optimal choice depends on factors such as the complexity of the task, the number of agents, the desired level of autonomy, the need for robustness, and the acceptable communication overhead. Future advancements in multi-agent systems will likely continue to explore and refine these models, as well as develop new paradigms for collaborative intelligence.

<mark>总之,为多智能体系统选择相互关系和通信模型是一个关键的设计决策。每种模型都具有独特的优势和劣势,最佳选择取决于任务的复杂性、智能体数量、所需的自主性水平、鲁棒性需求以及可接受的通信开销等因素。多智能体系统的未来进展可能会继续探索和完善这些模型,并开发协作智能的新范式。</mark>

---

## Hands-On code (Crew AI) | <mark>实战代码:使用 CrewAI</mark>

This Python code defines an AI-powered crew using the CrewAI framework to generate a blog post about AI trends. It starts by setting up the environment, loading API keys from a .env file. The core of the application involves defining two agents: a researcher to find and summarize AI trends, and a writer to create a blog post based on the research.

<mark>这段 Python 代码使用 CrewAI 框架定义了一个由 AI 驱动的团队来生成关于 AI 趋势的博客文章。它首先设置环境,从 <code>.env</code> 文件加载 API 密钥。应用的核心涉及定义两个智能体:一个研究员负责查找和总结 AI 趋势,一个作家负责基于研究创建博客文章。</mark>

Two tasks are defined accordingly: one for researching the trends and another for writing the blog post, with the writing task depending on the output of the research task. These agents and tasks are then assembled into a Crew, specifying a sequential process where tasks are executed in order. The Crew is initialized with the agents, tasks, and a language model (specifically the "gemini-2.0-flash" model). The main function executes this crew using the kickoff() method, orchestrating the collaboration between the agents to produce the desired output. Finally, the code prints the final result of the crew's execution, which is the generated blog post.

<mark>相应地定义了两个任务:一个用于研究趋势,另一个用于撰写博客文章,写作任务依赖于研究任务的输出。然后将这些智能体和任务组装成一个 Crew,指定按顺序执行任务的顺序流程。Crew 使用智能体、任务和语言模型(特别是 <code>gemini-2.0-flash</code> 模型)进行初始化。主函数使用 <code>kickoff()</code> 方法执行此 Crew,编排智能体之间的协作以产生所需的输出。最后,代码打印 Crew 执行的最终结果,即生成的博客文章。</mark>

```python
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

def setup_environment():
   """Loads environment variables and checks for the required API key."""
   # 加载环境变量并检查所需的 API 密钥
   load_dotenv()
   if not os.getenv("GOOGLE_API_KEY"):
       raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")

def main():
   """
   Initializes and runs the AI crew for content creation using the latest Gemini model.
   """
   # 使用最新的 Gemini 模型初始化并运行用于内容创建的 AI 团队
   setup_environment()

   # Define the language model to use.
   # Updated to a model from the Gemini 2.0 series for better performance and features.
   # For cutting-edge (preview) capabilities, you could use "gemini-2.5-flash".
   # 定义要使用的语言模型
   # 更新为 Gemini 2.0 系列的模型以获得更好的性能和功能
   # 如需前沿（预览）功能，可以使用 "gemini-2.5-flash"
   llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

   # Define Agents with specific roles and goals
   # 定义具有特定角色和目标的智能体
   researcher = Agent(
       role='Senior Research Analyst',
       goal='Find and summarize the latest trends in AI.',
       backstory="You are an experienced research analyst with a knack for identifying key trends and synthesizing information.",
       verbose=True,
       allow_delegation=False,
   )

   writer = Agent(
       role='Technical Content Writer',
       goal='Write a clear and engaging blog post based on research findings.',
       backstory="You are a skilled writer who can translate complex technical topics into accessible content.",
       verbose=True,
       allow_delegation=False,
   )

   # Define Tasks for the agents
   # 为智能体定义任务
   research_task = Task(
       description="Research the top 3 emerging trends in Artificial Intelligence in 2024-2025. Focus on practical applications and potential impact.",
       expected_output="A detailed summary of the top 3 AI trends, including key points and sources.",
       agent=researcher,
   )

   writing_task = Task(
       description="Write a 500-word blog post based on the research findings. The post should be engaging and easy for a general audience to understand.",
       expected_output="A complete 500-word blog post about the latest AI trends.",
       agent=writer,
       context=[research_task],
   )

   # Create the Crew
   # 创建 Crew
   blog_creation_crew = Crew(
       agents=[researcher, writer],
       tasks=[research_task, writing_task],
       process=Process.sequential,
       llm=llm,
       verbose=2 # Set verbosity for detailed crew execution logs
   )

   # Execute the Crew
   # 执行 Crew
   print("## Running the blog creation crew with Gemini 2.0 Flash... ##")
   try:
       result = blog_creation_crew.kickoff()
       print("\n------------------\n")
       print("## Crew Final Output ##")
       print(result)
   except Exception as e:
       print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
   main()
```

We will now delve into further examples within the Google ADK framework, with particular emphasis on hierarchical, parallel, and sequential coordination paradigms, alongside the implementation of an agent as an operational instrument.

<mark>我们现在将深入探讨 Google ADK 框架内的更多示例,特别强调层级、并行和顺序协调范式,以及将智能体实现为操作工具。</mark>

---

## Hands-on Code (Google ADK) | <mark>实战代码:使用 Google ADK</mark>

The following code example demonstrates the establishment of a hierarchical agent structure within the Google ADK through the creation of a parent-child relationship. The code defines two types of agents: LlmAgent and a custom TaskExecutor agent derived from BaseAgent. The TaskExecutor is designed for specific, non-LLM tasks and in this example, it simply yields a "Task finished successfully" event. An LlmAgent named greeter is initialized with a specified model and instruction to act as a friendly greeter. The custom TaskExecutor is instantiated as task_doer. A parent LlmAgent called coordinator is created, also with a model and instructions. The coordinator's instructions guide it to delegate greetings to the greeter and task execution to the task_doer. The greeter and task_doer are added as sub-agents to the coordinator, establishing a parent-child relationship. The code then asserts that this relationship is correctly set up. Finally, it prints a message indicating that the agent hierarchy has been successfully created.

<mark>以下代码示例演示了如何通过创建父子关系在 Google ADK 中建立层级智能体结构。代码定义了两种类型的智能体:<code>LlmAgent</code> 和从 <code>BaseAgent</code> 派生的自定义 <code>TaskExecutor</code> 智能体。<code>TaskExecutor</code> 专为特定的非 LLM 任务而设计,在此示例中,它只是产生一个「任务成功完成」事件。名为 <code>greeter</code> 的 <code>LlmAgent</code> 使用指定的模型和指令进行初始化,充当友好的问候者。自定义 <code>TaskExecutor</code> 被实例化为 <code>task_doer</code>。创建名为 <code>coordinator</code> 的父 <code>LlmAgent</code>,同样具有模型和指令。<code>coordinator</code> 的指令指导它将问候委托给 <code>greeter</code>,将任务执行委托给 <code>task_doer</code>。将 <code>greeter</code> 和 <code>task_doer</code> 作为子智能体添加到 <code>coordinator</code>,建立父子关系。然后代码断言此关系已正确设置。最后,它打印一条消息,指示已成功创建智能体层级结构。</mark>

```python
from google.adk.agents import LlmAgent, BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator

# Correctly implement a custom agent by extending BaseAgent
# 通过扩展 BaseAgent 正确实现自定义智能体
class TaskExecutor(BaseAgent):
   """A specialized agent with custom, non-LLM behavior."""
   # 具有自定义非 LLM 行为的专业智能体
   name: str = "TaskExecutor"
   description: str = "Executes a predefined task."

   async def _run_async_impl(self, context: InvocationContext) -> AsyncGenerator[Event, None]:
       """Custom implementation logic for the task."""
       # 任务的自定义实现逻辑
       # This is where your custom logic would go.
       # For this example, we'll just yield a simple event.
       # 这里是你的自定义逻辑所在
       # 在这个示例中，我们只是产生一个简单的事件
       yield Event(author=self.name, content="Task finished successfully.")

# Define individual agents with proper initialization
# LlmAgent requires a model to be specified.
# 定义具有正确初始化的各个智能体
# LlmAgent 需要指定模型
greeter = LlmAgent(
   name="Greeter",
   model="gemini-2.0-flash-exp",
   instruction="You are a friendly greeter."
)
task_doer = TaskExecutor() # Instantiate our concrete custom agent
                            # 实例化我们的具体自定义智能体

# Create a parent agent and assign its sub-agents
# The parent agent's description and instructions should guide its delegation logic.
# 创建父智能体并分配其子智能体
# 父智能体的描述和指令应指导其委派逻辑
coordinator = LlmAgent(
   name="Coordinator",
   model="gemini-2.0-flash-exp",
   description="A coordinator that can greet users and execute tasks.",
   instruction="When asked to greet, delegate to the Greeter. When asked to perform a task, delegate to the TaskExecutor.",
   sub_agents=[
       greeter,
       task_doer
   ]
)

# The ADK framework automatically establishes the parent-child relationships.
# These assertions will pass if checked after initialization.
# ADK 框架自动建立父子关系
# 如果在初始化后检查，这些断言将通过
assert greeter.parent_agent == coordinator
assert task_doer.parent_agent == coordinator

print("Agent hierarchy created successfully.")
```

This code excerpt illustrates the employment of the LoopAgent within the Google ADK framework to establish iterative workflows. The code defines two agents: ConditionChecker and ProcessingStep. ConditionChecker is a custom agent that checks a "status" value in the session state. If the "status" is "completed", ConditionChecker escalates an event to stop the loop. Otherwise, it yields an event to continue the loop. ProcessingStep is an LlmAgent using the "gemini-2.0-flash-exp" model. Its instruction is to perform a task and set the session "status" to "completed" if it's the final step. A LoopAgent named StatusPoller is created. StatusPoller is configured with max_iterations=10. StatusPoller includes both ProcessingStep and an instance of ConditionChecker as sub-agents. The LoopAgent will execute the sub-agents sequentially for up to 10 iterations, stopping if ConditionChecker finds the status is "completed".

<mark>这段代码摘录说明了在 Google ADK 框架中使用 <code>LoopAgent</code> 来建立迭代工作流。代码定义了两个智能体:<code>ConditionChecker</code> 和 <code>ProcessingStep</code>。<code>ConditionChecker</code> 是一个自定义智能体,用于检查会话状态中的「status」值。如果「status」为「completed」,<code>ConditionChecker</code> 会升级事件以停止循环。否则,它会产生事件以继续循环。<code>ProcessingStep</code> 是使用 <code>gemini-2.0-flash-exp</code> 模型的 <code>LlmAgent</code>。其指令是执行任务,如果是最后一步,则将会话「status」设置为「completed」。创建名为 <code>StatusPoller</code> 的 <code>LoopAgent</code>。<code>StatusPoller</code> 配置为 <code>max_iterations=10</code>。<code>StatusPoller</code> 包括 <code>ProcessingStep</code> 和 <code>ConditionChecker</code> 实例作为子智能体。<code>LoopAgent</code> 将顺序执行子智能体最多 10 次迭代,如果 <code>ConditionChecker</code> 发现状态为「completed」则停止。</mark>

```python
import asyncio
from typing import AsyncGenerator
from google.adk.agents import LoopAgent, LlmAgent, BaseAgent
from google.adk.events import Event, EventActions
from google.adk.agents.invocation_context import InvocationContext

# Best Practice: Define custom agents as complete, self-describing classes.
# 最佳实践：将自定义智能体定义为完整的、自描述的类
class ConditionChecker(BaseAgent):
   """A custom agent that checks for a 'completed' status in the session state."""
   # 检查会话状态中是否有「completed」状态的自定义智能体
   name: str = "ConditionChecker"
   description: str = "Checks if a process is complete and signals the loop to stop."

   async def _run_async_impl(
       self, context: InvocationContext
   ) -> AsyncGenerator[Event, None]:
       """Checks state and yields an event to either continue or stop the loop."""
       # 检查状态并产生事件以继续或停止循环
       status = context.session.state.get("status", "pending")
       is_done = (status == "completed")

       if is_done:
           # Escalate to terminate the loop when the condition is met.
           # 满足条件时升级以终止循环
           yield Event(author=self.name, actions=EventActions(escalate=True))
       else:
           # Yield a simple event to continue the loop.
           # 产生简单事件以继续循环
           yield Event(author=self.name, content="Condition not met, continuing loop.")

# Correction: The LlmAgent must have a model and clear instructions.
# 更正：LlmAgent 必须有模型和清晰的指令
process_step = LlmAgent(
   name="ProcessingStep",
   model="gemini-2.0-flash-exp",
   instruction="You are a step in a longer process. Perform your task. If you are the final step, update session state by setting 'status' to 'completed'."
)

# The LoopAgent orchestrates the workflow.
# LoopAgent 编排工作流
poller = LoopAgent(
   name="StatusPoller",
   max_iterations=10,
   sub_agents=[
       process_step,
       ConditionChecker() # Instantiating the well-defined custom agent.
                          # 实例化定义良好的自定义智能体
   ]
)

# This poller will now execute 'process_step'
# and then 'ConditionChecker'
# repeatedly until the status is 'completed' or 10 iterations
# have passed.
# 此轮询器现在将执行 'process_step'
# 然后执行 'ConditionChecker'
# 重复执行直到状态为 'completed' 或已经过 10 次迭代
```

This code excerpt elucidates the SequentialAgent pattern within the Google ADK, engineered for the construction of linear workflows. This code defines a sequential agent pipeline using the google.adk.agents library. The pipeline consists of two agents, step1 and step2. step1 is named "Step1_Fetch" and its output will be stored in the session state under the key "data". step2 is named "Step2_Process" and is instructed to analyze the information stored in session.state["data"] and provide a summary. The SequentialAgent named "MyPipeline" orchestrates the execution of these sub-agents. When the pipeline is run with an initial input, step1 will execute first. The response from step1 will be saved into the session state under the key "data". Subsequently, step2 will execute, utilizing the information that step1 placed into the state as per its instruction. This structure allows for building workflows where the output of one agent becomes the input for the next. This is a common pattern in creating multi-step AI or data processing pipelines.

<mark>这段代码摘录阐明了 Google ADK 中的 <code>SequentialAgent</code> 模式,专为构建线性工作流而设计。此代码使用 <code>google.adk.agents</code> 库定义了一个顺序智能体管道。管道由两个智能体组成:<code>step1</code> 和 <code>step2</code>。<code>step1</code> 命名为「Step1_Fetch」,其输出将存储在会话状态中的「data」键下。<code>step2</code> 命名为「Step2_Process」,被指示分析存储在 <code>session.state["data"]</code> 中的信息并提供摘要。名为「MyPipeline」的 <code>SequentialAgent</code> 编排这些子智能体的执行。当使用初始输入运行管道时,<code>step1</code> 将首先执行。来自 <code>step1</code> 的响应将保存到会话状态中的「data」键下。随后,<code>step2</code> 将执行,根据其指令利用 <code>step1</code> 放入状态中的信息。这种结构允许构建工作流,其中一个智能体的输出成为下一个智能体的输入。这是创建多步骤 AI 或数据处理管道的常见模式。</mark>

```python
from google.adk.agents import SequentialAgent, Agent

# This agent's output will be saved to session.state["data"]
# 此智能体的输出将保存到 session.state["data"]
step1 = Agent(name="Step1_Fetch", output_key="data")

# This agent will use the data from the previous step.
# We instruct it on how to find and use this data.
# 此智能体将使用上一步的数据
# 我们指示它如何查找和使用这些数据
step2 = Agent(
   name="Step2_Process",
   instruction="Analyze the information found in state['data'] and provide a summary."
)

pipeline = SequentialAgent(
   name="MyPipeline",
   sub_agents=[step1, step2]
)

# When the pipeline is run with an initial input, Step1 will execute,
# its response will be stored in session.state["data"], and then
# Step2 will execute, using the information from the state as instructed.
# 当使用初始输入运行管道时，Step1 将执行，
# 其响应将存储在 session.state["data"] 中，然后
# Step2 将执行，按照指示使用状态中的信息
```

The following code example illustrates the ParallelAgent pattern within the Google ADK, which facilitates the concurrent execution of multiple agent tasks. The data_gatherer is designed to run two sub-agents concurrently: weather_fetcher and news_fetcher. The weather_fetcher agent is instructed to get the weather for a given location and store the result in session.state["weather_data"]. Similarly, the news_fetcher agent is instructed to retrieve the top news story for a given topic and store it in session.state["news_data"]. Each sub-agent is configured to use the "gemini-2.0-flash-exp" model. The ParallelAgent orchestrates the execution of these sub-agents, allowing them to work in parallel. The results from both weather_fetcher and news_fetcher would be gathered and stored in the session state. Finally, the example shows how to access the collected weather and news data from the final_state after the agent's execution is complete.

<mark>以下代码示例说明了 Google ADK 中的 <code>ParallelAgent</code> 模式,它促进了多个智能体任务的并发执行。<code>data_gatherer</code> 旨在并发运行两个子智能体:<code>weather_fetcher</code> 和 <code>news_fetcher</code>。<code>weather_fetcher</code> 智能体被指示获取给定位置的天气并将结果存储在 <code>session.state["weather_data"]</code> 中。类似地,<code>news_fetcher</code> 智能体被指示检索给定主题的头条新闻并将其存储在 <code>session.state["news_data"]</code> 中。每个子智能体都配置为使用 <code>gemini-2.0-flash-exp</code> 模型。<code>ParallelAgent</code> 编排这些子智能体的执行,允许它们并行工作。来自 <code>weather_fetcher</code> 和 <code>news_fetcher</code> 的结果将被收集并存储在会话状态中。最后,示例展示了如何在智能体执行完成后从 <code>final_state</code> 访问收集的天气和新闻数据。</mark>

```python
from google.adk.agents import Agent, ParallelAgent

# It's better to define the fetching logic as tools for the agents
# For simplicity in this example, we'll embed the logic in the agent's instruction.
# In a real-world scenario, you would use tools.
# 最好将获取逻辑定义为智能体的工具
# 为了简单起见，在这个示例中，我们将逻辑嵌入到智能体的指令中
# 在实际场景中，你应该使用工具

# Define the individual agents that will run in parallel
# 定义将并行运行的各个智能体
weather_fetcher = Agent(
   name="weather_fetcher",
   model="gemini-2.0-flash-exp",
   instruction="Fetch the weather for the given location and return only the weather report.",
   output_key="weather_data"  # The result will be stored in session.state["weather_data"]
                              # 结果将存储在 session.state["weather_data"]
)

news_fetcher = Agent(
   name="news_fetcher",
   model="gemini-2.0-flash-exp",
   instruction="Fetch the top news story for the given topic and return only that story.",
   output_key="news_data"      # The result will be stored in session.state["news_data"]
                              # 结果将存储在 session.state["news_data"]
)

# Create the ParallelAgent to orchestrate the sub-agents
# 创建 ParallelAgent 以编排子智能体
data_gatherer = ParallelAgent(
   name="data_gatherer",
   sub_agents=[
       weather_fetcher,
       news_fetcher
   ]
)
```

The provided code segment exemplifies the "Agent as a Tool" paradigm within the Google ADK, enabling an agent to utilize the capabilities of another agent in a manner analogous to function invocation. Specifically, the code defines an image generation system using Google's LlmAgent and AgentTool classes. It consists of two agents: a parent artist_agent and a sub-agent image_generator_agent. The generate_image function is a simple tool that simulates image creation, returning mock image data. The image_generator_agent is responsible for using this tool based on a text prompt it receives. The artist_agent's role is to first invent a creative image prompt. It then calls the image_generator_agent through an AgentTool wrapper. The AgentTool acts as a bridge, allowing one agent to use another agent as a tool. When the artist_agent calls the image_tool, the AgentTool invokes the image_generator_agent with the artist's invented prompt. The image_generator_agent then uses the generate_image function with that prompt. Finally, the generated image (or mock data) is returned back up through the agents. This architecture demonstrates a layered agent system where a higher-level agent orchestrates a lower-level, specialized agent to perform a task.

<mark>提供的代码段示例说明了 Google ADK 中的「智能体作为工具」范式,使智能体能够以类似于函数调用的方式利用另一个智能体的能力。具体来说,代码使用 Google 的 <code>LlmAgent</code> 和 <code>AgentTool</code> 类定义了一个图像生成系统。它由两个智能体组成:父智能体 <code>artist_agent</code> 和子智能体 <code>image_generator_agent</code>。<code>generate_image</code> 函数是一个简单的工具,模拟图像创建,返回模拟图像数据。<code>image_generator_agent</code> 负责根据接收到的文本提示使用此工具。<code>artist_agent</code> 的角色首先是发明创意图像提示。然后通过 <code>AgentTool</code> 包装器调用 <code>image_generator_agent</code>。<code>AgentTool</code> 充当桥梁,允许一个智能体将另一个智能体用作工具。当 <code>artist_agent</code> 调用 <code>image_tool</code> 时,<code>AgentTool</code> 使用艺术家发明的提示调用 <code>image_generator_agent</code>。然后 <code>image_generator_agent</code> 使用该提示调用 <code>generate_image</code> 函数。最后,生成的图像(或模拟数据)通过智能体返回。此架构演示了一个分层智能体系统,其中高级智能体编排低级专业智能体来执行任务。</mark>

```python
from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.genai import types

# 1. A simple function tool for the core capability.
# This follows the best practice of separating actions from reasoning.
# 1. 核心功能的简单函数工具
# 这遵循将操作与推理分离的最佳实践
def generate_image(prompt: str) -> dict:
   """
   Generates an image based on a textual prompt.

   Args:
       prompt: A detailed description of the image to generate.

   Returns:
       A dictionary with the status and the generated image bytes.
   """
   # 基于文本提示生成图像
   #
   # 参数:
   #     prompt: 要生成的图像的详细描述
   #
   # 返回:
   #     包含状态和生成的图像字节的字典
   print(f"TOOL: Generating image for prompt: '{prompt}'")
   # In a real implementation, this would call an image generation API.
   # For this example, we return mock image data.
   # 在实际实现中，这将调用图像生成 API
   # 在这个示例中，我们返回模拟图像数据
   mock_image_bytes = b"mock_image_data_for_a_cat_wearing_a_hat"
   return {
       "status": "success",
       # The tool returns the raw bytes, the agent will handle the Part creation.
       # 工具返回原始字节，智能体将处理 Part 创建
       "image_bytes": mock_image_bytes,
       "mime_type": "image/png"
   }

# 2. Refactor the ImageGeneratorAgent into an LlmAgent.
# It now correctly uses the input passed to it.
# 2. 将 ImageGeneratorAgent 重构为 LlmAgent
# 它现在正确使用传递给它的输入
image_generator_agent = LlmAgent(
   name="ImageGen",
   model="gemini-2.0-flash",
   description="Generates an image based on a detailed text prompt.",
   instruction=(
       "You are an image generation specialist. Your task is to take the user's request "
       "and use the `generate_image` tool to create the image. "
       "The user's entire request should be used as the 'prompt' argument for the tool. "
       "After the tool returns the image bytes, you MUST output the image."
   ),
   tools=[generate_image]
)

# 3. Wrap the corrected agent in an AgentTool.
# The description here is what the parent agent sees.
# 3. 将修正后的智能体包装在 AgentTool 中
# 这里的描述是父智能体看到的内容
image_tool = agent_tool.AgentTool(
   agent=image_generator_agent,
   description="Use this tool to generate an image. The input should be a descriptive prompt of the desired image."
)

# 4. The parent agent remains unchanged. Its logic was correct.
# 4. 父智能体保持不变。其逻辑是正确的
artist_agent = LlmAgent(
   name="Artist",
   model="gemini-2.0-flash",
   instruction=(
       "You are a creative artist. First, invent a creative and descriptive prompt for an image. "
       "Then, use the `ImageGen` tool to generate the image using your prompt."
   ),
   tools=[image_tool]
)
```

---

## At a Glance | <mark>要点速览</mark>

**What:** Complex problems often exceed the capabilities of a single, monolithic LLM-based agent. A solitary agent may lack the diverse, specialized skills or access to the specific tools needed to address all parts of a multifaceted task. This limitation creates a bottleneck, reducing the system's overall effectiveness and scalability. As a result, tackling sophisticated, multi-domain objectives becomes inefficient and can lead to incomplete or suboptimal outcomes.

<mark><strong>问题所在:</strong>复杂问题往往超出单个单体 LLM 智能体的能力范围。单一智能体可能缺乏处理多方面任务所有部分所需的多样化专业技能或特定工具访问权限。这种限制造成了瓶颈,降低了系统的整体有效性和可扩展性。因此,处理复杂的多领域目标变得低效,可能导致不完整或次优的结果。</mark>

**Why:** The Multi-Agent Collaboration pattern offers a standardized solution by creating a system of multiple, cooperating agents. A complex problem is broken down into smaller, more manageable sub-problems. Each sub-problem is then assigned to a specialized agent with the precise tools and capabilities required to solve it. These agents work together through defined communication protocols and interaction models like sequential handoffs, parallel workstreams, or hierarchical delegation. This agentic, distributed approach creates a synergistic effect, allowing the group to achieve outcomes that would be impossible for any single agent.

<mark><strong>解决之道:</strong>多智能体协作模式通过创建一个由多个协作智能体组成的系统来提供标准化解决方案。复杂问题被分解为更小、更易管理的子问题。然后将每个子问题分配给具有解决该问题所需的精确工具和能力的专业智能体。这些智能体通过定义的通信协议和交互模型(如顺序交接、并行工作流或层级委派)协同工作。这种智能体式的分布式方法产生了协同效应,使团队能够实现任何单个智能体都无法实现的成果。</mark>

**Rule of thumb:** Use this pattern when a task is too complex for a single agent and can be decomposed into distinct sub-tasks requiring specialized skills or tools. It is ideal for problems that benefit from diverse expertise, parallel processing, or a structured workflow with multiple stages, such as complex research and analysis, software development, or creative content generation.

<mark><strong>经验法则:</strong>当任务对于单个智能体来说过于复杂且可以分解为需要专业技能或工具的不同子任务时,使用此模式。它非常适合从多样化专业知识、并行处理或具有多个阶段的结构化工作流中受益的问题,例如复杂的研究与分析、软件开发或创意内容生成。</mark>

**Visual summary:** | <mark>可视化总结:</mark>

![Multi-Agent Design Pattern](/images/chapter07_fig3.png)

Fig.3: Multi-Agent design pattern

<mark>图 3:多智能体设计模式</mark>

---

## Key Takeaways | <mark>核心要点</mark>

- Multi-agent collaboration involves multiple agents working together to achieve a common goal.

   <mark>多智能体协作涉及多个智能体协同工作以实现共同目标。</mark>

- This pattern leverages specialized roles, distributed tasks, and inter-agent communication.

   <mark>此模式利用专业化角色、分布式任务和智能体间通信。</mark>

- Collaboration can take forms like sequential handoffs, parallel processing, debate, or hierarchical structures.

   <mark>协作可以采取顺序交接、并行处理、辩论或层级结构等形式。</mark>

- This pattern is ideal for complex problems requiring diverse expertise or multiple distinct stages.

   <mark>此模式非常适合需要多样化专业知识或多个不同阶段的复杂问题。</mark>

---

## Conclusion | <mark>结语</mark>

This chapter explored the Multi-Agent Collaboration pattern, demonstrating the benefits of orchestrating multiple specialized agents within systems. We examined various collaboration models, emphasizing the pattern's essential role in addressing complex, multifaceted problems across diverse domains. Understanding agent collaboration naturally leads to an inquiry into their interactions with the external environment.

<mark>本章探讨了多智能体协作模式,展示了在系统内编排多个专业智能体的优势。我们检查了各种协作模型,强调了该模式在解决跨各领域复杂多面问题中的关键作用。理解智能体协作自然会引发对其与外部环境交互的探究。</mark>

---

## References | <mark>参考文献</mark>

1. Multi-Agent Collaboration Mechanisms: A Survey of LLMs, https://arxiv.org/abs/2501.06322

   <mark>多智能体协作机制:大语言模型调研,https://arxiv.org/abs/2501.06322</mark>

2. Multi-Agent System — The Power of Collaboration, https://aravindakumar.medium.com/introducing-multi-agent-frameworks-the-power-of-collaboration-e9db31bba1b6

   <mark>多智能体系统——协作的力量,https://aravindakumar.medium.com/introducing-multi-agent-frameworks-the-power-of-collaboration-e9db31bba1b6</mark>
