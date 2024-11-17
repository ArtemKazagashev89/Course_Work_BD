from typing import Any, Dict, List

import requests

companies_ids = [49357, 106223, 1159819, 61750, 4750373, 5560707, 5563417, 1353073, 67843, 2603304]


def get_companies(companies_ids: List[int]) -> List[Dict[str, Any]]:
    """Получение данных о компаниях"""
    companies_data = []
    for company_id in companies_ids:
        response = requests.get(f"https://api.hh.ru/employers/{company_id}")
        if response.status_code == 200:
            companies_data.append(response.json())
    return companies_data


def get_vacancies(company_id: int) -> List[Dict[str, Any]]:
    """Получение данных о вакансиях"""
    vacancies_data = []
    response = requests.get(f"https://api.hh.ru/vacancies?employer_id={company_id}")
    if response.status_code == 200:
        vacancies_data.extend(response.json().get("items", []))
    return vacancies_data
