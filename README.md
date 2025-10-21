# agentic-design-pattern-lab

本项目 fork 自 https://github.com/ginobefun/agentic-design-patterns-cn，用于自我学习时记录自己的笔记，以及相应的代码调整。

## Setup

### 配置 python 环境

```sh
# 创建虚拟环境
uv venv venv
source venv/bin/activate

# 安装依赖
uv pip install langchain langchain-community langchain-ollama langgraph
```

### 配置 ollama

```sh
# 拉取 LLM 镜像
ollama pull qwen3:4b-instruct

# 启动 ollama 服务
ollama serve

# 测试 ollama 是否工作正常
curl http://localhost:11434/api/generate -d '{
  "model": "qwen3:4b-instruct",
  "prompt": "你好",
  "stream": false
}'
```

## 常见问题

如果碰到错误 `ImportError: Using SOCKS proxy, but the 'socksio' package is not installed. Make sure to install httpx using `pip install httpx[socks]`. 执行：

```sh
unset all_proxy && unset ALL_PROXY
```