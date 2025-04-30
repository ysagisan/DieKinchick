from minio import Minio, S3Error
from io import BytesIO
import requests

client = Minio(
    "127.0.0.1:9000",
    access_key="ysagisan",
    secret_key="diekinchic2025",
    secure=False
)

# Эта функция проверяет есть ли уже файл с названием object_name в bucket_name
def object_exists(client, bucket_name: str, object_name: str) -> bool:
    try:
        client.stat_object(bucket_name, object_name)
        return True
    except S3Error as err:
        if err.code in ["NoSuchKey", "NoSuchObject", "NoSuchBucket"]:
            return False
        raise

# Эта функция загружает постер poster_url в бакет bucket_name
def upload_poster_from_url(poster_url: str, object_name: str, bucket_name="films-posters"):

    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    if object_exists(client, bucket_name, object_name):
        print(f"\033[33mMINIO:\033[0m Файл  <{object_name}> уже существует, пропускаем.")
        return

    response = requests.get(poster_url)
    if response.status_code != 200:
        raise Exception(f"\033[31mMINIO:\033[0m Не удалось скачать постер: {poster_url}")

    data = BytesIO(response.content)
    client.put_object(
        bucket_name,
        object_name,
        data,
        length=len(response.content),
        content_type="image/jpeg"
    )
    print(f"\033[32mMINIO:\033[0m Постер <{object_name}> успешно загружен!")

