FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

COPY . /app

RUN set -eux; \
    for i in 1 2 3 4 5; do \
      pip install --no-cache-dir --retries 10 --timeout 120 fastapi uvicorn[standard] && break; \
      if [ "$i" -eq 5 ]; then exit 1; fi; \
      sleep 5; \
    done

EXPOSE 8080

CMD ["uvicorn", "deploy.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
