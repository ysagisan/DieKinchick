import os
import psycopg2
from kinopoisk_api.kinopoisk_api import get_info
from minio_posters.minio_uploader import upload_poster_from_url

conn = psycopg2.connect(
    dbname="films",
    user="admin_film_db",
    password="diekinchic2025",
    host="localhost",
    port=5440
)

cur = conn.cursor()

def read_sql_from_file(filename):
    base_path = os.path.dirname(__file__)  # путь к папке, где лежит postgres_db.py
    file_path = os.path.join(base_path, filename)
    with open(file_path, 'r') as file:
        return file.read()

create_table_query = read_sql_from_file("queries.sql")
cur.execute(create_table_query)

def film_exists(kinopoiskId):
    check_table = """
    SELECT 1 FROM films_information WHERE kinopoiskId = %s;
    """
    cur.execute(check_table, (kinopoiskId,))
    return cur.fetchone() is not None

def insert_film(kinopoiskId, name, year, genre, rating, webUrl, description):
    if film_exists(kinopoiskId):
        print(f"\033[33mPOSTGRES:\033[0m Фильм {kinopoiskId}: {name} уже существует в бд")
        return

    insert_query = """
    INSERT INTO films_information (kinopoiskId, name, year, genre, rating, webUrl, description)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    print(f"\033[32mPOSTGRES:\033[0m Фильм {kinopoiskId}: {name} успешно загружен!")

    try:
        cur.execute(insert_query, (kinopoiskId, name, year, genre, rating, webUrl, description))
        conn.commit()
    except Exception as e:
        print(f"\033[31mPOSTGRES:\033[0m Ошибка при вставке фмильма: {e}")
        conn.rollback()

def parse_and_add_films(page_num):
    for page in range(1, page_num+1):
        films_data = get_info(page)
        for film in films_data["items"]:
            kinopoiskId = film.get("kinopoiskId")
            name = film.get("nameRu") or film.get("nameEn") or film.get("nameOriginal")
            year = film.get("year")
            rating = film.get("ratingKinopoisk") or film.get("ratingImdb")
            description = film.get("description")
            webUrl = f"https://www.kinopoisk.ru/film/{kinopoiskId}"
            genres = film.get("genres")
            genre = ', '.join([g["genre"] for g in genres]) if genres else None

            insert_film(kinopoiskId, name, year, genre, rating, webUrl, description)

            poster_url = film.get("posterUrlPreview") or film.get("posterUrl")
            if poster_url:
                upload_poster_from_url(poster_url, f"{kinopoiskId}")

if __name__ == "__main__":
    parse_and_add_films(page_num=2)
    cur.close()
    conn.close()
