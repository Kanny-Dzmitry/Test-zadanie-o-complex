# Веб-приложение прогноза погоды

Веб-приложение, которое позволяет пользователям получать прогноз погоды для указанного города на ближайшее время. Приложение предоставляет актуальные данные о температуре, осадках, влажности и скорости ветра, используя API сервиса Open-Meteo.

## Описание проекта

Приложение разработано с использованием фреймворка Django и предоставляет удобный интерфейс для получения прогноза погоды. Основные возможности:

- Поиск погоды по названию города с автодополнением
- Отображение текущих погодных условий и почасового прогноза на ближайшие сутки
- Сохранение истории поисков для каждого пользователя
- Предложение ранее просмотренных городов при повторном посещении сайта
- API для получения статистики по популярности городов

Приложение использует сессии для отслеживания пользователей даже без регистрации, что позволяет сохранять историю поисков и предлагать ранее просмотренные города.

## Принцип работы

1. Пользователь вводит название города в поисковую строку (с поддержкой автодополнения)
2. Приложение отправляет запрос к API Open-Meteo для получения координат города
3. Затем отправляется запрос для получения погодных данных по этим координатам
4. Результаты отображаются в удобном формате с текущими условиями и почасовым прогнозом
5. Информация о поиске сохраняется в базе данных для статистики и истории

## Реализованный функционал

✅ Вывод данных прогноза погоды в удобно читаемом формате  
✅ Автодополнение (подсказки) при вводе города  
✅ При повторном посещении сайта предлагается посмотреть погоду в городе, который пользователь уже смотрел ранее  
✅ Сохранение истории поиска для каждого пользователя  
✅ API, показывающее сколько раз вводили какой город  
✅ Размещение в Docker-контейнере  

## Использованные технологии

- **Backend**: Django 5.x
- **API погоды**: Open-Meteo API
- **Контейнеризация**: Docker и Docker Compose
- **Веб-сервер**: Gunicorn
- **Дополнительные библиотеки**: Requests
- **База данных**: SQLite (для простоты развертывания)

## Структура проекта

- `forecast` - основное приложение Django, содержащее модели, представления и шаблоны
- `weather_app` - основной проект Django
- `Dockerfile` и `docker-compose.yml` - файлы для контейнеризации приложения

## Примеры использования

### Поиск погоды

1. На главной странице введите название города (например, "Москва")
2. По мере ввода появятся подсказки с возможными вариантами
3. Выберите нужный город из списка или завершите ввод самостоятельно
4. Нажмите кнопку поиска или клавишу Enter
5. Получите актуальный прогноз погоды с текущими условиями и почасовым прогнозом

### Использование API

Получение статистики по популярности городов:
```
GET /stats/
```

Пример ответа:
```json
[
  {"city": "Москва", "count": 42},
  {"city": "Санкт-Петербург", "count": 28},
  {"city": "Новосибирск", "count": 15}
]
```

Автодополнение при вводе города:
```
GET /autocomplete/?term=Мос
```

Пример ответа:
```json
["Москва, Россия", "Московский, Россия", "Мосальск, Россия"]
```

## Установка и запуск приложения

### С использованием Docker (рекомендуется)

1. Убедитесь, что у вас установлены Docker и Docker Compose
2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Kanny-Dzmitry/Test-zadanie-o-complex.git
   cd weather-app
   ```
3. Запустите приложение с помощью Docker Compose:
   ```bash
   docker-compose up --build
   ```
4. Откройте браузер и перейдите по адресу: http://localhost:8001

Для запуска в фоновом режиме используйте:
```bash
docker-compose up -d
```

Для остановки контейнеров:
```bash
docker-compose down
```

### Без использования Docker

1. Убедитесь, что у вас установлен Python 3.11
2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/username/weather-app.git
   cd weather-app
   ```
3. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Linux/Mac
   venv\Scripts\activate  # для Windows
   ```
4. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
5. Выполните миграции:
   ```bash
   python manage.py migrate
   ```
6. Запустите сервер разработки:
   ```bash
   python manage.py runserver
   ```
7. Откройте браузер и перейдите по адресу: http://localhost:8001

## API

- `/stats/` - Получение статистики по поиску городов (топ-10 самых популярных городов)
- `/autocomplete/` - API для автодополнения при вводе названия города 