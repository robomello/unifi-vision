FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir flask psycopg2-binary

COPY server.py pricing.py index.html /app/

EXPOSE 8080

CMD ["python3", "server.py"]
