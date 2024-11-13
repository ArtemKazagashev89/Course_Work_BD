import psycopg2
from src.db_manager import DBManager
from src.get_data_hh import get_companies, get_vacancies


def main():
    """Функция взаимодействия с пользователем"""

    conn = psycopg2.connect(dbname='postgres', host='localhost', password=39303, port=5432)
    db_manager = DBManager()




    while True:
        print("1. Получить компании и количество вакансий")
        print("2. Получить все вакансии")
        print("3. Получить среднюю зарплату")
        print("4. Получить вакансии с зарплатой выше средней")
        print("5. Получить вакансии по ключевому слову")
        print("0. Выход")

        choice = input("Выберите опцию: ")

        if choice == '1':
            print(db_manager.get_companies_and_vacancies_count())
        elif choice == '2':
            print(db_manager.get_all_vacancies())
        elif choice == '3':
            print(db_manager.get_avg_salary())
        elif choice == '4':
            print(db_manager.get_vacancies_with_higher_salary())
        elif choice == '5':
            keyword = input("Введите ключевое слово: ")
            print(db_manager.get_vacancies_with_keyword(keyword))
        elif choice == '0':
            break
        else:
            print("Некорректный выбор, попробуйте снова.")

    conn.close()

if __name__ == "__main__":
    main()