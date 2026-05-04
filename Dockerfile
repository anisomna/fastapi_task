FROM python:latest

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN mkdir -p /fastapi_app/images && chmod 777 /fastapi_app/images

COPY . .

EXPOSE 8000

CMD ["./start.sh"]
