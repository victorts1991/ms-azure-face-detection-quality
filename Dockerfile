# Estágio 1: Builder
FROM python:3.11-slim as builder
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Estágio 2: Runtime
FROM python:3.11-slim
WORKDIR /app

# Copia as dependências do builder
COPY --from=builder /root/.local /root/.local
COPY . .

# Garante que o Python encontre os pacotes instalados no estágio anterior
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]