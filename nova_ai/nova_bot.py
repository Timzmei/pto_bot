import openai as novaai
import os
from dotenv import load_dotenv
import g4f, asyncio

g4f.debug.logging = True # enable logging
g4f.check_version = False # Disable automatic version checking


class Nova_bot:
  # Загрузить переменные окружения из .env файла
  load_dotenv()

  # Получить значение переменных окружения
  NOVA_AI_TOKEN = os.environ.get("NOVA_AI_TOKEN")

  # Установка базового URL и API-ключа novaai
  novaai.api_base = 'https://api.nova-oss.com/v1'
  novaai.api_key = NOVA_AI_TOKEN


  semaphore = asyncio.Semaphore(1)

  # @classmethod
  # async def create_chat_completion(cls, messages):
  #     # Создание объекта ChatCompletion с использованием данных из chat_instance
  #     # messages = await cls.get_messages()
  #     completion = novaai.ChatCompletion.create(
  #         model="gpt-3.5-turbo",
  #         messages=messages
  #     )
  #     print(f'messages={messages}\n')
  #     print(f'completion={completion}\n')
  #     return completion.choices[0].message.content
  @classmethod
  async def create_chat_completion(cls, messages):
      try:
          print("Начало create_chat_completion")
          async with cls.semaphore:
            completion = await g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_35_turbo,
                messages=messages
            )
          print("Завершение create_chat_completion")
          return completion
      except Exception as e:
          # Обработка ошибки
          print(f"Произошла ошибка: {e}")
          return None  # Возврат None или другого значения, чтобы показать, что произошла ошибка


        


  @classmethod
  def get_messages(cls, all_messages, all_users):
    system_info = 'You are a useful, but not particularly talkative chat assistant who loves sarcasm, black humor and girls. When it is necessary to show empathy and care. Chat participants: Timur and Gulnaz and a useful assistant. Gulnaz likes to communicate in Spanish'

    messages = []
    messages.append({'role': 'system', 'content': system_info})
    for message in all_messages:
      text = message.text
      name = ''
      role = 'user'
      for user in all_users:
        if user.id == message.user:
          name = user.first_name
          if user.username == 'rtrs_pto_bot':
            role = 'assistant'
      messages.append({'role': role, 'name': name, 'content': text})
    return messages
  
  
# async def main():
#   text = await Nova_bot.create_chat_completion([{"role": "user", "content": "Hello"}])
#   print(text)

# if __name__ == "__main__":
#     asyncio.run(main())
          