from crewai import Agent, Task, Crew, Process, LLM

# 安装依赖
# pip install crewai langchain-ollama

# 使用本地 ollama 模型，并使用较高的 temperature 以促进创造性输出。
llm = LLM(model="ollama/qwen3:4b-instruct", temperature=0.7)

# 第一个智能体生成初始草稿。
draft_writer = Agent(
    role="Draft Writer",
    goal="Generate initial draft content on a given subject.",
    backstory="""You are an experienced content writer who can produce clear, 
    informative paragraphs on various topics. You focus on creating well-structured 
    and engaging content.""",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# 第二个智能体评审第一个智能体的草稿。
fact_checker = Agent(
    role="Fact Checker",
    goal="Review text for factual accuracy and provide a structured critique.",
    backstory="""You are a meticulous fact-checker with expertise in verifying claims 
    and identifying inaccuracies. You provide detailed, constructive feedback on content 
    accuracy and cite specific issues when found.""",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


def run_review_pipeline(subject: str):
    """
    Execute the write and review pipeline for a given subject.
    
    Args:
        subject: The topic to write about and review.
    
    Returns:
        The review result containing status and reasoning.
    """
    # 任务 1：生成初始草稿
    draft_task = Task(
        description=f"Write a short, informative paragraph about: {subject}",
        expected_output="A clear, well-structured paragraph about the given subject.",
        agent=draft_writer,
    )
    
    # 任务 2：审查草稿的事实准确性
    review_task = Task(
        description="""Review the draft text from the previous task for factual accuracy.
        Your output must be structured as follows:
        - Status: Either "ACCURATE" or "INACCURATE"
        - Reasoning: A clear explanation for your status, citing specific issues if any are found.
        
        Carefully verify all factual claims and provide detailed feedback.""",
        expected_output="""A structured review containing:
        1. Status (ACCURATE or INACCURATE)
        2. Detailed reasoning explaining the assessment""",
        agent=fact_checker,
        context=[draft_task],  # This task depends on draft_task output
    )
    
    # 创建并执行团队
    crew = Crew(
        agents=[draft_writer, fact_checker],
        tasks=[draft_task, review_task],
        process=Process.sequential,  # Sequential execution ensures draft is written before review
        verbose=True,
    )
    
    # 执行流程
    result = crew.kickoff()
    return result



# 示例用法：
if __name__ == "__main__":
    subject = "The impact of artificial intelligence on modern healthcare"
    print(f"\n--- Processing subject: '{subject}' ---\n")
    result = run_review_pipeline(subject)
    print("\n--- Final Review Result ---")
    print(result)