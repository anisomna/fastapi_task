FROM python:latest

WORKDIR /fastapi_app

ENV PYTHONPATH=/fastapi_app/src

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt


RUN mkdir -p /fastapi_app/images /fastapi_app/comment_images /fastapi_app/avatars && chmod 777 /fastapi_app/images /fastapi_app/comment_images /fastapi_app/avatars

COPY . .

EXPOSE 8000

CMD ["./start.sh"]
