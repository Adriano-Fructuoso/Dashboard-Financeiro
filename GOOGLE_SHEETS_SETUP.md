# 🔧 Configuração do Google Sheets

Este guia te ajudará a configurar o Google Sheets como banco de dados para o Dashboard Financeiro.

## 📋 Pré-requisitos

1. Conta Google
2. Python 3.7+
3. Dependências instaladas (`pip install -r requirements.txt`)

## 🚀 Passo a Passo

### 1. Criar uma Planilha no Google Sheets

1. Acesse [Google Sheets](https://sheets.google.com)
2. Crie uma nova planilha
3. Renomeie a primeira aba para `Lancamentos`
4. Adicione os cabeçalhos na primeira linha:
   ```
   Data | Descrição | Categoria | Tipo | Valor
   ```
5. Copie o ID da planilha da URL:
   ```
   https://docs.google.com/spreadsheets/d/SEU_ID_AQUI/edit
   ```

### 2. Configurar Google Cloud Console

1. Acesse [Google Cloud Console](https://console.cloud.google.com)
2. Crie um novo projeto ou selecione um existente
3. Habilite a **Google Sheets API**:
   - Vá em "APIs e serviços" > "Biblioteca"
   - Procure por "Google Sheets API"
   - Clique em "Ativar"

### 3. Criar Credenciais

1. Vá em "APIs e serviços" > "Credenciais"
2. Clique em "Criar credenciais" > "Conta de serviço"
3. Preencha:
   - **Nome**: `dashboard-financeiro`
   - **Descrição**: `Conta de serviço para Dashboard Financeiro`
4. Clique em "Criar e continuar"
5. Pule as etapas de permissões (clique em "Continuar")
6. Clique em "Concluído"

### 4. Gerar Chave JSON

1. Na lista de contas de serviço, clique na que você criou
2. Vá na aba "Chaves"
3. Clique em "Adicionar chave" > "Criar nova chave"
4. Selecione "JSON"
5. Clique em "Criar"
6. O arquivo será baixado automaticamente

### 5. Configurar o Projeto

1. Renomeie o arquivo baixado para `google-credentials.json`
2. Mova-o para a raiz do projeto (`dashboard-financeiro/`)
3. **IMPORTANTE**: Adicione `google-credentials.json` ao `.gitignore`

### 6. Compartilhar a Planilha

1. Abra sua planilha no Google Sheets
2. Clique em "Compartilhar" (canto superior direito)
3. Adicione o email da conta de serviço (encontrado no arquivo JSON)
4. Dê permissão de "Editor"

### 7. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
USE_GOOGLE_SHEETS=true
GOOGLE_SPREADSHEET_ID=seu_id_da_planilha_aqui
GOOGLE_SHEET_NAME=Lancamentos
GOOGLE_CREDENTIALS_FILE=google-credentials.json
```

### 8. Migrar Dados Existentes

Execute o script de migração:

```bash
streamlit run migrate_to_sheets.py
```

## 🔍 Verificação

Para verificar se tudo está funcionando:

1. Execute o dashboard: `streamlit run app.py`
2. Verifique se aparece "Google Sheets" como fonte de dados
3. Teste adicionando um novo lançamento
4. Verifique se aparece na planilha

## 🛠️ Solução de Problemas

### Erro: "Módulo Google Sheets não disponível"
- Execute: `pip install gspread google-auth`

### Erro: "Arquivo de credenciais não encontrado"
- Verifique se `google-credentials.json` está na raiz do projeto

### Erro: "Acesso negado"
- Verifique se a planilha foi compartilhada com o email da conta de serviço

### Erro: "ID da planilha inválido"
- Verifique se o ID está correto na URL da planilha

## 🔄 Alternância entre CSV e Google Sheets

Para voltar a usar CSV:
```env
USE_GOOGLE_SHEETS=false
```

Para usar Google Sheets:
```env
USE_GOOGLE_SHEETS=true
GOOGLE_SPREADSHEET_ID=seu_id_aqui
```

## 📊 Estrutura da Planilha

A planilha deve ter as seguintes colunas:
- **Data**: Data do lançamento (formato: YYYY-MM-DD)
- **Descrição**: Descrição do lançamento
- **Categoria**: Categoria (ex: Alimentação, Salário)
- **Tipo**: Receita ou Despesa
- **Valor**: Valor numérico

## 🔒 Segurança

- Nunca commite o arquivo `google-credentials.json`
- Mantenha as credenciais seguras
- Use contas de serviço específicas para cada projeto 