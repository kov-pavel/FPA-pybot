# Создаем минималистичный образ Python.
FROM python:3.10-slim

# Устанавливаем необходимые зависимости.
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Определяем рабочую папку.
WORKDIR /code

# Копируем исходные коды бота.
COPY ./src ./src

# Запускаем бота.
CMD [ "python", "-u", "./src/main.py" ]