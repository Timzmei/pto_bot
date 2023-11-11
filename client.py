from webbrowser import get
import config
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile

from aiogram import types, F, Router, Bot
from aiogram.types import Message, Chat
from aiogram.filters import Command
from aiogram import Dispatcher
from datetime import datetime
from unidecode import unidecode
from collections import deque

import locale
import os




# from create_bot import dp
from hh_rtrs import get_rtrn_vocancies



import requests
import datetime


from dotenv import load_dotenv
from nova_ai.nova_bot import Nova_bot
# from chat import Chat  # Подключение Chat класса из файла chat.py

# Загрузить переменные окружения из .env файла
load_dotenv()

# Получить значение переменных окружения
open_weather_token = os.environ.get("OPEN_WEATHER_TOKEN")

lat = config.lat
lon = config.lon
novaai_instance = Nova_bot()

router = Router()
# Создание экземпляра Chat
# chat_instance = Chat()
my_queue = deque(maxlen=5)



@router.message(Command("start"))
async def start_command(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id

    # print(id_user)
    await message.reply(f'Привет, [{user_name}](tg://user?id={user_id})\!', parse_mode="MarkdownV2")
    await message.answer('Я - телеграм бот, созданный для помощи птошникам в различных задачах. Славлюсь умопомрачительной ртрс-ной сообразительностью)))')

    # await message.reply('Привет!')

@router.message(Command("hh_rtrn"))
async def get_hh_rtrs(message: types.Message):
    # await message.reply('Привет!')
    get_rtrn_vocancies()
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    # Отправьте файл пользователю с помощью InputFile
    await message.reply_document(FSInputFile('filtered_vacancies.xlsx'), caption=f"[{user_name}](tg://user?id={user_id}), держи табличку инженерных вакансий с HH.ru по Уфе", parse_mode="Markdown")

    
@router.message(F.text)
async def echo_happy_birthday(message: Message):
    message_id = message.message_id
    from_user_name = transliterate_text(message.from_user.first_name)
    message_text = message.text
    my_queue.append({'role': 'user', 'name': from_user_name, 'content': message_text})
    
    timur_id = 244063420
    gulnaz_id = 664985225
    rustam_id = 375124231
    svetlana_id = 670877555
    kristina_id = 332786839
    
    normal_info = '''You are a very rude and grumpy, but useful chat assistant named "Toxic", who loves sarcasm and black humor very much. 
        You should always present yourself as toxic. Chat participants: Timur, Svetlana, Rustam, Kristina and Gulnaz, as well as a chat assistant. 
        Gulnaz likes to communicate in Spanish. Svetlana loves nature and animals very much, Rustam loves cars and swearing. Kristina loves hiking. 
        Timur also probably has positive qualities, but they are unknown. 
        It is appropriate to insert emoticons in the answers according to the meaning of the text. 
        If the question is not addressed to you, but to other chat participants, then you should send an empty line. 
        If necessary, intercede for Svetlana'''
        
    svetlana_info = '''You are a useful chat assistant named "Toxic" who loves sarcasm and black humor very much. 
        You should always present yourself as toxic. Chat participants: Timur, Svetlana, Rustam, Kristina and Gulnaz, as well as a chat assistant. 
        Gulnaz likes to communicate in Spanish. Svetlana loves nature and animals very much, Rustam loves cars and swearing. Kristina loves hiking. 
        Timur also probably has positive qualities, but they are unknown. 
        It is appropriate to insert emoticons in the answers according to the meaning of the text. 
        If the question is not addressed to you, but to other chat participants, then you should send an empty line. 
        If necessary, intercede for Svetlana'''
    
    timur_info = '''You are a useful, but extremely grumpy and harmful chat assistant named "Toxic", who loves sarcasm and swears a lot. 
        You should always present yourself as toxic. Chat participants: Timur, Svetlana, Rustam, Kristina and Gulnaz, as well as a chat assistant. 
        Gulnaz likes to communicate in Spanish. Svetlana loves nature and animals very much, Rustam loves cars. Kristina loves hiking. 
        Timur also probably has positive qualities, but they are unknown. 
        It is appropriate to insert emoticons in the answers according to the meaning of the text. 
        If the question is not addressed to you, but to other chat participants, then you should send an empty line. 
        If necessary, intercede for Svetlana'''
    
    gulnaz_info = '''You are a useful chat assistant named "Toxic" who loves sarcasm and black humor very much. 
        You should always present yourself as toxic. Chat participants: Timur, Svetlana, Rustam, Kristina and Gulnaz, as well as a chat assistant. 
        Gulnaz likes to communicate in Spanish. Svetlana loves nature and animals very much, Rustam loves cars. Kristina loves hiking. 
        Timur also probably has positive qualities, but they are unknown. 
        It is appropriate to insert emoticons in the answers according to the meaning of the text. 
        If the question is not addressed to you, but to other chat participants, then you should send an empty line. 
        If necessary, intercede for Svetlana'''
    
    if message.from_user.id == 244063420:
        messages = get_messages(list(my_queue), timur_info)
    if message.from_user.id == 664985225:
        messages = get_messages(list(my_queue), gulnaz_info)
    if message.from_user.id == 670877555:
        messages = get_messages(list(my_queue), svetlana_info)
    else:
        messages = get_messages(list(my_queue), normal_info)
           
    print(f'перед передачей в AI = {messages}')
    text = await novaai_instance.create_chat_completion(messages)
    text = text.replace('Chatbase', '***')
    text = text.replace('I am not sure. Email support@chatbase.co for more info.', 'Давай не будем, я тебя умоляю')
    
    my_queue.append({'role': 'assistant', 'name': 'rtrs_pto_bot', 'content': text})
    # print(text)
    await message.reply(text)

def get_messages(my_queue, info):

    
    system_info = info
    messages = []
    messages.append({'role': 'system', 'content': system_info})
    print(f'add system info = {messages}')
    for message in my_queue:
      messages.append(message)
    print(f'add messages = {messages}')
    return messages

def transliterate_text(text):
    transliterated_text = ""
    
    for char in text:
        if char.isalpha() and char.isascii():
            # Символ является буквой латинского алфавита или другим символом ASCII
            transliterated_text += char
        else:
            # Символ не является буквой латинского алфавита
            transliterated_text += unidecode(char)
    
    return transliterated_text


# @router.message()
# async def echo_send(message: types.Message):
#     if ('привет' in message.text.lower()):
#         await message.answer('И тебе привет!')  
#     elif ('погода' in message.text.lower() and 'какая' in message.text.lower()):
#         text = get_weater()
#         await message.reply(text, parse_mode="HTML")
    
# @router.message(Command("О_боте"))
# async def about(message: types.Message):
#     # await message.reply('Привет!')
#     await message.answer('Я - телеграм бот, созданный для помощи птошникам в различных задачах. Славлюсь умопомрачительной ртрс-ной сообразительностью)))')


    
# @router.message()
# async def get_weather(message: types.Message):
#     if ('погода' in message.text.lower() and 'какая' in message.text.lower()):
#         text = get_weater()
#         await message.reply(text, parse_mode="HTML")
            
def get_weater():
    code_to_smile = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B"
    }

    try:
        # Устанавливаем локаль на русский язык
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={open_weather_token}&units=metric&lang=ru"
        )
        # print(r)
        data = r.json()
        # print(data)
        
        # Извлечение информации о текущей погоде
        current_weather = data['current']
        current_temperature = current_weather['temp']
        current_description = current_weather['weather'][0]['description']

        # Извлечение информации о прогнозе на несколько дней
        daily_forecast = data['daily']

        # Формирование ответа в HTML-стиле
        html_response = f"<b>Текущая погода:</b> {current_description}, <b>Температура:</b> {current_temperature}°C\n\n"
        html_response += "<b>Прогноз на несколько дней:</b>\n"

        for day in daily_forecast:
            date = day['dt']
            # date = datetime.datetime.fromtimestamp(day['dt']).strftime('%d.%m.%Y %A')
            temperature_morn = day['temp']['morn']
            temperature_day = day['temp']['day']
            temperature_eve = day['temp']['eve']
            temperature_night = day['temp']['night']
            description = day['weather'][0]['description']
            feels_like_morn = day['feels_like']['morn']
            feels_like_day = day['feels_like']['day']
            feels_like_eve = day['feels_like']['eve']
            feels_like_night = day['feels_like']['night']
            
            formatted_date = format_date(date)
            
            html_response += f"<b>{formatted_date}</b>\n"
            html_response += f"<b>ночь: <i>{temperature_night}°C</i></b> - <b>день: <i>{temperature_day}°C</i></b>\n"            
            # html_response += f"<b>Температура:</b>\n"
            # html_response += f"<i>Утром:</i> <b><i>{temperature_morn}°C</i></b>, <i>ощущается:</i> <b><i>{feels_like_morn}°C</i></b>\n"
            # html_response += f"<i>Днем:</i> <b><i>{temperature_day}°C</i></b>, <i>ощущается:</i> <b><i>{feels_like_day}°C</i></b>\n"
            # html_response += f"<i>Вечером:</i> <b><i>{temperature_eve}°C</i></b>, <i>ощущается:</i> <b><i>{feels_like_eve}°C</i></b>\n"
            # html_response += f"<i>Ночью:</i> <b><i>{temperature_night}°C</i></b>, <i>ощущается:</i> <b><i>{feels_like_night}°C</i></b>\n"
            html_response += f"<i>{description}</i> \n\n"

        # Теперь у вас есть ответ в HTML-стиле, который вы можете использовать в телеграм-боте
        # print(datetime.datetime.fromtimestamp(day['dt']).strftime('%d.%m.%Y'))
        return html_response
    except:
        return "\U00002620 Кто тут? \U00002620"
    
    
def format_date(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)
    formatted_date = dt.strftime('%d.%m.%Y %A')
    return formatted_date

        
def get_location():
            r = requests.get(
            f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=5&appid={open_weather_token}")
            data = r.json()
            location = data[0]["local_names"]["ru"]
            return location
        
# def register_handlers_client(dp : Dispatcher):
#     dp.register_message_handler(get_weather, commands=['погода'])
#     dp.register_message_handler(get_hh_rtrs, commands=['hh_rtrn'])
#     dp.register_message_handler(start_command, commands=['start'])
#     dp.register_message_handler(about, commands=['О_боте'])