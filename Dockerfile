FROM jfloff/alpine-python:2.7-slim

WORKDIR /app

ADD . /app

RUN apk update

RUN apk add py-pip

RUN pip install -r requirements.txt

# Add app configuration to Nginx
COPY nginx.conf /etc/nginx/conf.d/

EXPOSE 80

# Copy sample app
COPY ./app /app

CMD ["python", "main.py"]
