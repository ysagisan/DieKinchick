from flask import Flask, jsonify
from minio import Minio
import psycopg2
import random
from flask import request

app = Flask(__name__)

# Соединение с PostgreSQL
conn = psycopg2.connect(
    dbname="films",
    user="admin_film_db",
    password="diekinchic2025",
    host="postgres",
    port=5432
)
cur = conn.cursor()

# Настройка MinIO клиента
minio_client = Minio(
    "minio:9000",
    access_key="ysagisan",
    secret_key="diekinchic2025",
    secure=False
)

# Функция для получения информации о фильме из БД
def get_film_info(kinopoisk_id):
    querie = """
        SELECT name, year, genre, rating, webUrl, description FROM films_information
        WHERE kinopoiskId = %s;
    """
    cur.execute(querie, (kinopoisk_id,))
    result = cur.fetchone()
    if result:
        return {
            "name": result[0],
            "year": result[1],
            "genre": result[2],
            "rating": result[3],
            "webUrl": result[4],
            "description": result[5]
        }
    return None

# Функция для получения постера фильма из MinIO
def get_film_poster(kinopoisk_id):
    try:
        # Преобразуем ID фильма в имя объекта (название файла)
        object_name = f"{kinopoisk_id}"
        # Проверим, существует ли объект в MinIO
        minio_client.stat_object("films-posters", object_name)
        # этот адрес получен с помощью cloudflared эта штука строит тунель от локального адреса в внешний мир так сказатб,
        # каждый раз после запуска нужно запускать cloudflared tunnel --url http://localhost:9000 и менять ссылку
        return f"https://classical-herbal-toilet-buddy.trycloudflare.com/films-posters/{object_name}"
    except Exception as e:
        print(f"Ошибка при получении постера: {e}")
        return None

def build_film_list(kinopoisk_ids):
    films = []
    for kinopoisk_id in kinopoisk_ids:
        film_info = get_film_info(kinopoisk_id)
        if film_info:
            poster_url = get_film_poster(kinopoisk_id)
            film = {
                "kinopoiskId": kinopoisk_id,
                "name": film_info["name"],
                "year": film_info["year"],
                "genre": film_info["genre"],
                "rating": film_info["rating"],
                "webUrl": film_info["webUrl"],
                "description": film_info["description"],
                "poster_url": poster_url
            }
            films.append(film)
    return films

def get_random_films(limit):
    cur.execute("SELECT kinopoiskId FROM films_information")
    film_ids = [row[0] for row in cur.fetchall()]
    random.shuffle(film_ids)
    selected = film_ids[:limit]

    return build_film_list(selected)

def get_films_by_genre(limit, genre):
    query = """
        SELECT kinopoiskId FROM films_information
        WHERE genre ILIKE %s
    """
    cur.execute(query, (f"%{genre}%",))
    film_ids = [row[0] for row in cur.fetchall()]
    random.shuffle(film_ids)
    selected = film_ids[:limit]
    return build_film_list(selected)

@app.route('/film/<int:kinopoisk_id>', methods=['GET']) # тут обрабатываем запрос на поиск фильма по id
def get_film_data(kinopoisk_id):
    # Получаем информацию о фильме из базы данных
    film_info = get_film_info(kinopoisk_id)
    if not film_info:
        return jsonify({"error": "Film not found"}), 404

    # Получаем постер фильма из MinIO
    poster_url = get_film_poster(kinopoisk_id)

    # Собираем всю информацию и отправляем её
    response = film_info
    if poster_url:
        response['poster_url'] = poster_url
    return jsonify(response)

@app.route('/search', methods=['GET']) # тут запрос на поиск фильма по названию
def search_film_by_title():
    title = request.args.get('title')
    print(title)
    if not title:
        return jsonify({"error": "No title provided"}), 400

    try:
        query = """
            SELECT kinopoiskId, name FROM films_information
            WHERE name ILIKE %s
            LIMIT 1;
        """
        cur.execute(query, (f"%{title}%",))
        result = cur.fetchone()

        if result:
            kinopoisk_id, name = result
            return jsonify({
                "kinopoisk_id": kinopoisk_id,
                "name": name
            })
        else:
            return jsonify({"error": "Film not found"}), 404

    except Exception as e:
        return jsonify({"error": f"Server error: {e}"}), 500

@app.get("/films/recommendations")
def get_recommendations():
    limit = int(request.args.get("limit", 10))
    genre = request.args.get("genre")

    if genre:
        films = get_films_by_genre(limit, genre)
    else:
        films = get_random_films(limit)
    return {"films": films}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3298)
