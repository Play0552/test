FROM python:3.12

WORKDIR /app/

RUN apt update && apt upgrade -y

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "PYTHONPATH=. alembic upgrade head && python3 main.py"]
