# Usar Ubuntu 24.04 como base
FROM ubuntu:24.04

# Evitar prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Definir o diretório de trabalho
WORKDIR /app

# Instalar Python, pip e venv
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Criar um ambiente virtual
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar os arquivos de requisitos
COPY requeriments_updated.txt .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requeriments_updated.txt

# Copiar o restante do código do backend
COPY . .

# Expor a porta que o Django usa
EXPOSE 8000

# Comando para rodar as migrações e iniciar o servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
