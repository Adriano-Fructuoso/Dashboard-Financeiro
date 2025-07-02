# 🚀 Configuração do Streamlit Cloud

## 📋 Pré-requisitos

1. ✅ Conta no Streamlit Cloud (gratuita)
2. ✅ Repositório no GitHub com o código
3. ✅ Projeto Supabase configurado
4. ✅ Banco de dados populado com dados

## 🔧 Passo a Passo

### 1. Acessar Streamlit Cloud

1. Vá para [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta GitHub
3. Clique em "New app"

### 2. Configurar o App

- **Repository**: `Adriano-Fructuoso/Dashboard-Financeiro`
- **Branch**: `main`
- **Main file path**: `app.py`
- **App URL**: deixe o padrão ou escolha um nome personalizado

### 3. Configurar Secrets (CRÍTICO)

Antes de fazer deploy, configure os secrets:

1. No painel do Streamlit Cloud, vá em **Settings** → **Secrets**
2. Adicione o seguinte JSON:

```json
{
  "SUPABASE": {
    "SUPABASE_URL": "https://kcyerufpbzmtfohyfyrq.supabase.co",
    "SUPABASE_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtjeWVydWZwenN0Zm9oeWZ5cnEiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTczNTQ5NzE5NywiZXhwIjoyMDUxMDczMTk3fQ.Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8",
    "SUPABASE_SERVICE_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtjeWVydWZwenN0Zm9oeWZ5cnEiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNzM1NDk3MTk3LCJleHAiOjIwNTEwNzMxOTd9.Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8"
  }
}
```

**⚠️ IMPORTANTE**: Substitua as chaves pelas suas reais do Supabase!

### 4. Fazer Deploy

1. Clique em **Deploy**
2. Aguarde o build (pode demorar alguns minutos)
3. O app estará disponível em: `https://seu-app.streamlit.app`

### 5. Testar o App

1. Acesse a URL do app
2. Faça login com:
   - **Usuário**: `adriano`
   - **Senha**: `senha123`
3. Verifique se os dados estão carregando

## 🔍 Troubleshooting

### Erro: "Banco de dados não configurado"

**Causa**: Secrets não configurados corretamente

**Solução**:
1. Verifique se os secrets estão no formato correto
2. Confirme se as chaves do Supabase estão corretas
3. Aguarde alguns minutos após salvar os secrets

### Erro: "Módulo não encontrado"

**Causa**: Dependências não instaladas

**Solução**:
1. Verifique se o `requirements.txt` está atualizado
2. O Streamlit Cloud instala automaticamente as dependências

### Erro: "Conexão recusada"

**Causa**: Configurações do Supabase incorretas

**Solução**:
1. Verifique se a URL do Supabase está correta
2. Confirme se a chave anônima está correta
3. Teste a conexão localmente primeiro

## 📊 Verificação Final

Após o deploy, você deve ver:

1. ✅ Tela de login funcionando
2. ✅ Login com usuário `adriano` e senha `senha123`
3. ✅ Dashboard carregando com dados
4. ✅ Gráficos e análises funcionando
5. ✅ Funcionalidade de adicionar transações

## 🆘 Suporte

Se ainda houver problemas:

1. Verifique os logs no Streamlit Cloud
2. Teste localmente com `streamlit run app.py`
3. Execute o script `test_config.py` para verificar configurações
4. Verifique se o banco Supabase está acessível

## 🎯 Próximos Passos

Após o deploy bem-sucedido:

1. **Personalizar**: Adicione mais usuários e dados
2. **Melhorar**: Implemente novas funcionalidades
3. **Monitorar**: Acompanhe o uso e performance
4. **Expandir**: Considere funcionalidades premium 