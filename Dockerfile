FROM python:3.10

WORKDIR /home/python/app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .
RUN mkdir static
EXPOSE 8000
RUN

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]

