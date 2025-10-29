# Copyright (c) 2025 Marco Fago
#
# This code is licensed under the MIT License.
# See the LICENSE file in the repository for the full license text.

from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool

# 安装依赖
# pip install crewai langchain-openai

# Local Ollama LLM configuration
local_llm = LLM(model="ollama/qwen3:4b-instruct")


# --- 定义工具函数 ---
# 这些函数模拟了专业智能体的具体行动 (例如调接口)。
def booking_handler(request: str) -> str:
    """
    Handles booking requests for flights and hotels.
    Args:
        request: The user's request for a booking.
    Returns:
        A confirmation message that the booking was handled.
    """
    print("-------------------------- Booking Handler Called ----------------------------")
    return f"Booking action for '{request}' has been simulated."

def info_handler(request: str) -> str:
    """
    Handles general information requests.
    Args:
        request: The user's question.
    Returns:
        A message indicating the information request was handled.
    """
    print("-------------------------- Info Handler Called ----------------------------")
    return f"Information request for '{request}'. Result: Simulated information retrieval."


# --- 从函数创建 agent 可调用的工具 ---
@tool("Booking Tool")
def booking_tool(request: str) -> str:
    """CrewAI tool that simulates flight/hotel booking for the given natural language request."""
    return booking_handler(request)

@tool("Info Tool")
def info_tool(request: str) -> str:
    """CrewAI informational tool that returns a simulated info retrieval result for the given request."""
    return info_handler(request)

# --- 定义配备了各自工具的专业子智能体 (CrewAI) ---
booking_agent = Agent(
    role="Travel Booking Specialist",
    goal="Handle all flight and hotel booking requests using the Booking Tool.",
    backstory="You specialize in booking flights and hotels efficiently.",
    tools=[booking_tool],
    llm=local_llm,
    verbose=True,
    allow_delegation=False,
)

info_agent = Agent(
    role="Information Specialist",
    goal="Answer general user questions using the Info Tool.",
    backstory="You provide general knowledge and informational responses.",
    tools=[info_tool],
    llm=local_llm,
    verbose=True,
    allow_delegation=False,
)

# 在 CrewAI 中没有内建子智能体自动路由，这里通过任务描述来模拟。
coordinator_agent = Agent(
    role="Routing Coordinator",
    goal="Analyze requests and decide whether it's a booking or info query, then produce the correct response by leveraging tasks.",
    backstory="You are a dispatcher that routes user intents to either booking or information specialist.",
    llm=local_llm,
    verbose=True,
    allow_delegation=True,
)

# --- 执行逻辑 ---

def run_dynamic_request(request: str):
    """
    使用 CrewAI 的协作机制处理动态请求。
    协调者智能体会自动分析请求并委托给合适的专业智能体。
    """
    print(f"\n--- Processing request: '{request}' ---")
    
    # 创建任务,让协调者智能分析并委托
    task = Task(
        description=(
            f"User request: '{request}'\n"
            "Analyze this request carefully. If it's about booking flights/hotels/travel, "
            "delegate to the Travel Booking Specialist. If it's a general information question, "
            "delegate to the Information Specialist. Ensure the appropriate tool is used."
        ),
        expected_output="Complete response to the user's request with confirmation of action taken.",
        agent=coordinator_agent,  # 协调者会自动委托给合适的智能体
    )
    
    # 创建包含所有智能体的 Crew,利用协作机制
    crew = Crew(
        agents=[coordinator_agent, booking_agent, info_agent],
        tasks=[task],
        verbose=True,
    )
    
    result = crew.kickoff()
    print(f"\n=== Final Response ===\n{result}\n")
    return result

def main():
    """运行 CrewAI 路由示例的主函数。"""

    # 使用示例 - 动态请求,由 CrewAI 自动协作路由
    run_dynamic_request("Book me a hotel in Paris.")
    # run_dynamic_request("What is the highest mountain in the world?")
    # run_dynamic_request("Tell me a random fact.")
    # run_dynamic_request("Find flights to Tokyo next month.")


if __name__ == "__main__":
    main()