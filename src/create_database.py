import psycopg2
from src.get_data_hh import get_companies, get_vacancies

def create_database(database_name: str, user: str, password: str) -> None:
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях."""

    conn = psycopg2.connect(dbname="postgres", user=user, password=password, port=5432)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, user=user, password=password, port=5432)

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


def save_data_to_database(database_name: str, user: str, password: str) -> None:
    """Сохранение данных о компаниях и вакансиях в базу данных."""
    conn = psycopg2.connect(dbname=database_name, user=user, password=password, port=5432)
    cur = conn.cursor()

    companies = get_companies([49357, 106223, 1159819, 61750, 4750373, 5560707, 5563417, 1353073, 67843, 2603304])
    for company in companies:
        cur.execute("INSERT INTO companies (name) VALUES (%s) RETURNING company_id", (company["name"],))
        company_id = cur.fetchone()[0]

        vacancies = get_vacancies(company["id"])
        for vacancy in vacancies:
            salary = vacancy.get("salary")
            salary_from = salary.get("from") if salary else None
            salary_to = salary.get("to") if salary else None
            name = vacancy.get("name")
            published_at = vacancy.get("published_at")
            responsibility = vacancy.get("snippet", {}).get("responsibility", "")

            # Отладочный вывод
            print(f"Inserting into vacancies: company_id={company_id}, name={name}, salary_from={salary_from}, salary_to={salary_to}, published_at={published_at}, responsibility={responsibility}")

            cur.execute(
                "INSERT INTO vacancies (company_id, name, salary, published_at, responsibility) VALUES (%s, %s, %s, %s, %s)",
                (
                    company_id,
                    name,
                    salary_from,
                    published_at,
                    responsibility,
                ),
            )

    conn.commit()
    cur.close()
    conn.close()
