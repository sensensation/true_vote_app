FROM python:3.11-slim

COPY ./requirements*.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

ADD ./src /app/code
COPY entrypoint.sh /app/entrypoint.sh
WORKDIR /app/code
RUN chmod +x /app/entrypoint.sh