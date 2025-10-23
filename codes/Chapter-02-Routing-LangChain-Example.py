# Copyright (c) 2025 Marco Fago
#
# This code is licensed under the MIT License.
# See the LICENSE file in the repository for the full license text.

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableBranch


# --- Configuration ---
# 使用本地 ollama
llm = ChatOllama(model="qwen3:4b-instruct", temperature=0)

# --- 定义模拟的子智能体处理器 (等同于 ADK 中的 sub_agents) ---
# 子智能体同样会把自然语言（request）作为输入，这里是简单模拟，实际上也需要调用 LLM。
def booking_handler(request: str) -> str:
    """Simulates the Booking Agent handling a request."""
    print("\n--- DELEGATING TO BOOKING HANDLER ---")
    return f"Booking Handler processed request: '{request}'. Result: Simulated booking action."

def info_handler(request: str) -> str:
    """Simulates the Info Agent handling a request."""
    print("\n--- DELEGATING TO INFO HANDLER ---")
    return f"Info Handler processed request: '{request}'. Result: Simulated information retrieval."

def unclear_handler(request: str) -> str:
    """Handles requests that couldn't be delegated."""
    print("\n--- HANDLING UNCLEAR REQUEST ---")
    return f"Coordinator could not delegate request: '{request}'. Please clarify."

# --- 定义协调员的路由链 (等同于 ADK 协调员的指令) ---
# 这个链负责决定将任务委派给哪个处理器。

# 定义一个简单的 prompt template：系统需要识别 request 的意图，并返回 "booker"，"info" 或者 "unclear"。
coordinator_router_prompt = ChatPromptTemplate.from_messages([
    ("system", """Analyze the user's request and determine which specialist handler should process it.
     - If the request is related to booking flights or hotels, output 'booker'.
     - For all other general information questions, output 'info'.
     - If the request is unclear or doesn't fit either category, output 'unclear'.
     ONLY output one word: 'booker', 'info', or 'unclear'."""),
    ("user", "{request}")
])

coordinator_router_chain = coordinator_router_prompt | llm | StrOutputParser()

# --- 定义委派逻辑 (等同于 ADK 基于 sub_agents 的自动流) ---
# 使用 RunnableBranch 根据路由链的输出进行路由。

# 为 RunnableBranch 定义分支
# 这里其实就是个简单的字典，基于 coordinator_router_prompt 返回的关键字，返回相应的 RunnablePassthrough
# value 部分使用 RunnablePassthrough 属于保留原始输入，并添加 request 字段。
branches = {
    "booker": RunnablePassthrough.assign(output=lambda x: booking_handler(x['request']['request'])),
    "info": RunnablePassthrough.assign(output=lambda x: info_handler(x['request']['request'])),
    "unclear": RunnablePassthrough.assign(output=lambda x: unclear_handler(x['request']['request'])),
}

# 创建 RunnableBranch。它会接收路由链的输出，
# 并将原始输入 ('request') 路由到相应的处理器。

# RunnableBranch 的语法结构如下：
# RunnableBranch(
#   (条件1, 分支1),  # 如果条件1为True，执行分支1
#   (条件2, 分支2),  # 否则如果条件2为True，执行分支2
#   默认分支         # 否则执行默认分支
# )
delegation_branch = RunnableBranch(
    (lambda x: x['decision'].strip() == 'booker', branches["booker"]), # Added .strip()
    (lambda x: x['decision'].strip() == 'info', branches["info"]),     # Added .strip()
    branches["unclear"] # Default branch for 'unclear' or any other output
)

# 将路由链和委派分支组合成一个可执行单元
# 路由链的输出 ('decision') 会连同原始输入 ('request') 一起
# 传递给 delegation_branch。
coordinator_agent = {
    "decision": coordinator_router_chain,
    "request": RunnablePassthrough()
} | delegation_branch | (lambda x: x['output']) # Extract the final output

# --- 调用分析 ---
# 假设用户输入是： "Book me a flight to London."
# 1. 组装出 origin_request = { "request": "Book me a flight to London." }
# 1. 调用入口：coordinator_agent.invoke(origin_request)。
# 2. 调用 coordinator_router_chain.invoke(origin_request)，分析目的，得到 "booker"。
# 3. 组装出 delegation_input = {"decision": "booker", "request": { "request": "Book me a flight to London." }}。
# 4. 调用 delegation_branch.invoke(delegation_input)。
# 5. delegation_branch 根据 decision == "booker"，执行 booking_handler(delegation_input['request']['request'])。
# 6. booking_handler 返回后，组装出 passthrough_result = {"decision": "booker", "request": { "request": "Book me a flight to London." }, "output": "booking_handler的返回值"}。
# 7. 从 passthrough_result 中提取 output 并返回，作为 coordinator_agent 的输出。

# --- Example Usage ---
# --- 使用示例 ---
def main():
    print("--- Running with a booking request ---")
    request_a = "Book me a flight to London."
    result_a = coordinator_agent.invoke({"request": request_a})
    print(f"Final Result A: {result_a}")

    print("\n--- Running with an info request ---")
    request_b = "What is the capital of Italy?"
    result_b = coordinator_agent.invoke({"request": request_b})
    print(f"Final Result B: {result_b}")

    print("\n--- Running with an unclear request ---")
    request_c = "Tell me about quantum physics."
    result_c = coordinator_agent.invoke({"request": request_c})
    print(f"Final Result C: {result_c}")

if __name__ == "__main__":
    main()