# Reference HTTP adapter image (EP-003 SPR-003).
# Core + Flask only — no PySide6 / Studio (keeps the image small).
FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    BOARDCOMPOSER_MAX_UPLOAD_BYTES=5242880

WORKDIR /app

# Runtime deps for the HTTP adapter only.
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir "flask>=3,<4"

COPY src/boardcomposer /app/src/boardcomposer
COPY data/samples /app/data/samples

# Drop privileges; bind all interfaces inside the container.
RUN useradd --create-home --uid 10001 --shell /usr/sbin/nologin app \
 && chown -R app:app /app
USER app

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=3)"

CMD ["python", "-m", "boardcomposer.http_cli", "--host", "0.0.0.0", "--port", "8080"]
