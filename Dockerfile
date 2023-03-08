FROM python:3.11

RUN mkdir /app

COPY /src/requirements.txt /opt/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /opt/requirements.txt

COPY /src /app

WORKDIR /app

CMD python runner.py