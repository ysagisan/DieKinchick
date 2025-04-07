import requests

API_URL = "http://localhost:3298/film"  # адрес для запроса /films/<kinopoiskId>
SEARCH_URL = "http://localhost:3298/search" # адрес для запроса /search?title=<Название фильма>

def get_film_data(kinopoisk_id):
    try:
        response = requests.get(f"{API_URL}/{kinopoisk_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Ошибка при запросе данных с API Gateway: {e}")
        return None

def get_kinopoisk_id_by_title(title):
    try:
        response = requests.get(f"{SEARCH_URL}", params={"title": title})
        if response.status_code == 200:
            return response.json().get("kinopoisk_id")
        return None
    except Exception as e:
        print(f"Ошибка при поиске ID по названию: {e}")
        return None
