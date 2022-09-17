# Базовый образ Python.
FROM python:3.10 AS builder
COPY requirements.txt .

# Устанавливаем зависимости в директорию локального пользователя (т.е. /root/.local)/
RUN pip install --user -r requirements.txt

# Создаем минималистичный образ Python.
FROM python:3.10-slim
WORKDIR /code

# Копируем только те зависимости, которые нужны для нашего приложения и исходные коды.
COPY --from=builder /root/.local /root/.local
COPY ./src ./src

# Обновляем PATH.
ENV PATH=/root/.local:$PATH

# Запускаем бота.
CMD [ "python", "-u", "./src/main.py" ]