from typing import Any, Dict

import psycopg2

from src.get_data_hh import get_companies, get_vacancies


def create_database(database_name: str, params: Dict[str, Any]) -> None:
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях."""

    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE companies (
                company_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            )
        """
        )

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE vacancies (
                vacancies_id SERIAL PRIMARY KEY,
                company_id INT REFERENCES companies(company_id),
                name VARCHAR NOT NULL,
                salary INTEGER,
                published_at DATE,
                responsibility TEXT
            )
        """
        )

    conn.commit()


def save_data_to_database(database_name: str, params: Dict[str, Any]) -> None:
    """Сохранение данных о компаниях и вакансиях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)
    cur = conn.cursor()

    companies = get_companies
    for company in companies:
        cur.execute("INSERT INTO companies (name) VALUES (%s)", (company["name"],))
        company_id = cur.fetchone()[0]

        vacancies = get_vacancies(company["id"])
        for vacancy in vacancies:
            cur.execute(
                "INSERT INTO vacancies (company_id, name, salary,  published_at, responsibility) VALUES (%s, %s, %s, %s, %s)",
                (
                    company_id,
                    vacancy["name"],
                    vacancy["salary"],
                    vacancy["published_at DATE"],
                    vacancy["responsibility"],
                ),
            )

    conn.commit()
    cur.close()
    conn.close()
