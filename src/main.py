from src.config import config
from src.create_database import create_database, save_data_to_database
from src.db_manager import DBManager


def main():
    """Функция взаимодействия с пользователем"""

    db_manager = DBManager()
    params = config()

    while True:
        print("1. Получить компании и количество вакансий")
        print("2. Получить все вакансии")
        print("3. Получить среднюю зарплату")
        print("4. Получить вакансии с зарплатой выше средней")
        print("5. Получить вакансии по ключевому слову")
        print("0. Выход")

        choice = input("Выберите опцию: ")

        if choice == "1":
            print(db_manager.get_companies_and_vacancies_count())
        elif choice == "2":
            print(db_manager.get_all_vacancies())
        elif choice == "3":
            print(db_manager.get_avg_salary())
        elif choice == "4":
            print(db_manager.get_vacancies_with_higher_salary())
        elif choice == "5":
            keyword = input("Введите ключевое слово: ")
            print(db_manager.get_vacancies_with_keyword(keyword))
        elif choice == "0":
            break
        else:
            print("Некорректный выбор, попробуйте снова.")


if __name__ == "__main__":
    params = config()
    create_database(params)
    save_data_to_database(params)
    main()
