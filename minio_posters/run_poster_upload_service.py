from kinopoisk_api.kinopoisk_api import get_info
from minio_posters.minio_uploader import upload_poster_from_url

# Получаем информацию о страницах с фильмами
first_page = get_info(1)
total_pages = first_page["totalPages"]

# Добавляем фиильмы в бакет
for page in range(1, 10):
    films = get_info(page)
    if not films:
        continue
    for film in films["items"]:
        id = film.get("kinopoiskId")
        poster_url = film.get("posterUrl")
        if poster_url:
            upload_poster_from_url(poster_url, str(id))
