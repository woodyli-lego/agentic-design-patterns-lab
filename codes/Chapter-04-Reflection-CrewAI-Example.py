from crewai import Agent, Task, Crew, Process, LLM

# ============================================================================
# CrewAI Reflection Pattern - 使用 Task 链实现（推荐方式）
# ============================================================================
#
# 本示例展示了在 CrewAI 中实现 Reflection 模式的最佳实践：
# - 使用单一 Crew 完成所有工作（符合 CrewAI 设计理念）
# - 通过 Task 的 context 参数构建依赖链
# - 预定义固定次数的 reflection 循环（3 次）
#
# 架构：
#   Task 1: 初始草稿
#      ↓ (context)
#   Task 2: 第 1 轮评审
#      ↓ (context)
#   Task 3: 第 1 轮改进
#      ↓ (context)
#   Task 4: 第 2 轮评审
#      ↓ (context)
#   Task 5: 第 2 轮改进
#      ↓ (context)
#   Task 6: 第 3 轮评审
#      ↓ (context)
#   Task 7: 第 3 轮改进（最终版本）
#
# ============================================================================

# 安装依赖
# pip install crewai langchain-ollama

# 使用本地 ollama 模型，并使用较高的 temperature 以促进创造性输出。
llm = LLM(model="ollama/qwen3:4b-instruct", temperature=0.7)

# 定义写作智能体
draft_writer = Agent(
    role="Content Writer",
    goal="Write clear, informative content and iteratively improve it based on feedback.",
    backstory="""You are an experienced content writer who excels at creating 
    well-structured, engaging paragraphs. You are excellent at incorporating 
    constructive feedback to refine and improve your work.""",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# 定义评审智能体
fact_checker = Agent(
    role="Content Critic",
    goal="Provide detailed, constructive feedback on content quality and accuracy.",
    backstory="""You are a meticulous editor and fact-checker with expertise in 
    identifying areas for improvement. You provide specific, actionable feedback 
    on factual accuracy, clarity, coherence, and completeness.""",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


def create_reflection_tasks(subject: str, num_iterations: int = 3):
    """
    创建 Reflection 模式的 Task 链。
    
    这个函数构建一个完整的 Task 链，实现多轮的"写作-评审-改进"循环。
    每个 Task 通过 context 参数依赖于前一个 Task 的输出。
    
    Args:
        subject: 要写作的主题
        num_iterations: 反思循环的次数（默认 3 次）
    
    Returns:
        tasks: Task 列表，按顺序执行
    """
    tasks = []
    
    # Task 1: 初始草稿
    initial_task = Task(
        description=f"""Write a clear, informative paragraph about the following topic:
        
        Topic: {subject}
        
        Focus on:
        - Accuracy of information
        - Clear and engaging writing style
        - Well-structured content
        - Completeness of key points""",
        expected_output="A well-written paragraph about the given topic (initial draft).",
        agent=draft_writer,
    )
    tasks.append(initial_task)
    
    # 构建 N 轮的 critique -> refine 循环
    previous_task = initial_task
    
    for i in range(num_iterations):
        iteration_num = i + 1
        
        # Critique Task
        critique_task = Task(
            description=f"""Review the content from the previous task (Round {iteration_num} review).
            
            Evaluate the content based on:
            - Factual accuracy and correctness
            - Clarity and coherence
            - Completeness of information
            - Writing quality and engagement
            
            Provide specific, actionable feedback for improvement. 
            Be constructive and point out exactly what needs to be changed.""",
            expected_output=f"Detailed critique with specific improvement suggestions (Round {iteration_num}).",
            agent=fact_checker,
            context=[previous_task],  # 依赖上一个任务的输出
        )
        tasks.append(critique_task)
        
        # Refine Task
        refine_task = Task(
            description=f"""Based on the critique from the previous task, improve the content (Round {iteration_num} refinement).
            
            Address ALL the issues mentioned in the feedback:
            - Fix any factual inaccuracies
            - Improve clarity where needed
            - Add missing information
            - Enhance overall quality
            
            Produce a refined version that incorporates all the suggested improvements.""",
            expected_output=f"Improved and refined content addressing all critique points (Version {iteration_num + 1}).",
            agent=draft_writer,
            context=[critique_task],  # 依赖 critique 的输出
        )
        tasks.append(refine_task)
        previous_task = refine_task
    
    return tasks


def run_reflection_pipeline(subject: str, num_iterations: int = 3):
    """
    执行完整的 Reflection 流程（CrewAI 推荐方式）。
    
    使用单一 Crew + Task 链实现 reflection 模式。
    所有 Task 在一个 Crew 中顺序执行，通过 context 自动传递结果。
    
    Args:
        subject: 要写作的主题
        num_iterations: 反思循环的次数（默认 3 次）
    
    Returns:
        最终优化后的内容
    """
    print(f"\n{'='*70}")
    print(f"CrewAI Reflection Pattern - Task Chain Approach")
    print(f"{'='*70}\n")
    print(f"Topic: {subject}")
    print(f"Reflection iterations: {num_iterations}")
    print(f"Total tasks: {1 + num_iterations * 2} (1 initial + {num_iterations} × 2)")
    print()
    
    # 创建 Task 链
    tasks = create_reflection_tasks(subject, num_iterations)
    
    # 创建单一 Crew 执行所有任务
    crew = Crew(
        agents=[draft_writer, fact_checker],
        tasks=tasks,
        process=Process.sequential,  # 顺序执行所有任务
        verbose=True,
    )
    
    print(f"\n{'='*70}")
    print(f"Starting Crew execution with {len(tasks)} tasks...")
    print(f"{'='*70}\n")
    
    # 执行整个流程
    result = crew.kickoff()
    
    print(f"\n{'='*70}")
    print(f"FINAL RESULT (after {num_iterations} reflection rounds)")
    print(f"{'='*70}\n")
    print(result)
    print()
    
    return result


# 示例用法
if __name__ == "__main__":
    subject = "The impact of artificial intelligence on modern healthcare"
    
    # 运行 Reflection 流程（3 轮迭代）
    final_content = run_reflection_pipeline(subject, num_iterations=3)
    
    print(f"\n{'='*70}")
    print("Execution complete!")
    print(f"{'='*70}")
    print("""
    Summary:
    - ✅ Used single Crew (CrewAI best practice)
    - ✅ Tasks linked via context parameter
    - ✅ 3 rounds of reflection completed
    - ✅ Automatic result propagation between tasks
    
    Note: This approach executes all iterations regardless of quality.
    For dynamic stopping based on quality assessment, see the alternative
    implementation in Chapter-04-Reflection-CrewAI-Example-Alternative.py
    """)