# api_yamdb
api_yamdb

# API для api_yamdb

## Описание

API для социальной сети Yatube.

### В данном проекте можно:
* Создавать, просматривать, удалять и изменять посты.
* Добавлять посты в группы.
* Создавать, удалять, смотреть и изменять комментарии к записям.
* Подписываться на авторов и смотреть подписки.

#### Документация по адресу:
```
http://localhost:8000/redoc/
```

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/1emd/api_final_yatube.git 
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
Для Mac: source venv/bin/activate
```

```
Для Win(cmd.exe): venv\Scripts\activate.bat
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры запросов
- POST: api/v1/posts/  
Request samples 
```json
{
"text": "string",
"image": "string",
"group": 0
} 
```
Response samples
```json
{
"id": 0,
"author": "string",
"text": "string",
"pub_date": "2019-08-24T14:15:22Z",
"image": "string",
"group": 0
}
```
- PUT: api/v1/posts/{id}/
Request samples 
```json
{
"text": "string",
"image": "string",
"group": 0
}
```
Response samples
```json
{
"id": 0,
"author": "string",
"text": "string",
"pub_date": "2019-08-24T14:15:22Z",
"image": "string",
"group": 0
}
```
- POST: api/v1/posts/{post_id}/comments/
Request samples
```json
{
"text": "string"
}
```
Response samples
```json
{
"id": 0,
"author": "string",
"text": "string",
"created": "2019-08-24T14:15:22Z",
"post": 0
}
```
- POST: api/v1/follow/
Request samples 
```json
{
"following": "string"
}
```
Response samples
```json
{
"user": "string",
"following": "string"
}
```

### Основные использованные технологии
- Python 3.9
- Django 3.2.16
- Djangorestframework 3.12.4
- Djangorestframework-simplejwt 4.7.2