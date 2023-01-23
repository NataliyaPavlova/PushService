FROM python:3.10.4

ENV APP_HOME=/app
ENV PYTHONPATH=/app/src

RUN mkdir -p $APP_HOME \
    && groupadd -r app \
    && useradd -d $APP_HOME -r -g app app \
    && chown app:app -R $APP_HOME

WORKDIR $APP_HOME

RUN mkdir -p $APP_HOME/worker
COPY worker/requirements.txt $APP_HOME/worker/

RUN pip install --upgrade --no-cache-dir pip wheel setuptools \
    && pip install --no-cache-dir --upgrade -r worker/requirements.txt

USER app:app

COPY ./core $APP_HOME/core
COPY ./worker $APP_HOME/worker

WORKDIR $APP_HOME/
CMD ["python", "worker/main.py"]
