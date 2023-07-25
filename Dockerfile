
FROM python:3.10

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .

EXPOSE 33060
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "33060"]
