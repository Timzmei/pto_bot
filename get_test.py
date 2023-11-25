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
def create_pdf(test_data, answers_array, result_test, from_user_username, from_user_id, test_name):
    pdf_filename = "test_results.pdf"
    
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    
    y_position = 750  # Начальная позиция на странице
    
    # Добавление информации на страницу
    def add_info(text, ypos):
        nonlocal y_position
        c.drawString(100, ypos, text)
        y_position -= 20
        if y_position < 50:  # Если информация не помещается, создаем новую страницу
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = 750  # Сбрасываем позицию на новой странице
            c.drawString(100, y_position, text)
            y_position -= 20
    
    # Добавление вопросов и ответов из answersArray
    add_info("Результаты теста:", y_position)
    for i, answer_dict in enumerate(answers_array, start=1):
        question_number = int(answer_dict['question'].split()[1]) - 1
        question_text = test_data["questions"][question_number]["question"]
        answer_value = answer_dict['answer']
        add_info(f"Вопрос {i}: {question_text}", y_position)
        add_info(f"Ответ: {answer_value}", y_position)
    
    # Добавление баллов по каждой шкале
    add_info("Баллы по каждой шкале:", y_position)
    for scale, score in result_test.items():
        add_info(f"{scale}: {score}", y_position)
    
    # # Добавление общего балла (GSI), индекс PSI и индекс PDSI
    # add_info(f"Общий балл (GSI): {total_score}", y_position)
    # add_info(f"Индекс PSI: {psi_count}", y_position)
    # add_info(f"Индекс PDSI: {pdsi}", y_position)
    
    c.save()
    print(f"PDF-файл с результатами теста создан: {pdf_filename}")

def get_test_data(test_name):
    # Путь к вашему JSON файлу с тестовыми данными
    json_file_path = f'{test_name}.json'

    # Загрузка данных из файла
    with open(json_file_path, 'r', encoding='utf-8') as file:
        test_data = json.load(file)
    return test_data

def get_result_test_scl(answersArray, test_data):
    
    # Суммирование баллов по каждой шкале
    scales = test_data["keys"][0]  # Получаем ключи для шкал

    scale_scores = {}  # Словарь для хранения баллов по каждой шкале

    for scale, items in scales.items():
        scale_scores[scale] = sum(1 for item in answersArray if int(item[f"Вопрос {item}"]) in items) / len(items)

    # Вычисление общего балла (индекс GSI)
    gsi_index = sum(scale_scores.values()) / len(answersArray)

    # Подсчет количества пунктов от 1 до 4 (индекс PSI)
    psi_count = sum(1 for item in answersArray if 1 <= int(item[f"Вопрос {item}"]) <= 4)

    # Расчет индекса выраженности дистресса PDSI
    pdsi_index = (gsi_index * len(answersArray)) / psi_count if psi_count != 0 else 0
    
    scale_scores['gsi_index'] = gsi_index
    scale_scores['psi_count'] = psi_count
    scale_scores['pdsi_index'] = pdsi_index

    return scale_scores, gsi_index, psi_count, pdsi_index

def get_total_scores(answersArray, test_data):
    
    result_test = {}
    total_score = 0
    
    for answer_dict in answersArray:
        question_number = int(answer_dict['question'].split()[1]) - 1  # Получаем номер вопроса из словаря
        question = test_data["questions"][question_number]
        selected_answer = next((ans for ans in question["answers"] if ans["value"] == int(answer_dict['answer'])), None)
        if selected_answer:
            total_score += selected_answer["value"]
    
    result_ranges = test_data['resultRanges']
    result_text = ''

    for result_range in result_ranges:
        if result_range["minScore"] <= total_score <= result_range["maxScore"]:
            result_text = result_range["resultText"]

    result_test['total_score'] = total_score
    result_test['result_text'] = result_text

    return result_test


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
    # test_result = test_info.get('result', 'Результат не указан')
    # text_result = test_info.get('text_result', 'Текстовый результат не указан')
    
    file_data = get_test_data(test_name)
    
    full_test_name = file_data['testName']

    # Получаем информацию о вопросах и ответах
    answers_array = data_test[:-1]
    
    result_test = {}
    
    if (test_name == 'SCL_90_R'):
        result_test = get_result_test_scl(answers_array, file_data)
    else:
        result_test = get_total_scores(answers_array, file_data)
    
    
    pdf_file = create_pdf(file_data, answers_array, result_test, from_user_username, from_user_id, full_test_name)

    # Выводим информацию о тесте
    print(f"Название теста: {full_test_name}")
    # print(f"Результат: {test_result}")
    # print(f"Текстовый результат: {text_result}")

    # # Выводим информацию о вопросах и ответах
    # for qa in questions_answers:
    #     print(f"\nВопрос: {qa['question']}")
    #     print(f"Ответ: {qa['answer']}")
    
    # print(from_user_username, web_app_message.web_app_data.data)
    
    await web_app_message.answer(f'Тест завершен.\nТестировался: {from_user_username}\nНазвание теста: {full_test_name}\nРезультат: {result_test}\n', reply_markup=ReplyKeyboardRemove())
    await bot.send_document(244063420, FSInputFile('Результаты теста.pdf'), caption=f'Тест завершен.\nТестировался: {from_user_username}\nНазвание теста: {full_test_name}\nРезультат: {result_test}')


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
    