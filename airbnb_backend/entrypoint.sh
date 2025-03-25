#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Check if database is running..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "The database is up and running :-D"
fi

echo "Створення міграцій для всіх додатків..."
python manage.py makemigrations useraccount
python manage.py makemigrations property
python manage.py makemigrations chat

echo "Застосування міграцій у правильному порядку..."
python manage.py migrate useraccount
python manage.py migrate property
python manage.py migrate chat
python manage.py migrate --fake-initial

# python manage.py makemigrations
# python manage.py migrate

"$@" & 
wait 