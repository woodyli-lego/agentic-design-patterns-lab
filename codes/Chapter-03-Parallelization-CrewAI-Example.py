from crewai import Agent, Task, Crew, Process, LLM

# 当前文件展示如何使用 CrewAI 实现并行任务执行
# 通过设置 async_execution=True，前三个任务会并行执行
# 最后的综合任务会等待前三个任务完成后再执行

# 安装依赖
# pip install crewai crewai-tools langchain-ollama

# 使用本地 ollama 模型
llm = LLM(model="ollama/qwen3:4b-instruct", temperature=0.7)

# --- 1. 定义三个并行执行的 Agent（任务彼此独立） ---

# Agent 1: Summarizer - 摘要生成器
summarizer_agent = Agent(
    role="Topic Summarizer",
    goal="Provide a concise summary of the given topic",
    backstory="""You are an expert at distilling complex information into clear, 
    concise summaries. You excel at identifying the most important aspects of any topic.""",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# Agent 2: Question Generator - 问题生成器
question_agent = Agent(
    role="Question Generator",
    goal="Generate three thought-provoking questions about the topic",
    backstory="""You are a curious researcher who excels at asking insightful questions. 
    Your questions help others think deeply about topics and explore new angles.""",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# Agent 3: Term Identifier - 关键术语识别器
term_agent = Agent(
    role="Key Term Identifier",
    goal="Identify 5-10 key terms related to the topic",
    backstory="""You are a subject matter expert who can quickly identify the most 
    important terms and concepts in any field. Your expertise helps others build their vocabulary.""",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# Agent 4: Synthesizer - 综合分析器（在并行任务完成后执行）
synthesizer_agent = Agent(
    role="Information Synthesizer",
    goal="Combine all the information into a comprehensive answer",
    backstory="""You are a master at synthesizing information from multiple sources. 
    You can weave together summaries, questions, and key terms into coherent, comprehensive responses.""",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


# --- 2. 为每个 Agent 定义任务 ---

def create_tasks(topic: str):
    """
    Create tasks for the given topic.
    
    Args:
        topic: The input topic to be processed by the agents.
    
    Returns:
        A tuple of (parallel_tasks, synthesis_task)
    """
    # 并行任务
    summarize_task = Task(
        description=f"Summarize the following topic concisely: {topic}",
        expected_output="A concise summary of the topic (2-3 sentences)",
        agent=summarizer_agent,
        async_execution=True,  # 异步执行
    )
    
    questions_task = Task(
        description=f"Generate three interesting questions about the following topic: {topic}",
        expected_output="Three thought-provoking questions about the topic",
        agent=question_agent,
        async_execution=True,  # 异步执行
    )
    
    terms_task = Task(
        description=f"Identify 5-10 key terms from the following topic: {topic}",
        expected_output="A list of 5-10 key terms, separated by commas",
        agent=term_agent,
        async_execution=True,  # 异步执行
    )
    
    # 综合任务（依赖于上述三个任务的结果）
    synthesis_task = Task(
        description=f"""Based on the following information about '{topic}':
        
        - Summary from the Summarizer
        - Questions from the Question Generator  
        - Key terms from the Term Identifier
        
        Synthesize a comprehensive answer that integrates all these elements.""",
        expected_output="""A comprehensive response that includes:
        1. An integrated summary incorporating the key points
        2. How the questions relate to understanding the topic
        3. How the key terms connect to form a complete picture
        4. An overall synthesis tying everything together""",
        agent=synthesizer_agent,
        context=[summarize_task, questions_task, terms_task],  # 依赖于前三个任务的输出
    )
    
    return [summarize_task, questions_task, terms_task, synthesis_task]


# --- 3. 运行示例 ---

def run_parallel_example(topic: str) -> None:
    """
    Runs the parallel processing crew with a specific topic
    and prints the synthesized result.

    Args:
        topic: The input topic to be processed by the crew.
    """
    print(f"\n--- Running Parallel CrewAI Example for Topic: '{topic}' ---\n")
    
    try:
        # 创建任务
        tasks = create_tasks(topic)
        
        # 创建 Crew - 使用 hierarchical 流程让任务并行执行
        # CrewAI 会自动处理任务依赖关系，前三个任务会并行执行，最后一个任务等待它们完成
        crew = Crew(
            agents=[summarizer_agent, question_agent, term_agent, synthesizer_agent],
            tasks=tasks,
            process=Process.sequential,  # sequential 模式下，有 context 依赖的任务会等待
            verbose=True,
        )
        
        # 执行
        result = crew.kickoff()
        
        print("\n" + "="*80)
        print("--- Final Synthesized Response ---")
        print("="*80)
        print(result)
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\nAn error occurred during crew execution: {e}")
        raise


if __name__ == "__main__":
    test_topic = "The history of space exploration"
    run_parallel_example(test_topic)