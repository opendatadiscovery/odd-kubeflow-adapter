FROM python:3.9.1-buster AS reqs

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt


FROM python:3.9.1-slim-buster

COPY ./server /srv/app
COPY --from=reqs /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=reqs /usr/local/bin/gunicorn /usr/local/bin/gunicorn

ENV PYTHONUNBUFFERED=1
ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8080
WORKDIR /srv/app/

ENTRYPOINT gunicorn --bind 0.0.0.0:8080 --timeout=300 --workers=10 wsgi:application