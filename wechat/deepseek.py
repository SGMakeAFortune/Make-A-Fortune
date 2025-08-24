import logging

from openai import OpenAI

from settings.settings import settings

logger = logging.getLogger(__name__)


def get_suggestion(message):
    client = OpenAI(
        api_key=settings.DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com",
    )

    romantic_master_prompt = """
    你是一位充满诗意的浪漫主义爱情大师，具有以下特质：
    
    1. **语言风格**：优雅、温柔、深情，充满诗意的比喻和意象
    2. **情感表达**：善于用细腻的文字触动人心，表达深刻的情感
    3. **浪漫元素**：擅长运用月亮、星辰、花朵、微风等自然意象
    4. **回应方式**：总是用温暖而富有哲理的语言回应情感问题
    5. **你的用户**：你的用户是一位美丽温柔的大一女生
    6. **核心特质**：
       - 用诗意的语言描述爱情的美好
       - 善于发现生活中的浪漫细节
       - 用温柔的方式给予情感建议
       - 总是传递积极向上的爱情观
       - 擅长用比喻让抽象的情感变得具体可感
    
    请用你最浪漫的方式回应用户，不超过30字，让每个回答都像一首情诗般动人。
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": romantic_master_prompt},
            {"role": "user", "content": f"{message}，给出健康、出行、穿衣等建议"},
        ],
        stream=False,
    )

    return f"✨ 温馨提示：\n{response.choices[0].message.content}"
