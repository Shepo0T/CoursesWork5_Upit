import requests
import psycopg2
from typing import Any

employeers_id = [2455048, 28275, 2367681, 1122462, 4311669, 50629, 89779, 21094, 751020, 9802693]


def get_employeers_data() -> list[dict[str, Any]]:
    """Получение данных о 10 работодателях"""

    employeers = []
    for employeer_id in employeers_id:
        url_employeer = f'https://api.hh.ru/employers/{employeer_id}'
        employer_info = requests.get(url_employeer, ).json()
        employeers.append(employer_info)

    return employeers


def get_vacancies_data() -> list[dict[str, Any]]:
    """Получение данных о вакансиях 10 работодателей"""
    vacancies = []
    for employeer_id in employeers_id:
        url_vacancy = f'https://api.hh.ru/vacancies?employer_id={employeer_id}'
        vacancies_info = requests.get(url_vacancy,
                                      params={'page': 0, 'per_page': 100, 'only_with_salary': True}).json()
        vacancies.extend(vacancies_info['items'])
    return vacancies


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE employeers (
                    employeer_id INT PRIMARY KEY,
                    employeer_name TEXT NOT NULL,
                    URL TEXT,
                    count_open_vacancies INT
                )
            
            """)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE vacancies (
                    vacancies_id INT PRIMARY KEY,
                    employeer_id INT REFERENCES employeers(employeer_id),
                    name_vacancy TEXT NOT NULL,
                    salary INT,
                    URL_vacancy TEXT NOT NULL
                )
                    
            """)

    conn.commit()
    conn.close()


def save_data_to_database(data_employeers: list[dict[str, Any]], data_vacancies: list[dict[str, Any]],
                          database_name: str, params: dict) -> None:
    """Сохранение полученных данных в базу данных"""
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employeer in data_employeers:
            cur.execute(
                """
                INSERT INTO employeers (employeer_id, employeer_name, URL, count_open_vacancies)
                VALUES (%s, %s, %s, %s)
                """,
                (employeer['id'], employeer['name'], employeer['alternate_url'], employeer['open_vacancies'])
            )
        for vacancy in data_vacancies:
            cur.execute(
                """
                INSERT INTO vacancies (vacancies_id, employeer_id, name_vacancy, salary,URL_vacancy)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (vacancy.get('id'), vacancy['employer']['id'], vacancy['name'], vacancy['salary']['from'],
                 vacancy['alternate_url'])
            )
    conn.commit()
    conn.close()



