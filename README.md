# transfer-api-test

Переименовываем в папке docker, и во вложенных в ней, файлы .exv-example в .env

В папке докера:
sudo docker-compose build
sudo docker-compose up -d

sudo docker-compose exec django bash
cd website
python manage.py createsuperuser

Заходим в админку http://0.0.0.0:8000/admin/
Создайте для тестов несколько валют в Currency

Можно тетстировать апи по адресу http://0.0.0.0:8000/api/register/