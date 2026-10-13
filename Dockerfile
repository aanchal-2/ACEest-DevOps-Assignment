FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ACEEST_DB_PATH=/app/instance/aceest.db
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && useradd --create-home appuser \
 && mkdir -p /app/instance \
 && chown -R appuser:appuser /app
COPY app.py storage.py ./
COPY templates/ ./templates/
COPY tests/ ./tests/
USER appuser
EXPOSE 5000
CMD ["python", "app.py"]
