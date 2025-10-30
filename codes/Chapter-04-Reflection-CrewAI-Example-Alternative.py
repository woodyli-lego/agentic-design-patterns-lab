from crewai import Agent, Task, Crew, Process, LLM

# ============================================================================
# CrewAI Reflection 最佳实践对比
# ============================================================================
# 
# 本文件展示两种在 CrewAI 中实现 Reflection 模式的方案：
#
# 方案 A（推荐）：固定迭代次数 + 单一 Crew + Task 链
#   - 优点：符合 CrewAI 设计理念，一个 Crew 完成所有工作
#   - 缺点：无法根据质量动态停止，可能做无用功
#   - 适用：质量要求高，愿意用固定次数换取稳定性
#
# 方案 B（灵活）：动态循环 + 多次 Crew 创建
#   - 优点：可以根据 critique 结果提前停止，节省成本
#   - 缺点：每次循环创建新 Crew，不够优雅
#   - 适用：成本敏感，需要智能停止条件
#
# ============================================================================

# 安装依赖
# pip install crewai langchain-ollama

llm = LLM(model="ollama/qwen3:4b-instruct", temperature=0.7)


# ============================================================================
# 方案 A：固定迭代次数的 Task 链（推荐用于 CrewAI）
# ============================================================================

def run_reflection_with_task_chain(subject: str, num_iterations: int = 2):
    """
    方案 A：使用 CrewAI 的 Task 链实现固定次数的 reflection。
    
    优点：
    - 符合 CrewAI 理念：一个 Crew 内完成所有工作
    - Task 之间通过 context 自动传递结果
    - 代码结构清晰，易于理解和维护
    
    缺点：
    - 无法动态停止（必须执行完所有迭代）
    - 即使内容已经完美，仍会继续改进
    
    Args:
        subject: 要写作的主题
        num_iterations: 固定的改进次数（默认 2 次）
    """
    print(f"\n{'='*70}")
    print(f"方案 A：固定迭代的 Task 链（CrewAI 推荐方式）")
    print(f"{'='*70}\n")
    print(f"主题: {subject}")
    print(f"固定迭代次数: {num_iterations}\n")
    
    # 定义 Agent
    writer = Agent(
        role="Content Writer",
        goal="Write and iteratively improve content based on feedback.",
        backstory="""You are an experienced writer who excels at creating clear, 
        engaging content and incorporating feedback to improve your work.""",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    
    critic = Agent(
        role="Content Critic",
        goal="Provide constructive feedback on written content.",
        backstory="""You are a meticulous editor with expertise in identifying 
        areas for improvement. You provide specific, actionable feedback.""",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    
    # 动态构建 Task 链
    tasks = []
    
    # 第一个任务：初始写作
    initial_task = Task(
        description=f"Write a clear, informative paragraph about: {subject}",
        expected_output="A well-structured paragraph about the given subject.",
        agent=writer,
    )
    tasks.append(initial_task)
    
    # 构建 N 轮的 critique -> refine 循环
    previous_task = initial_task
    
    for i in range(num_iterations):
        # Critique 任务
        critique_task = Task(
            description=f"""Review the content from the previous task.
            
            Provide specific, constructive feedback on:
            - Factual accuracy
            - Clarity and coherence
            - Completeness
            - Areas for improvement
            
            Be detailed and actionable in your critique.""",
            expected_output=f"Detailed critique with specific improvement suggestions (Round {i+1})",
            agent=critic,
            context=[previous_task],  # 依赖上一个任务的输出
        )
        tasks.append(critique_task)
        
        # Refine 任务
        refine_task = Task(
            description=f"""Based on the critique, improve the content.
            
            Address all the issues mentioned in the feedback and produce 
            a refined version that is more accurate, clear, and complete.""",
            expected_output=f"Improved content addressing the critique (Version {i+2})",
            agent=writer,
            context=[critique_task],  # 依赖 critique 的输出
        )
        tasks.append(refine_task)
        previous_task = refine_task
    
    # 创建单一 Crew 执行所有任务
    crew = Crew(
        agents=[writer, critic],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )
    
    # 执行
    result = crew.kickoff()
    
    print(f"\n{'='*70}")
    print(f"最终结果（经过 {num_iterations} 轮改进）")
    print(f"{'='*70}\n")
    print(result)
    
    return result


# ============================================================================
# 方案 B：动态循环 + 智能停止（灵活但不够 CrewAI 风格）
# ============================================================================

def run_reflection_with_dynamic_loop(subject: str, max_iterations: int = 3):
    """
    方案 B：使用 Python 循环 + 动态停止条件实现 reflection。
    
    优点：
    - 可以根据质量提前停止，节省成本
    - 灵活控制停止条件
    - 不会做无用功
    
    缺点：
    - 每次循环创建新 Crew，不够优雅
    - 不符合 CrewAI 的设计理念
    - 状态管理需要手动处理
    
    Args:
        subject: 要写作的主题
        max_iterations: 最大迭代次数
    """
    print(f"\n{'='*70}")
    print(f"方案 B：动态循环 + 智能停止（灵活方案）")
    print(f"{'='*70}\n")
    print(f"主题: {subject}")
    print(f"最大迭代次数: {max_iterations}\n")
    
    writer = Agent(
        role="Content Writer",
        goal="Write and improve content based on feedback.",
        backstory="""You are an experienced writer who excels at incorporating 
        feedback to improve your work.""",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    
    critic = Agent(
        role="Content Critic",
        goal="Evaluate content and decide if it needs improvement.",
        backstory="""You are a meticulous critic. When content is perfect, 
        you respond with 'CONTENT_IS_PERFECT'. Otherwise, you provide detailed feedback.""",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
    
    current_content = None
    
    for iteration in range(max_iterations):
        print(f"\n{'='*25} 迭代 {iteration + 1} {'='*25}\n")
        
        # 阶段 1：写作或改进
        if iteration == 0:
            write_task = Task(
                description=f"Write a clear paragraph about: {subject}",
                expected_output="A well-structured paragraph.",
                agent=writer,
            )
        else:
            write_task = Task(
                description=f"""Improve this content based on the critique:
                
                Current Content:
                {current_content}
                
                Critique:
                {critique}
                
                Produce an improved version.""",
                expected_output="Improved content addressing the critique.",
                agent=writer,
            )
        
        write_crew = Crew(
            agents=[writer],
            tasks=[write_task],
            process=Process.sequential,
            verbose=False,
        )
        
        current_content = str(write_crew.kickoff())
        print(f"\n--- 内容 (v{iteration + 1}) ---\n{current_content}\n")
        
        # 阶段 2：评审
        critique_task = Task(
            description=f"""Review this content:
            
            {current_content}
            
            If it's perfect, respond ONLY with: "CONTENT_IS_PERFECT"
            Otherwise, provide detailed improvement suggestions.""",
            expected_output="Either 'CONTENT_IS_PERFECT' or detailed critique.",
            agent=critic,
        )
        
        critique_crew = Crew(
            agents=[critic],
            tasks=[critique_task],
            process=Process.sequential,
            verbose=False,
        )
        
        critique = str(critique_crew.kickoff())
        print(f"--- 评审 ---\n{critique}\n")
        
        # 阶段 3：检查停止条件
        if "CONTENT_IS_PERFECT" in critique.upper():
            print(f"✅ 内容完美！在第 {iteration + 1} 轮停止。\n")
            break
        
        if iteration == max_iterations - 1:
            print(f"⚠️  达到最大迭代次数 ({max_iterations})。\n")
    
    return current_content


# ============================================================================
# 方案对比示例
# ============================================================================

if __name__ == "__main__":
    subject = "The impact of artificial intelligence on modern healthcare"
    
    print("\n" + "="*70)
    print("CrewAI Reflection 模式：两种方案对比")
    print("="*70)
    
    # 方案 A：Task 链（CrewAI 推荐）
    print("\n执行方案 A...")
    result_a = run_reflection_with_task_chain(subject, num_iterations=2)
    
    print("\n\n" + "="*70 + "\n")
    
    # 方案 B：动态循环（灵活但不够优雅）
    print("执行方案 B...")
    result_b = run_reflection_with_dynamic_loop(subject, max_iterations=3)
    
    # 总结
    print("\n" + "="*70)
    print("方案对比总结")
    print("="*70)
    print("""
    方案 A（Task 链）：
    ✅ 符合 CrewAI 设计理念
    ✅ 代码结构清晰优雅
    ✅ 自动传递 context
    ❌ 无法动态停止
    ❌ 可能做无用功
    
    📌 推荐场景：质量优先，固定预算，追求代码优雅
    
    ---
    
    方案 B（动态循环）：
    ✅ 可以智能停止
    ✅ 节省成本
    ✅ 灵活控制
    ❌ 多次创建 Crew
    ❌ 不够 CrewAI 风格
    
    📌 推荐场景：成本敏感，需要动态控制，灵活性优先
    """)
