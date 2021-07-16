FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD gunicorn core.wsgi:application — bind 0.0.0.0:$PORT

