# 🚀 Guia de Deploy - Dashboard Financeiro

Este guia explica como fazer o deploy do Dashboard Financeiro em diferentes plataformas.

## 📋 Pré-requisitos

1. **Conta Google Cloud** com Google Sheets API ativada
2. **Credenciais configuradas** seguindo `GOOGLE_SHEETS_SETUP.md`
3. **Planilha do Google Sheets** criada e compartilhada

## 🌐 Deploy no Streamlit Cloud (Recomendado)

### 1. Preparar o Repositório
```bash
# Certifique-se de que todos os arquivos estão commitados
git add .
git commit -m "Preparando para deploy"
git push origin main
```

### 2. Configurar no Streamlit Cloud
1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Conecte sua conta GitHub
3. Selecione o repositório `dashboard-financeiro`
4. Configure o arquivo principal: `app.py`

### 3. Configurar Variáveis de Ambiente
No Streamlit Cloud, adicione as seguintes variáveis:

```bash
GOOGLE_SPREADSHEET_ID=seu-spreadsheet-id
GOOGLE_SHEET_NAME=Adriano
USE_GOOGLE_SHEETS=true
```

### 4. Configurar Credenciais
1. Crie um arquivo `google-credentials.json` com suas credenciais
2. No Streamlit Cloud, vá em "Advanced settings"
3. Adicione o conteúdo do arquivo como variável `GOOGLE_CREDENTIALS_JSON`

### 5. Deploy
Clique em "Deploy" e aguarde a conclusão.

## 🐳 Deploy com Docker

### 1. Criar Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Expor porta
EXPOSE 8501

# Comando para executar
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. Build e Executar
```bash
# Build da imagem
docker build -t dashboard-financeiro .

# Executar container
docker run -p 8501:8501 \
  -e GOOGLE_SPREADSHEET_ID=seu-spreadsheet-id \
  -e GOOGLE_SHEET_NAME=Adriano \
  -e USE_GOOGLE_SHEETS=true \
  dashboard-financeiro
```

## ☁️ Deploy no Heroku

### 1. Criar Procfile
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### 2. Configurar Buildpacks
```bash
heroku buildpacks:set heroku/python
```

### 3. Configurar Variáveis
```bash
heroku config:set GOOGLE_SPREADSHEET_ID=seu-spreadsheet-id
heroku config:set GOOGLE_SHEET_NAME=Adriano
heroku config:set USE_GOOGLE_SHEETS=true
```

### 4. Deploy
```bash
git push heroku main
```

## 🔧 Deploy Local (Produção)

### 1. Usando Gunicorn
```bash
# Instalar gunicorn
pip install gunicorn

# Executar
gunicorn -w 4 -b 0.0.0.0:8501 streamlit.web.cli:main -- app.py
```

### 2. Usando Nginx (Reverso Proxy)
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 Configurações de Segurança

### 1. Variáveis de Ambiente
Nunca commite credenciais no repositório:
```bash
# ❌ NUNCA faça isso
GOOGLE_SPREADSHEET_ID=1234567890

# ✅ Use variáveis de ambiente
export GOOGLE_SPREADSHEET_ID=1234567890
```

### 2. HTTPS
Configure HTTPS em produção:
```bash
# Streamlit Cloud já fornece HTTPS
# Para outros deploys, configure certificados SSL
```

### 3. Firewall
Configure firewall para permitir apenas tráfego necessário:
```bash
# Permitir apenas porta 8501
ufw allow 8501
```

## 📊 Monitoramento

### 1. Logs
Configure logs para monitoramento:
```bash
# Logs do Streamlit
streamlit run app.py --logger.level=info

# Logs do sistema
journalctl -u dashboard-financeiro -f
```

### 2. Métricas
Monitore:
- Uptime da aplicação
- Tempo de resposta
- Uso de memória/CPU
- Erros de aplicação

## 🚨 Troubleshooting

### Problema: Erro de credenciais
```bash
# Verificar se as credenciais estão corretas
python -c "from utils.google_sheets import test_connection; test_connection()"
```

### Problema: Planilha não encontrada
```bash
# Verificar se a planilha está compartilhada
# Verificar se o ID está correto
```

### Problema: Porta em uso
```bash
# Verificar portas em uso
lsof -i :8501

# Matar processo se necessário
kill -9 PID
```

## 📞 Suporte

Para problemas de deploy:
1. Verifique os logs da aplicação
2. Confirme as configurações de ambiente
3. Teste localmente primeiro
4. Abra uma issue no GitHub

## 🔄 Atualizações

Para atualizar o deploy:
1. Faça as mudanças no código
2. Commit e push para o repositório
3. O deploy automático atualizará a aplicação
4. Verifique se tudo está funcionando 