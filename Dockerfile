FROM python:3.10

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.local.txt .
RUN pip install -r requirements.local.txt

COPY src/. /src/
COPY . .