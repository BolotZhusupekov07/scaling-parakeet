FROM python:3.8-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

RUN adduser -D myuser
USER myuser

# run gunicorn
CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT