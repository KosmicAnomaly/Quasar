FROM python:3.10.2-slim-buster
RUN apt-get update && apt-get -y upgrade
RUN pip install --upgrade pip
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
