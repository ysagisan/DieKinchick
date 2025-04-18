import requests

API_URL = "http://localhost:3298/film"  # адрес для запроса /films/<kinopoiskId>
SEARCH_URL = "http://localhost:3298/search" # адрес для запроса /search?title=<Название фильма>
RECOMMEND_URL = "http://localhost:3298/films/recommendations"

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

def get_recommended_films(limit=10):
    try:
        response = requests.get(RECOMMEND_URL, params={"limit": limit})
        if response.status_code == 200:
            return response.json().get("films", [])
        return []
    except Exception as e:
        print(f"Ошибка при получении рекомендованных фильмов: {e}")
        return []

def get_recommended_film_with_genre(limit=10, genre=None):
    try:
        params = {"limit": limit}
        if genre:
            params["genre"] = genre
        response = requests.get(RECOMMEND_URL, params=params)
        if response.status_code == 200:
            return response.json().get("films", [])
        return []
    except Exception as e:
        print(f"Ошибка при получении рекомендованных фильмов: {e}")
        return []
