FROM python:3.10-slim

ENV PYTHONBUFFERED  True
ENV APP_HOME /app
WORKDIR $APP_HOME

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./

CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT
