FROM python:3.11-alpine
# 
WORKDIR /app
# 
COPY requirements.txt /app/requirements.txt
# 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
# 
COPY . .

WORKDIR /app/

CMD ["alembic", "upgrade", "head"]