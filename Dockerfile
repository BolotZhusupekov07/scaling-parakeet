FROM python:3.8-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
WORKDIR /django
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

RUN adduser -D myuser
USER myuser

# run gunicorn
CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT