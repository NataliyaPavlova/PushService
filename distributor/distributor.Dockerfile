FROM python:3.10.4

ENV APP_HOME=/app

RUN mkdir -p $APP_HOME \
    && groupadd -r app \
    && useradd -d $APP_HOME -r -g app app \
    && chown app:app -R $APP_HOME

WORKDIR $APP_HOME

RUN mkdir -p $APP_HOME/distributor
COPY distributor/requirements.txt $APP_HOME/distributor/

RUN pip install --upgrade --no-cache-dir pip wheel setuptools \
    && pip install --no-cache-dir --upgrade -r distributor/requirements.txt

USER app:app

COPY ./core $APP_HOME/core
COPY ./distributor $APP_HOME/distributor

WORKDIR $APP_HOME/
