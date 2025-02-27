# LiveStremingBackend



## Clone este repositório
```git clone https://github.com/PedroProgramming/LiveStreamingBackend.git```
## Entrar no diretório
```cd LiveStreamingBackend```
## Crie um ambiente virtual
```python3 -m venv venv```
## Ative o ambiente virtual
```source venv/bin/activate```
## Instale as dependências
```pip install -r requirements.txt```


# Criar .env na raiz do projeto
```bash
# Chave secreta do Django para criptografia
SECRET_KEY=django-insecure-!y1kz02b@x&ob8e&o4y8h+$pk#^mb_v@kp1(swej6ti0nm_1!0

# Configuração de ambiente do Django (ex: desenvolvimento ou produção)
DJANGO_CONFIG_MODULE=config.development

# Hosts permitidos para acessar o site
ALLOWED_HOSTS=localhost,127.0.0.1,example.com,localhost:5173,127.0.0.1:5500

# Permite CORS para esses domínios
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5500

# Chave secreta para assinatura de tokens JWT
SIGNING_KEY=c0a7e647e4777bc0384e5f9c4264a7e1e7d7902b4e6e2f0e29cfb67d58ff9cb0

# Algoritmo usado para assinar tokens JWT
ALGORITHM=HS256

# Configuração do banco PostgreSQL
ENGINE=django.db.backends.postgresql
NAME=Teste
USER=Teste
PASSWORD=Teste
HOST=Teste
PORT=5432

# Configuração de Cache
REDIS_URL=redis://127.0.0.1:6379/0

# Configuração de Redis Celery
REDIS_CELERY_URL=REDIS://127.0.0.1:6379/1
```

# Rodando o Projeto

## Fazer migrações
```python manage.py migrate```

## Criar superusuário
```python manage.py createsuperuser```

## Iniciar servidor
```python manage.py runserver```