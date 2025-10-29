import os
import time

os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

print("开始导入 crewai...")
start_time = time.time()
from crewai import Agent, Task, Crew
end_time = time.time()
import_time = end_time - start_time
print(f"crewai 导入完成，耗时: {import_time:.2f} 秒")

if __name__ == "__main__":
    print("Creating CrewAI agents...")