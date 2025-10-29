import os
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage


# 安装依赖
# pip install langchain langchain-community langchain-openai


# --- Configuration ---
# 使用 ollama qwen3 模型，并设置较低的温度值以获得更稳定的输出
llm = ChatOllama(model="qwen3:4b-instruct", temperature=0.1)


def run_reflection_loop():
    """
    Demonstrates a multi-step AI reflection loop to progressively improve a Python function.
    """

    # --- 核心任务的提示词: 编写一个 python 函数 ---
    task_prompt = """
    Your task is to create a Python function named `calculate_factorial`.
    This function should do the following:
    1.  Accept a single integer `n` as input.
    2.  Calculate its factorial (n!).
    3.  Include a clear docstring explaining what the function does.
    4.  Handle edge cases: The factorial of 0 is 1.
    5.  Handle invalid input: Raise a ValueError if the input is a negative number.
    """

    # --- 反思循环：最大循环数为 3 ---
    max_iterations = 3
    current_code = ""

    # 构建对话历史，为每一步提供必要的上下文信息。
    message_history = [HumanMessage(content=task_prompt)]

    for i in range(max_iterations):
        print("\n" + "="*25 + f" REFLECTION LOOP: ITERATION {i + 1} " + "="*25)

        # --- 1. GENERATE / REFINE STAGE ---
        # 在第一次迭代时，生成初始代码；在后续迭代时，基于上一步的反馈优化代码。
        if i == 0:
            print("\n>>> STAGE 1: GENERATING initial code...")
            # 第一次迭代时，只需要任务提示词。
            response = llm.invoke(message_history)
            current_code = response.content
        else:
            print("\n>>> STAGE 1: REFINING code based on previous critique...")
            # 后续迭代时，除了任务提示词，还包含上一步的代码和反馈。
            # 然后要求模型根据反馈意见优化代码。
            message_history.append(HumanMessage(content="Please refine the code using the critiques provided."))
            response = llm.invoke(message_history)
            current_code = response.content

        # 把生成的代码加入对话历史，供后续迭代使用。
        # 这里会把每一次的成代码放入 history，对于 context engineering 的考虑，可以选择只保留最新一次代码，
        # 和最新一次 的 critique，来节省上下文长度，帮助 LLM 保持专注。
        # 但是这样的实践只针对本例，对于不同的任务，history 的管理策略并不一样。
        print("\n--- Generated Code (v" + str(i + 1) + ") ---\n" + current_code)
        message_history.append(response)

        # --- 2. REFLECT STAGE ---
        print("\n>>> STAGE 2: REFLECTING on the generated code...")

        # 创建一个特定的提示词，要求模型扮演高级软件工程师的角色，对代码进行仔细的审查。
        reflector_prompt = [
            SystemMessage(content="""
                You are a senior software engineer and an expert in Python.
                Your role is to perform a meticulous code review.
                Critically evaluate the provided Python code based on the original task requirements.
                Look for bugs, style issues, missing edge cases, and areas for improvement.
                If the code is perfect and meets all requirements, respond with the single phrase 'CODE_IS_PERFECT'.
                Otherwise, provide a bulleted list of your critiques.
            """),
            # 注意，对审查者而言，每次关注的是原始任务和当前代码，并不关注完整的对话历史。
            HumanMessage(content=f"Original Task:\n{task_prompt}\n\nCode to Review:\n{current_code}")
        ]

        critique_response = llm.invoke(reflector_prompt)
        critique = critique_response.content

        # --- 3. STOPPING CONDITION ---
        # 如果代码完美符合要求，则结束反思循环。
        if "CODE_IS_PERFECT" in critique:
            print("\n--- Critique ---\nNo further critiques found. The code is satisfactory.")
            break

        # 否则，把反馈加入对话历史，供下一轮优化使用。
        print("\n--- Critique ---\n" + critique)
        message_history.append(HumanMessage(content=f"Critique of the previous code:\n{critique}"))

    print("\n" + "="*30 + " FINAL RESULT " + "="*30)
    print("\nFinal refined code after the reflection process:\n")
    print(current_code)


if __name__ == "__main__":
    run_reflection_loop()
