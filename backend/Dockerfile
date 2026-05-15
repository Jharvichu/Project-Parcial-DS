FROM python:3.12-slim

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./app /app/app

# Ensure uploads directory exists (mounted by docker-compose for persistence)
RUN mkdir -p /app/uploads/photos /app/uploads/videos

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
