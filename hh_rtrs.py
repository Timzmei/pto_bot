import requests
import json
import pandas as pd


def get_rtrn_vocancies():


    # Выполняем GET-запрос к API HeadHunter
    url = "https://api.hh.ru/vacancies"
    params = {
        "area": 99,
        "industry": 47, # "Нефть и газ",
        "industry": 46, # "Энергетика"
        "industry": 45, # "Добывающая отрасль",
        "industry": 9, # "name": "Телекоммуникации, связь",
        "industry": 7, # "name": "Информационные технологии, системная интеграция, интернет"
        # "only_with_salary": 'true',
        "professional_role": 100, # [{'id': '100', 'name': 'Прораб, мастер СМР'}]
        "professional_role": 111, # [{'id': '111', 'name': 'Сервисный инженер, инженер-механик'}]
        "professional_role": 112, # [{'id': '112', 'name': 'Сетевой инженер'}]
        "professional_role": 114, # [{'id': '114', 'name': 'Системный инженер'}]
        "professional_role": 116, # [{'id': '116', 'name': 'Специалист по информационной безопасности'}]
        "professional_role": 144, # [{'id': '144', 'name': 'Инженер-энергетик, инженер-электрик'}]
        "professional_role": 169, # [{'id': '169', 'name': 'Инженер-электроник, инженер-электронщик'}]
        "professional_role": 174, # [{'id': '174', 'name': 'Инженер ПНР'}]
        "professional_role": 40, # [{'id': '40', 'name': 'Другое'}]
        "professional_role": 47, # [{'id': '47', 'name': 'Инженер ПТО, инженер-сметчик'}]
        "professional_role": 48, # [{'id': '48', 'name': 'Инженер-конструктор, инженер-проектировщик'}]
        "per_page": 100,
        "text": "инженер"
    }



    response = requests.get(url, params=params)

    # Проверяем, успешно ли выполнен запрос
    if response.status_code == 200:
        # Преобразуем JSON-ответ в словарь
        data = response.json()

        # Записываем JSON-данные в файл
        with open("vacancies.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
            print("JSON-данные успешно записаны в файл 'vacancies.json'")
    else:
        print(f"Ошибка при выполнении запроса: {response.status_code}")

    # Теперь мы имеем JSON-данные в файле 'vacancies.json'

    # Загружаем JSON-данные из файла
    with open("vacancies.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    # Преобразуем JSON в DataFrame
    df = pd.json_normalize(data["items"])

    # # Сохраняем DataFrame в файл Excel без кодировки
    # df.to_excel("vacancies_4.xlsx", index=False)
    # print("Данные успешно сохранены в файл Excel 'vacancies.xlsx'")


    filtered_df = df.copy()  # Создаем копию DataFrame


    # Выбираем только интересующие столбцы

    columns_to_keep = [
        'name',                     # Название вакансии
        'published_at',             # Дата публикации вакансии
        'area.name',                # Регион
        'employer.name',            # Название работодателя
        'salary.from',              # Минимальная зарплата
        'salary.to',                # Максимальная зарплата
        'alternate_url',            # Адрес вакансии на сайте
        'snippet.requirement',      # Требования к кандидатам
        'snippet.responsibility',   # Обязанности кандидатов
        'experience.name',          # Опыт работы
        'address.raw'               # Адрес работодателя
    ]

    filtered_df = filtered_df[columns_to_keep]

    # Заменяем наименования столбцов на свои собственные
    new_column_names = {
        'name': 'Название вакансии',
        'published_at': 'Дата публикации вакансии',
        'area.name': 'Регион',
        'employer.name': 'Работодатель',
        'salary.from': 'Минимальная зарплата',
        'salary.to': 'Максимальная зарплата',
        'alternate_url': 'Адрес вакансии на сайте',
        'snippet.requirement': 'Требования',
        'snippet.responsibility': 'Обязанности',
        'address.raw': 'Адрес работодателя'
    }

    filtered_df.rename(columns=new_column_names, inplace=True)

    # Сохраняем отфильтрованный DataFrame в файл Excel
    filtered_df.to_excel("filtered_vacancies.xlsx", index=False)
    print("Отфильтрованные данные успешно сохранены в файл Excel 'filtered_vacancies.xlsx'")
    
    # return filtered_df