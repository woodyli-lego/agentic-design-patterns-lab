import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 初始化语言模型（使用本地 Ollama 模型）
llm = ChatOllama(model="qwen3:4b-instruct", temperature=0)

# --- Prompt 1: 提取信息 ---
prompt_extract = ChatPromptTemplate.from_template(
    "Extract the technical specifications from the following text:\n\n{text_input}"
)

# --- Prompt 2: 转换为 JSON ---
prompt_transform = ChatPromptTemplate.from_template(
    "Transform the following specifications into a JSON object with 'cpu', 'memory', and 'storage' as keys:\n\n{specifications}"
)

# --- 使用 LCEL 构建链 ---
# StrOutputParser() 会将 LLM 的消息输出转换为一个简单的字符串。暂时理解为就是把 response 的内容字段拿出来。
extraction_chain = prompt_extract | llm | StrOutputParser()

# 通用函数：用于在链执行过程中打印中间结果
def print_intermediate(data, title="中间结果"):
    """
    打印中间结果并原样返回数据。
    
    Args:
        data: 要打印的数据（通常是字典）
        title: 打印时显示的标题
    
    Returns:
        原样返回输入的 data
    """
    print(f"\n--- {title} ---")
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{key}:")
            print("-------")
            # 如果 value 很长，可以考虑截断或格式化输出
            value_str = str(value)
            if len(value_str) > 200:
                print(f"{value_str[:200]}...")
            else:
                print(f"{value}")
    else:
        print(data)
    return data

# 完整的链将提取链的输出传递给转换提示中的 'specifications' 变量。
# 使用 RunnablePassthrough 确保中间结果被捕获并传递，同时只执行一次 LLM 调用。
full_chain = (
    # 这里的字典，其实是 prompt_transform (ChatPromptTemplate) 的入参。
    # ChatPromptTemplate 会从字段中提取 key=specifications 的内容并替换到 prompt 中。
    # 所以这里的 key 需要和 ChatPromptTemplate 中定义的变量名 `{specifications}` 保持一致。
    {"specifications": extraction_chain}
    # 在这里拦截并打印中间结果，使用 lambda 传递自定义标题
    | RunnablePassthrough(lambda x: print_intermediate(x, "Extract 步骤的输出 → Transform 步骤的输入"))
    | prompt_transform
    | llm
    | StrOutputParser()
)

# --- 运行链 ---
input_text = "The new laptop model features a 3.5 GHz octa-core processor, 16GB of RAM, and a 1TB NVMe SSD."
print("\n--- 输入文本 ---")
print(input_text)

# 执行完整的链，中间结果会通过 RunnablePassthrough 自动打印
final_result = full_chain.invoke({"text_input": input_text})

print("\n--- Final JSON Output ---")
print(final_result)

"""
输出示例 | Example Output:
--- Final JSON Output ---
{
    "cpu": "3.5 GHz octa-core",
    "memory": "16GB",
    "storage": "1TB NVMe SSD"
}
"""