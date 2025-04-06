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

def film_exists(name):
    check_table = """
    SELECT 1 FROM films_information WHERE name = %s;
    """
    cur.execute(check_table, (name,))
    return cur.fetchone() is not None

def insert_film(name, year, genre, rating, description):

    if film_exists(name):
        print(f"Фильм {name} уже существует в бд")
        return

    insert_query = """
    INSERT INTO films_information (name, year, genre, rating, description)
    VALUES (%s, %s, %s, %s, %s);
    """
    try:
        cur.execute(insert_query, (name, year, genre, rating, description))
        conn.commit()
    except Exception as e:
        print(f"Ошибка при вставке фмильма: {e}")
        conn.rollback()

def parse_and_add_films(page_num):
    for page in range(1, page_num):
        films_data = get_info(page)

        for film in films_data["items"]:
            name = film.get("nameRu") or film.get("nameEn")
            year = film.get("year")
            rating = film.get("ratingKinopoisk")
            description = film.get("description")

            genres = film.get("genres")
            genre = ', '.join([g["genre"] for g in genres]) if genres else None

            insert_film(name, year, genre, rating, description)


parse_and_add_films(page_num=5)

cur.close()
conn.close()