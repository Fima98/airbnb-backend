FROM python:3.13.0a4-slim

WORKDIR /usr/src/airbnb_backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/airbnb_backend/entrypoint.sh
RUN chmod +x /usr/src/airbnb_backend/entrypoint.sh

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
# ENTRYPOINT ["/usr/src/airbnb_backend/entrypoint.sh"]

