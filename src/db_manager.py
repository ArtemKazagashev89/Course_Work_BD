import psycopg2

class DB_Manager():
    def __init__(self):
        pass

    def get_companies_and_vacancies_count(self):
        """Функция получает список всех компаний и количество вакансий у каждой компании."""
        pass

    def get_all_vacancies(self):
        """Функция  получает список всех вакансий с указанием названия компании"""
        pass

    def get_avg_salary(self):
        """Функция получает среднюю зарплату по вакансиям"""
        pass

    def get_vacancies_with_higher_salary(self):
        """Функция  получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass

    def get_vacancies_with_keyword(self, keyword):
        """Функция получает список всех вакансий, по ключевому слову"""
        pass