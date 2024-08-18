import psycopg2
from prettytable import PrettyTable


class DBManager:
    """Класс для работы с данными в БД"""

    def __init__(self, params):
        self.conn = psycopg2.connect(dbname='hh', **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        self.cur.execute("""
        SELECT employeers.employeer_name, COUNT(vacancies.employeer_id) FROM employeers
        JOIN vacancies USING (employeer_id)
        GROUP BY employeers.employeer_name
        ORDER BY COUNT DESC
        """)
        table = PrettyTable()
        table.field_names = ['employeer', 'quantity_open_vacancy']
        table.add_rows(self.cur.fetchall())
        print(table)

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию"""
        self.cur.execute("""
        SELECT employeers.employeer_name, name_vacancy, salary,URL_vacancy
         FROM vacancies
         JOIN employeers USING(employeer_id)
         ORDER BY salary desc
         """)
        table = PrettyTable()
        table.field_names = ['employeer_name', 'name_vacancy', 'salary', 'URL_vacancy']
        table.add_rows(self.cur.fetchall())
        print(table)

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        self.cur.execute("""
        SELECT AVG(salary) FROM vacancies
        """)
        table = PrettyTable()
        table.field_names = ['avg_salary']
        table.add_rows(self.cur.fetchall())
        print(table)

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий,
        у которых зарплата выше средней по всем вакансиям"""
        self.cur.execute("""
        SELECT name_vacancy, salary FROM vacancies
        WHERE CAST(salary AS INTEGER) > (SELECT AVG(CAST(salary AS INTEGER)) FROM vacancies)
        """)
        table = PrettyTable()
        table.field_names = ['name_vacancy', 'salary']
        table.add_rows(self.cur.fetchall())
        print(table)

    def get_vacancies_with_keyword(self):
        """Получает список всех вакансий,
        в названии которых содержатся переданные в метод слова, например python"""
        keyword = input('Введите поисковый запрос: \n')
        self.cur.execute(f"""SELECT employeers.employeer_name, name_vacancy, salary,URL_vacancy
        FROM vacancies
        JOIN employeers USING(employeer_id)
        WHERE name_vacancy LIKE('%{keyword}%')
        """)
        table = PrettyTable()
        table.field_names = ['employeer_name', 'name_vacancy', 'salary', 'URL_vacancy']
        table.add_rows(self.cur.fetchall())
        print(table)
