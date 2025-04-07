from flask import Flask, jsonify
from minio import Minio
import psycopg2

app = Flask(__name__)

# Соединение с PostgreSQL
conn = psycopg2.connect(
    dbname="films",
    user="admin_film_db",
    password="diekinchic2025",
    host="localhost",
    port=5440
)
cur = conn.cursor()

# Настройка MinIO клиента
minio_client = Minio(
    "localhost:9000",
    access_key="ysagisan",
    secret_key="diekinchic2025",
    secure=False
)

# Функция для получения информации о фильме из БД
def get_film_info(kinopoisk_id):
    querie = """
        SELECT name, year, genre, rating, description FROM films_information
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
            "description": result[4]
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
        return f"https://reporters-watch-gold-tags.trycloudflare.com/films-posters/{object_name}"
    except Exception as e:
        print(f"Ошибка при получении постера: {e}")
        return None

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

from flask import request

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3298)
