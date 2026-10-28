FROM python:3.13-slim

WORKDIR /app

COPY docker.requirements .

RUN pip install --no-cache-dir -r docker.requirements

COPY . .

EXPOSE 8000
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]