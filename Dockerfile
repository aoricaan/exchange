FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app

EXPOSE 80

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80"]