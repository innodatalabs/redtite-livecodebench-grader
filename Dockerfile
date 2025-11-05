FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM alpine/git AS git

WORKDIR /app

RUN git clone https://github.com/LiveCodeBench/LiveCodeBench.git && git checkout 28fef95ea8c9f7a547c8329f2cd3d32b92c1fa24

FROM python:3.12-slim

WORKDIR /app

# Copy only the installed packages and application code from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn
COPY --from=git /app/LiveCodeBench /app/LiveCodeBench
COPY server.py .

EXPOSE 8000
ENV PYTHONPATH=.:/app/LiveCodeBench

CMD [ "gunicorn",  \
    "-w", "5", \
    "--bind", "0.0.0.0:8000", \
    "--timeout", "300", \
    "--worker-class", "aiohttp.GunicornWebWorker", \
    "server:app" \
]
