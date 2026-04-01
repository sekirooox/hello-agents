from agent import OpenAiChatClient
from utils import *
from openai import OpenAI
import re
API_KEY ='sk-cp-BrIDPeDEbO4sWRicd2Q_ZNo0_sbE0RgRfun5-mLWTEtRB2W9gIjN8f64Dz8-i8cUKLC1kwK70GPGy2ArtfGcMF_zq4Awn_Y4-ToMqhskLsa0DZpEClrS0Ns'
model_name = 'MiniMax-M2.7'
os.environ["TAVILY_API_KEY"] = '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'
agent = OpenAiChatClient(
    model_name=model_name,
    api_key=API_KEY
)

def main():
    user_prompt = "你好, 请帮助我查询今天广州的天气, 然后根据天气推荐一个合适的旅行计划"
    prompt_history = [f'user prompt: {user_prompt}\n']
    print(f"user prompt: {user_prompt}\n" + "="*40)
    
    for i in range(5):
        print(f"--- 循环 {i+1} ---\n")
        context = "\n".join(prompt_history) # 所有聊天记录拼接在一起
        print(f'上下文:{context}\n'+'='*40)
        response = agent.generate(prompt=context,system_prompt=AGENT_SYSTEM_PROMPT)
        print(f'模型输出:{response}\n')

        # 解析回答
        match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', response, re.DOTALL)
        if match:
            truncated = match.group(1).strip()
            if truncated != response.strip():
                response = truncated
                print("已截断多余的 Thought-Action 对")
        prompt_history.append(response)# 输出Thought:xxx Action:xxx

        # 解析Action
        action_match = re.search(r"Action: (.*)", response, re.DOTALL)
        if not action_match:
            # 错误动作, 直接返回Observation
            observation = "错误: 未能解析到 Action 字段。请确保你的回复严格遵循 'Thought: ... Action: ...' 的格式。"
            observation_str = f"Observation: {observation}"
            print(f"{observation_str}\n" + "="*40)
            prompt_history.append(observation_str)
            continue
        action_str = action_match.group(1).strip()
        if action_str.startswith("Finish"):
            finish_match = re.search(r"Finish\[(.*)\]", action_str, re.DOTALL)
            if finish_match:
                final_answer = finish_match.group(1)
            else:
                final_answer = action_str.replace("Finish", "").strip()
            print(f"任务完成, 最终答案为: {final_answer}")
            break


        # 获得任务参数
        tool_name = re.search(r"(\w+)\(", action_str).group(1)
        args_str = re.search(r"\((.*)\)", action_str).group(1)
        kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

        # 获得工具和回复
        if tool_name in available_tools:
            observation = available_tools[tool_name](**kwargs)
        else:
            observation = f"错误: 未知的工具 '{tool_name}'。请检查工具名称是否正确，并确保它在可用工具列表中。"

        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)
if __name__ == '__main__':
    main()
