from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile
from aiogram import types, Bot, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Dispatcher
from aiogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonDefault,
    MenuButtonWebApp,
    Message,
    WebAppInfo,
)
from datetime import datetime

from aiogram.utils import keyboard
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from nova_ai.nova_bot import Nova_bot

user_scores = {}
current_question = 1

router = Router()
web_app = WebAppInfo(url='https://timzmei.github.io/pto_bot')



# @router.message(Command('test'))
# async def start_test(message: types.Message):
#     await message.answer("Давай начнем тестирование. Выбери один из вариантов ответа для каждой группы утверждений:")
    # Здесь добавьте логику отправки вопросов и обработки ответов пользователя


# @router.message(F.text.contains('Тимур'))
# async def echo_timur(message: types.Message):
#     await message.answer('Тиму-у-ур!!! Хозяин, тут тебя вспомнили!!!')

@router.message(F.web_app_data)
async def buy_process(web_app_message):
    from_user_username = web_app_message.from_user.username
    from_user_id = web_app_message.from_user.id
    data_test = web_app_message.web_app_data.data
    
    # Получаем информацию о тесте
    test_info = data_test[-1]
    print(f'data_test: {data_test}')
    print(f'test_info: {test_info}')
    test_name = test_info['test_name']
    test_result = test_info['result']
    text_result = test_info['text_result']

    # Получаем информацию о вопросах и ответах
    questions_answers = data_test[:-1]

    # Выводим информацию о тесте
    print(f"Название теста: {test_name}")
    print(f"Результат: {test_result}")
    print(f"Текстовый результат: {text_result}")

    # Выводим информацию о вопросах и ответах
    for qa in questions_answers:
        print(f"\nВопрос: {qa['question']}")
        print(f"Ответ: {qa['answer']}")
    
    # print(from_user_username, web_app_message.web_app_data.data)
    
    # await web_app_message.answer(f'Тест завершен.\nТестировался: @{from_user_username}\n{test_info}', reply_markup=ReplyKeyboardRemove())


# Обработчик для команды /test
# @router.message(Command("test"))
# async def start_test(message: Message, bot: Bot):
#     user_id = message.from_user.id
    
#     kb = [
#         [
#             types.KeyboardButton(text="Шкала депрессии Бека", web_app=web_app)
#         ],
#     ]
#     keyboard = ReplyKeyboardMarkup(
#         keyboard=kb,
#         resize_keyboard=True,
#         input_field_placeholder="Выберите тест"
#     )
#     param_name = "test_BDI_mini"

#     await message.answer("Тестируемся", reply_markup=ReplyKeyboardRemove())
#     # await bot.set_chat_menu_button(
#     #     chat_id=message.chat.id,
#     #     menu_button=MenuButtonWebApp(text="Open Menu", web_app=WebAppInfo(url=f"https://timzmei.github.io/pto_bot?paramName={param_name}")),
#     # )
#     await bot.set_chat_menu_button(
#         chat_id=message.chat.id,
#         menu_button=MenuButtonDefault(text="Open Menu"),
#     )
#     await message.answer("Давай начнем тестирование. Выбери тест")
#     # await message.answer(message, reply_markup=keyboard)

@router.message(Command("тест"))
async def command_webview(message: Message):
    kb = [
        [
            types.KeyboardButton(text="Шкала депрессии Бека"
                                 , web_app=WebAppInfo(url=f"https://timzmei.github.io/pto_bot?paramName=test_BDI_mini"))
        ],
        [
            types.KeyboardButton(text="Шкала тревоги Бека"
                                 , web_app=WebAppInfo(url=f"https://timzmei.github.io/pto_bot?paramName=test_BAI"))
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Шкала депрессии Бека"
    )

    await message.answer(
        "Отлично\!\n Тесты разработаны психотерапевтом и создателем когнитивной психотерапии Аароном Беком\.\nБек работал в основном в области изучения и лечения депрессивных расстройств\.\n*Шкала депрессии Бека\.*\n_Тест предлагает оценить ваше состояние за прошедшую неделю по нескольким параметрам — отношение к будущему и к неудачам в прошлом\, испытываете ли вы чувство вины и грусти\, самокритика\.\n_*Шкала тревоги Бека\.*\n_Тест предлагает оценить ваше состояние за прошедшую неделю по нескольким симптомам тревоги — ощущение жара\, дрожь в ногах\, неспособность расслабиться\, страх\, затруднённое дыхание\._",
        parse_mode="MarkdownV2", reply_markup=keyboard
    )
    

# @router.message(~F.message.via_bot)  # Echo to all messages except messages via bot
# async def echo_all(message: Message):
#     param_name = "test_BDI"

#     await message.answer(
#         "Test webview",
#         reply_markup=InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [InlineKeyboardButton(text="Open", web_app=WebAppInfo(url=f"https://timzmei.github.io/pto_bot?paramName={param_name}"))]
#             ]
#         ),
#     )

# @router.message(content_types='web_app_data')
# async def test_process(web_app_message):
#     await web_app_message.send_invoice(web_app_message.chat.id,
#                            title='Laptop',
#                            need_email=True,
#                            start_parameter='example',
#                            payload='some_invoice')
    