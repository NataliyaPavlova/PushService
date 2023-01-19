FROM python:3.10.4

ENV APP_HOME=/app
ENV PYTHONPATH=/app/src

RUN mkdir -p $APP_HOME \
    && groupadd -r app \
    && useradd -d $APP_HOME -r -g app app \
    && chown app:app -R $APP_HOME

WORKDIR $APP_HOME

RUN mkdir -p $APP_HOME/admin_api
COPY ./admin_api/requirements.txt $APP_HOME/admin_api/

RUN pip install --upgrade --no-cache-dir pip wheel setuptools \
    && pip install --no-cache-dir --upgrade -r admin_api/requirements.txt

USER app:app

COPY ./core $APP_HOME/core
COPY ./admin_api $APP_HOME/admin_api

WORKDIR $APP_HOME
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8888", "--log-level",  "debug", "admin_api.src.main:app"]
