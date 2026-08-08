FROM python:3.13

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV HOST=0.0.0.0

CMD ["python", "app.py"]