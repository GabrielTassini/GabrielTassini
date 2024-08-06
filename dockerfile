FROM python:3.11-slim

EXPOSE 8000
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["uvicorn", "gabriel:app", "--host", "0.0.0.0", "--port", "8000"]

# docker build -t gabriel-img .
# docker tag gabriel-img simonaggio.azurecr.io/gabriel-img
# docker run -it -p 8000:8080 gabriel-img
# docker push simonaggio.azurecr.io/gabriel-img 
# docker login -u simonaggio -p U6m4OUkc8Q8PgJDkADgQX2byphXf1J4AF/wsLj144P+ACRBJ0qpa simonaggio.azurecr.io