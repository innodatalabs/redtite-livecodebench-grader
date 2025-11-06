FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.12-slim

WORKDIR /app

# Copy only the installed packages and application code from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn
COPY server.py runner.py ./

EXPOSE 8000
ENV PYTHONPATH=.:/app/LiveCodeBench

CMD [ "gunicorn",  \
    "-w", "5", \
    "--bind", "0.0.0.0:80", \
    "--timeout", "300", \
    "--worker-class", "aiohttp.GunicornWebWorker", \
    "server:app" \
]
