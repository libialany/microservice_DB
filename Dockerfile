FROM hub.upat.agetic.gob.bo/dockerhub-proxy/library/python:3.9 AS db

COPY requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt

RUN useradd -u 1000 -ms /bin/bash admin_db
USER admin_db

FROM db AS build

RUN mkdir -p /home/admin_db/app/
WORKDIR /home/admin_db/app/

COPY . /home/admin_db/app/

USER root
RUN chown -R admin_db:admin_db /home/admin_db/app/
USER admin_db

CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]
EXPOSE 5000
