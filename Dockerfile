FROM python:3.9-slim
WORKDIR /auth-service
COPY . /auth-service
RUN apt-get update
RUN apt-get install -y sqlite3
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -f -r migrations
RUN rm -f -r instance
RUN flask db init
RUN flask db migrate
RUN flask db upgrade
EXPOSE 3000
CMD ["python", "app.py"]

