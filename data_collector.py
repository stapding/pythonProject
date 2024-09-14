import requests
import time

class DataCollector:
    def __init__(self):
        self.api_url = "https://api.hh.ru/vacancies"
        self.params = {
            'text': 'Программист',
            'area': 1,  # Москва
            'per_page': 100
        }

    def fetch_data(self):
        response = requests.get(self.api_url, params=self.params)
        if response.status_code == 200:
            data = response.json()['items']
            # Преобразование данных в нужный формат
            processed_data = []
            for item in data:
                salary = item.get('salary')
                if salary:
                    salary_from = salary.get('from') or 0
                    salary_to = salary.get('to') or 0
                    salary_currency = salary.get('currency') or 'N/A'
                else:
                    salary_from = 0
                    salary_to = 0
                    salary_currency = 'N/A'

                employer = item.get('employer')
                if employer:
                    employer_name = employer.get('name', 'N/A')
                else:
                    employer_name = 'N/A'

                processed_data.append([
                    item.get('name', 'N/A'),
                    employer_name,
                    salary_from,
                    salary_to,
                    salary_currency,
                    item.get('published_at', 'N/A')
                ])
            return processed_data
        else:
            raise Exception(f"Ошибка при запросе к API hh.ru: {response.status_code}")
