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
import json

from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, blue, green
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
from flask import send_file

from aiogram.utils import keyboard
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from nova_ai.nova_bot import Nova_bot

from main import bot, BOT_TOKEN


user_scores = {}
current_question = 1

router = Router()
web_app = WebAppInfo(url='https://timzmei.github.io/pto_bot')

pdfmetrics.registerFont(TTFont('DejaVu', 'dejavu-sans.book.ttf'))  # Замените 'DejaVuSans.ttf' на имя вашего шрифта
pdfmetrics.registerFont(TTFont('DejaVu-Bold', 'dejavu-sans.bold.ttf'))  # Замените 'DejaVuSans.ttf' на имя вашего шрифта
pdfmetrics.registerFont(TTFont('DejaVu-Italic', 'dejavu-sans.oblique.ttf'))  # Замените 'DejaVuSans.ttf' на имя вашего шрифта


# Создаем PDF-файл
def create_pdf(test_name, test_result, text_result, questions_answers, from_user_username, from_user_id, doctor_name='', clinic_logo='', clinic_name='MentalHelp'):
    now = datetime.now()
    current_date = now.strftime("%d.%m.%Y")

    pdf_filename = f"Результаты теста.pdf"  # Имя PDF-файла

    c = canvas.Canvas(pdf_filename, pagesize=A4)


    # Устанавливаем цвет шрифта
    c.setFillColor(black)
    # Устанавливаем стиль (жирность и курсив) для шрифта
    c.setFont("DejaVu-Bold", 10)
    
    # Добавляем информацию о тестируемом, лечащем враче и клинике
    c.rect(170, 815, 250, 18)  # Координаты и размеры рамки
    c.drawString(45, 820, f"Имя тестируемого:")
    c.rect(170, 795, 250, 18)  # Координаты и размеры рамки
    c.drawString(45, 800, f"Лечащий врач:")  # Поле для заполнения
    # Добавляем информацию о тесте и результатах
    c.drawString(45, 760, f"Дата прохождения:")
    c.drawString(45, 730, f"Название теста:")
    c.drawString(45, 715, f"Результат:")
    c.drawString(45, 700, f"Описание результата:")
    
    c.setFont("DejaVu", 9)
    c.drawString(180, 820, f"{from_user_username}")
    c.drawString(180, 760, f"{current_date}")
    c.drawString(180, 730, f"{test_name}")
    c.drawString(180, 715, f"{test_result}")
    c.drawString(180, 700, f"{text_result}")
    # Добавляем логотип клиники
    c.drawImage('MentalHelp.jpg', 450, 735, width=100, height=100)

    # Добавляем информацию о вопросах и ответах
    y = 670
    for qa in questions_answers:
        question = qa['question']
        answer = qa['answer']
        
        # Устанавливаем цвет шрифта
        c.setFillColor(blue)
        # Устанавливаем кириллический шрифт и размер
        c.setFont("DejaVu-Bold", 8)
        
        c.drawString(70, y, f"Вопрос: {question}")
        
        # Устанавливаем цвет шрифта
        c.setFillColor(black)        
        # Устанавливаем стиль (жирность и курсив) для шрифта
        c.setFont("DejaVu-Italic", 8)
        
        c.drawString(100, y - 15, f"Ответ: {answer}")
        y -= 30  # Переход на следующую строку

    c.save()

    return pdf_filename


# @router.message(Command('test'))
# async def start_test(message: types.Message):
#     await message.answer("Давай начнем тестирование. Выбери один из вариантов ответа для каждой группы утверждений:")
    # Здесь добавьте логику отправки вопросов и обработки ответов пользователя


# @router.message(F.text.contains('Тимур'))
# async def echo_timur(message: types.Message):
#     await message.answer('Тиму-у-ур!!! Хозяин, тут тебя вспомнили!!!')

@router.message(F.web_app_data)
async def buy_process(web_app_message):
    from_user_username = web_app_message.from_user.full_name
    from_user_id = web_app_message.from_user.id
    data_test_str = web_app_message.web_app_data.data
    print(f'data_test_str: {data_test_str}')
    data_test = json.loads(data_test_str)
    # Получаем информацию о тесте
    test_info = data_test[-1]
    print(f'data_test: {data_test}')
    print(f'test_info: {test_info}')
    test_name = test_info.get('test_name', 'Название теста не указано')
    test_result = test_info.get('result', 'Результат не указан')
    text_result = test_info.get('text_result', 'Текстовый результат не указан')
    

    # Получаем информацию о вопросах и ответах
    questions_answers = data_test[:-1]
    pdf_file = create_pdf(test_name, test_result, text_result, questions_answers, from_user_username, from_user_id)

    # Выводим информацию о тесте
    print(f"Название теста: {test_name}")
    print(f"Результат: {test_result}")
    print(f"Текстовый результат: {text_result}")

    # Выводим информацию о вопросах и ответах
    for qa in questions_answers:
        print(f"\nВопрос: {qa['question']}")
        print(f"Ответ: {qa['answer']}")
    
    # print(from_user_username, web_app_message.web_app_data.data)
    
    await web_app_message.answer(f'Тест завершен.\nТестировался: {from_user_username}\nНазвание теста: {test_name}\nРезультат: {test_result}\n{text_result}', reply_markup=ReplyKeyboardRemove())
    await bot.send_document(244063420, FSInputFile('Результаты теста.pdf'), caption=f'Тест завершен.\nТестировался: {from_user_username}\nНазвание теста: {test_name}\nРезультат: {test_result}\n{text_result}')


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
        [
            types.KeyboardButton(text="Шкала безнадежности Бека"
                                 , web_app=WebAppInfo(url=f"https://timzmei.github.io/pto_bot?paramName=test_BHI"))
        ],
        [
            types.KeyboardButton(text="Опросник выраженности психопатологической симптоматики"
                                 , web_app=WebAppInfo(url=f"https://timzmei.github.io/pto_bot?paramName=SCL_90_R"))
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
    