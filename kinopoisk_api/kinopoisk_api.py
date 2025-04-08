import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

headers = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

params = {
    "type": "TOP_POPULAR_ALL",
    "page": 1
}

# Эта функция возвращает json с информацией о подборке фильмов
def get_info(page_num: int):
    params["page"] = page_num
    url = "https://kinopoiskapiunofficial.tech/api/v2.2/films/collections"
    response = requests.get(url, headers=headers, params=params)
    return response.json()
