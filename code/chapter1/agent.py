from openai import OpenAI
class OpenAiChatClient:
    def __init__(
        self,
        model_name:str,
        api_key:str,
        base_url:str = "https://api.minimaxi.com/v1",# minimax
    ):
        self.model_name = model_name
        self.client = OpenAI(api_key = api_key, base_url=base_url)
        
    def generate(
        self,
        prompt:str,
        system_prompt:str
    ) -> str:
        try:
            messages = [
                            {'role': 'system', 'content': system_prompt},
                            {'role': 'user', 'content': prompt}
                    ]
            model = self.model_name
            raw_response = self.client.chat.completions.create(
                model = model,
                messages = messages,
                stream = False,
            )
            response = raw_response.choices[0].message.content
            # print("大语言模型响应成功。")
            return response
        except Exception as e:
            print(f"调用LLM API时发生错误: {e}")
            return "错误:调用语言模型服务时出错。"                