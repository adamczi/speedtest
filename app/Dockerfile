# get the base image
FROM jfloff/alpine-python:2.7-slim

# things to create working dir
WORKDIR /app
ADD . /app

# things to install binaries and dependencies
RUN apk update
RUN apk add py-pip
RUN pip install -r requirements.txt

# Add app configuration to Nginx
COPY nginx.conf /etc/nginx/conf.d/

# expose port
EXPOSE 80

# Copy sample app
COPY ./app /app

CMD python, main.py
