from kinopoisk_api import get_info
from minio_uploader import upload_poster_from_url

# Получаем информацию о страницах с фильмами
first_page = get_info(1)
total_pages = first_page["totalPages"]

# Добавляем фиильмы в бакет
for page in range(1, 4):
    films = get_info(page)
    if not films:
        continue
    for film in films["items"]:
        name = film.get("nameRu") or film.get("nameEn") or f"film_{film['kinopoiskId']}"
        poster_url = film.get("posterUrl")
        if poster_url:
            upload_poster_from_url(poster_url, name)
