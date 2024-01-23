FROM python:3.11
WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "app:app", "-c", "/app/gunicorn_config.py"]