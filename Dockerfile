FROM python:3.11-slim



WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 600 -i https://pypi.org/simple -r requirements.txt



COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
