FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV PORT 8000
WORKDIR /dumblestore
COPY requirements.txt .
RUN apt-get update && apt-get install build-essential -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py migrate