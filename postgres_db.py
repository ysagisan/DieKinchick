import psycopg2
from kinopoisk_api import get_info

conn = psycopg2.connect(
    dbname="films",
    user="admin_film_db",
    password="diekinchic2025",
    host="localhost",
    port=5440
)

cur = conn.cursor()

def read_sql_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()

create_table_query = read_sql_from_file("queries.sql")
cur.execute(create_table_query)

def film_exists(kinopoiskId):
    check_table = """
    SELECT 1 FROM films_information WHERE kinopoiskId = %s;
    """
    cur.execute(check_table, (kinopoiskId,))
    return cur.fetchone() is not None

def insert_film(kinopoiskId, name, year, genre, rating, description):

    if film_exists(kinopoiskId):
        print(f"Фильм {kinopoiskId: name} уже существует в бд")
        return

    insert_query = """
    INSERT INTO films_information (kinopoiskId, name, year, genre, rating, description)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    try:
        cur.execute(insert_query, (kinopoiskId, name, year, genre, rating, description))
        conn.commit()
    except Exception as e:
        print(f"Ошибка при вставке фмильма: {e}")
        conn.rollback()

def parse_and_add_films(page_num):
    for page in range(1, page_num):
        films_data = get_info(page)

        for film in films_data["items"]:
            kinopoiskId = film.get("kinopoiskId")
            name = film.get("nameRu") or film.get("nameEn") or film.get("nameOriginal")
            year = film.get("year")
            rating = film.get("ratingKinopoisk") or film.get("ratingImdb")
            description = film.get("description")

            genres = film.get("genres")
            genre = ', '.join([g["genre"] for g in genres]) if genres else None

            insert_film(kinopoiskId, name, year, genre, rating, description)


parse_and_add_films(page_num=4)

cur.close()
conn.close()