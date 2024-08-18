from src import utils
from src.DBManager import DBManager
from src.config import config
import click


def main():
    params = config()
    employeers_data = utils.get_employeers_data()
    vacancies_data = utils.get_vacancies_data()
    utils.create_database('hh', params)
    utils.save_data_to_database(employeers_data, vacancies_data, 'hh', params)
    db_manager = DBManager(params)
    print(f"Выберите запрос: \n"
          f"1 - Список всех компаний и количество вакансий у каждой компании\n"
          f"2 - Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n"
          f"3 - Средняя зарплата по вакансиям\n"
          f"4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
          f"5 - Список всех вакансий, в названии которых содержатся запрашиваемое слово\n"
          f"0 - Выход из программы")

    commands = {
        '1': db_manager.get_companies_and_vacancies_count,
        '2': db_manager.get_all_vacancies,
        '3': db_manager.get_avg_salary,
        '4': db_manager.get_vacancies_with_higher_salary,
        '5': db_manager.get_vacancies_with_keyword,
        '0': exit}

    while True:
        try:
            user_select = input('выбери что-нибудь\n')
            commands.get(user_select)()
            click.pause()

        except ValueError:
            print('Можно только цифры')


if __name__ == '__main__':
    main()
