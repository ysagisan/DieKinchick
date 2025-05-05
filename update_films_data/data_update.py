from postgres_db.postgres_db import parse_and_add_films
from datetime import datetime

if __name__ == "__main__":
    print(f"[{datetime.now()}] Запуск задачи обновления фильмов")
    parse_and_add_films(page_num=20)
    print("Обновление завершено!")

