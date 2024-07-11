FROM python:3.12

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "api.py", "--host=0.0.0.0", "--port=5000"]