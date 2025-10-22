import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

def ensure_output_dir():
    """
    确保 output 目录存在
    """
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def save_to_markdown(content, filename, title, step_number=None):
    """
    将内容保存为 markdown 格式文件
    
    Args:
        content: 要保存的内容
        filename: 文件名（不含扩展名）
        title: markdown 文件的标题
        step_number: 步骤编号（可选）
    """
    output_dir = ensure_output_dir()
    filepath = os.path.join(output_dir, f"{filename}.md")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        if step_number:
            f.write(f"**步骤 {step_number}**\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        f.write(content)
        f.write("\n")
    
    print(f"✓ 已保存到: {filepath}")

def save_and_passthrough(filename, title, step_number=None):
    """
    创建一个可以保存内容并传递的函数，用于 RunnablePassthrough
    
    Args:
        filename: 文件名（不含扩展名）
        title: markdown 文件的标题
        step_number: 步骤编号（可选）
    
    Returns:
        一个接受内容并返回内容的函数
    """
    def _save(content):
        save_to_markdown(content, filename, title, step_number)
        return content
    return _save

def read_bruco_story():
    """
    读取 practices/bruco_story.txt 文件内容并返回
    
    Returns:
        str: 文件内容，如果文件不存在则返回 None
    """
    file_path = os.path.join(os.path.dirname(__file__), "bruco_story.txt")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
        return None
    except Exception as e:
        print(f"读取文件时出错：{e}")
        return None

# 初始化语言模型
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.25,
)

# --- Prompt 1: 总结市场故事  ---
summarize_prompt = ChatPromptTemplate.from_template(
    "Summarize the key findings of the following market story: \n\n{story}."
)

# --- Prompt 2: 推测未来趋势  ---
forecast_prompt = ChatPromptTemplate.from_template(
    "Based on the following summary, forecast the potential market trends for the next year:\n\n{summary}"
)

# --- Prompt 3: 生成投资建议  ---
suggest_prompt = ChatPromptTemplate.from_template(
    "Based on the market trend forecast below, provide investment suggestions:\n\n{forecast}"
)

# 构建 prompt chain

# 步骤 1: 总结市场故事
summarize_chain = (
    summarize_prompt
    | llm
    | StrOutputParser()
    | RunnablePassthrough(save_and_passthrough("01-summary", "市场故事总结", step_number=1))
)

# 步骤 2: 预测市场趋势
forecast_chain = (
    {"summary": summarize_chain}
    | forecast_prompt
    | llm
    | StrOutputParser()
    | RunnablePassthrough(save_and_passthrough("02-forecast", "市场趋势预测", step_number=2))
)

# 步骤 3: 生成投资建议
suggest_chain = (
    {"forecast": forecast_chain}
    | suggest_prompt
    | llm
    | StrOutputParser()
    | RunnablePassthrough(save_and_passthrough("03-suggestions", "投资建议", step_number=3))
)

# 完整的 prompt chain
full_chain = suggest_chain

# 执行完整的调用链
print("\n=== 开始执行 Prompt Chain ===\n")

story = read_bruco_story()
full_chain.invoke({"story": story})
print("\n✓ 所有步骤已完成，输出文件已保存到 practices/output/ 目录")
