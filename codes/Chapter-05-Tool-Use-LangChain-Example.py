import asyncio
import nest_asyncio

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool as langchain_tool
from langchain.agents import create_agent


# 使用本地 ollama
try:
   llm: ChatOllama = ChatOllama(model="qwen3:4b-instruct", temperature=0)
   print(f"Language model initialized: {llm.model}")
except Exception as e:
   print(f"Error initializing language model: {e}")
   raise RuntimeError("Failed to initialize language model. Please ensure Ollama is running and the model is available.") from e


# --- 定义模拟的搜索工具 ---
@langchain_tool
def search_information(query: str) -> str:
   """
   Provides factual information on a given topic. Use this tool to find answers to phrases
   like 'capital of France' or 'weather in London?'.
   """
   print(f"\n--- 🛠️ Tool Called: search_information with query: '{query}' ---")

   # 通过一个字典预定义的结果来模拟搜索工具。
   simulated_results = {
      "weather in london": "The weather in London is currently cloudy with a temperature of 15°C.",
      "capital of france": "The capital of France is Paris.",
      "population of earth": "The estimated population of Earth is around 8 billion people.",
      "tallest mountain": "Mount Everest is the tallest mountain above sea level.",
      "default": f"Simulated search result for '{query}': No specific information found, but the topic seems interesting."
   }
   result = simulated_results.get(query.lower(), simulated_results["default"])
   print(f"--- TOOL RESULT: {result} ---")
   return result

tools = [search_information]

# --- 创建一个使用工具的智能体 ---
# 这个提示模板需要一个 `agent_scratchpad` 占位符，用于记录智能体的内部步骤。
agent_prompt = ChatPromptTemplate.from_messages([
   ("system", "You are a helpful assistant."),
   ("human", "{input}"),
   ("placeholder", "{agent_scratchpad}"),
])

# 使用定义好的大语言模型、工具和提示词模板构建智能体。
agent = create_agent(model=llm, tools=tools, system_prompt="You are a helpful assistant")

async def run_agent_with_tool(query: str):
   """
   Invokes the agent executor with a query and prints the final response.
   """
   print(f"\n--- 🏃 Running Agent with Query: '{query}' ---")
   try:
      response = await agent.ainvoke({"messages": [{"role": "user", "content": query}]})

      print("\n--- ✅ Final Agent Response ---")
      print(response["messages"][ -1 ].content)
   except Exception as e:
      print(f"\n🛑 An error occurred during agent execution: {e}")

async def main():
   """
   Runs all agent queries concurrently.
   """
   tasks = [
      run_agent_with_tool("What is the capital of France?"),
      run_agent_with_tool("What's the weather like in London?"),
      # 不知道是怎么做到的，但是 tool 的文档应该明确说明支持 `population of earth` 关键字。
      run_agent_with_tool("Tell me the population of Earth."),
      run_agent_with_tool("Tell me something about dogs.") # Should trigger the default tool response
   ]
   await asyncio.gather(*tasks)

nest_asyncio.apply()
asyncio.run(main())
