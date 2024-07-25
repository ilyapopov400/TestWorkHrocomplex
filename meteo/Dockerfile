FROM python:3.10

SHELL ["/bin/bash", "-c"]

# set environment variables
# создание переменных
ENV PYTHONDONTWRITEBYTECODE 1  # запрет создавать в контейнере файлы с кэшом
ENV PYTHONUNBUFFERED 1  # запрет буферизации stdout, stderr

RUN pip install --upgrade pip

RUN apt update

# создана рабочая директория в контейнере
WORKDIR /web

# созданы директории
RUN mkdir /web/static && mkdir /web/media

# копируем все из текущей директории из компьютера в текущую (мы перешли в "/web") директорию контейнера
COPY . .

# установили зависимости
RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]

