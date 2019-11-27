FROM python:3.6-slim-stretch
RUN apt-get update && apt-get install build-essential libpq-dev libsasl2-dev python-dev libldap2-dev libssl-dev -y
RUN pip install --upgrade pip setuptools
ENV FLASK_APP=/opt/app
COPY app/ /opt/app
WORKDIR /opt
RUN python app/setup.py install
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
