# Setup

## 配置 python 环境

```sh
# 创建虚拟环境
uv venv venv
source venv/bin/activate

# 安装依赖
uv pip install langchain langchain-community langchain-openai langchain-ollama langgraph
```

## 配置 ollama

```sh
# 拉取 LLM 镜像
ollama pull qwen3:8b

# 启动 ollama 服务
ollama serve

# 测试 ollama 是否工作正常
curl http://localhost:11434/api/generate -d '{
  "model": "qwen3:4b-instruct",
  "prompt": "你好",
  "stream": false
}'
```

## 测试

```sh
cd codes
python 
```