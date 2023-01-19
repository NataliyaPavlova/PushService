FROM python:3.10.4

ENV APP_HOME=/app

RUN mkdir -p $APP_HOME \
    && groupadd -r app \
    && useradd -d $APP_HOME -r -g app app \
    && chown app:app -R $APP_HOME

WORKDIR $APP_HOME

COPY ./worker/requirements.txt $APP_HOME/

RUN pip install --upgrade --no-cache-dir pip wheel setuptools \
    && pip install --no-cache-dir --upgrade -r requirements.txt

USER app:app

COPY ./core $APP_HOME
COPY ./worker $APP_HOME
COPY ./run_worker.py $APP_HOME

WORKDIR $APP_HOME/
