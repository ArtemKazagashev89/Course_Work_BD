from typing import Optional, List, Tuple

import psycopg2


class DBManager:
    """Класс для работы с данными в БД"""

    def __init__(self, db_name: str, user: str, password: str) -> None:
        self.conn = psycopg2.connect(database=db_name, user="postgres", password=39303, port=5432)
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, Optional[int]]]:
        """Функция получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT name, COUNT(v.id) FROM companies c LEFT JOIN vacancies v ON c.id = v.company_id GROUP BY c.id"
            )
            return cursor.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, int, int, str]]:
        """Функуия получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT v.title, c.name, v.salary_min, v.salary_max, v.url FROM vacancies v JOIN companies c ON v.company_id = c.id"
            )
            return cursor.fetchall()

    def get_avg_salary(self) -> float:
        """Функция получает среднюю зарплату по вакансиям"""
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT AVG(salary_min) FROM vacancies WHERE salary_min IS NOT NULL")
            return cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> List[Tuple[int, str, int, str, str]]:
        """Функция получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM vacancies WHERE salary_min > %s", (avg_salary,))
            return cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[int, str, int, str, str]]:
        """Функция получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM vacancies WHERE title ILIKE %s", ("%" + keyword + "%",))
            return cursor.fetchall()

    def close_connection(self):
        """Функция для закрытия конекшена с БД"""
        if self.conn:
            self.conn.close()
            self.conn = None
