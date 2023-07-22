FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -U pip && pip install -r requirements.txt

RUN pip install gunicorn

COPY [ "predict.py", "models/lin_reg.bin", "./" ]

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict:app" ]