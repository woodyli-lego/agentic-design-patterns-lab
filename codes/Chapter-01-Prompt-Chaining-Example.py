import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Initialize the Language Model (using local Ollama model)
# 初始化语言模型（使用本地 Ollama 模型）
llm = ChatOllama(model="qwen3:4b-instruct", temperature=0)

# --- Prompt 1: Extract Information ---
# --- 提示 1: 提取信息 ---
prompt_extract = ChatPromptTemplate.from_template(
    "Extract the technical specifications from the following text:\n\n{text_input}"
)

# --- Prompt 2: Transform to JSON ---
# --- 提示 2: 转换为 JSON ---
prompt_transform = ChatPromptTemplate.from_template(
    "Transform the following specifications into a JSON object with 'cpu', 'memory', and 'storage' as keys:\n\n{specifications}"
)

# --- Build the Chain using LCEL ---
# The StrOutputParser() converts the LLM's message output to a simple string.
# --- 使用 LCEL 构建链 ---
# StrOutputParser() 会将 LLM 的消息输出转换为一个简单的字符串。
extraction_chain = prompt_extract | llm | StrOutputParser()

# The full chain passes the output of the extraction chain into the 'specifications'
# variable for the transformation prompt.
# 完整的链将提取链的输出传递给转换提示中的 'specifications' 变量。
full_chain = (
    {"specifications": extraction_chain}
    | prompt_transform
    | llm
    | StrOutputParser()
)

# --- Run the Chain ---
# --- 运行链 ---
input_text = "The new laptop model features a 3.5 GHz octa-core processor, 16GB of RAM, and a 1TB NVMe SSD."
print("\n--- Input Text ---")
print(input_text)

# Execute the extraction chain first to see intermediate result
# 先执行提取链以查看中间结果
extracted_specs = extraction_chain.invoke({"text_input": input_text})

print("\n--- Intermediate Result (Extracted Specifications) ---")
print(extracted_specs)

# Execute the chain with the input text dictionary.
# 接收输入文本并执行链。
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