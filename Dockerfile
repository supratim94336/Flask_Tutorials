# the image we need to build the container for linux
FROM python:3.6-alpine
# command in container image, adds an user inside the docker image
RUN adduser -D microblog
# current directory for the docker file
WORKDIR /home/microblog
# copying the file inside the docker container
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./
RUN chmod a+x boot.sh
# creates environment variable inside container
ENV FLASK_APP microblog.py
# changes ownership of the microblog user
RUN chown -R microblog:microblog ./
# describing the port number where the app will run
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]