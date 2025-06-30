# 💰 Dashboard Financeiro Pessoal

Um dashboard moderno e eficiente para controle financeiro pessoal, desenvolvido com Python e Streamlit. Agora com suporte a **Google Sheets** como banco de dados e sistema multi-usuário!

![Dashboard Financeiro](https://img.shields.io/badge/Status-Produção-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.46+-red)
![Google Sheets](https://img.shields.io/badge/Google%20Sheets-API-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚀 Características

### ✨ Interface Moderna
- **Design responsivo** e intuitivo
- **Tema personalizado** com cores atrativas
- **Navegação fluida** com sidebar organizada
- **Cards de métricas** visuais e informativos

### 🔐 Sistema Multi-Usuário
- **Login/Cadastro** completo com autenticação
- **Isolamento de dados** - cada usuário tem sua própria aba no Google Sheets
- **Privacidade total** - usuários não podem ver dados de outros
- **Criação automática** de abas para novos usuários

### 📊 Funcionalidades Principais
- **Sistema de login** com múltiplos usuários
- **Gestão completa** de receitas e despesas
- **Categorização automática** de lançamentos
- **Filtros avançados** por período e categoria
- **Relatórios mensais** com comparações
- **Gráficos interativos** e informativos
- **Sincronização automática** com Google Sheets

### 📈 Análises e Relatórios
- **Resumo financeiro** em tempo real
- **Evolução do saldo** ao longo do tempo
- **Distribuição por categorias** (receitas e despesas)
- **Comparativo mensal** detalhado
- **Médias e tendências** dos últimos meses
- **Exportação de dados** em CSV

### 🔧 Recursos Técnicos
- **Validação robusta** de dados
- **Tratamento de erros** elegante
- **Performance otimizada** para grandes volumes
- **Persistência segura** no Google Sheets
- **Backup automático** e sincronização

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+** - Linguagem principal
- **Streamlit** - Framework web para dashboards
- **Google Sheets API** - Armazenamento e sincronização
- **Pandas** - Manipulação e análise de dados
- **Plotly** - Gráficos interativos
- **Matplotlib** - Geração de gráficos
- **NumPy** - Computação numérica

## 📦 Instalação

### Pré-requisitos
- Python 3.9 ou superior
- Conta Google com Google Sheets
- Credenciais da Google Sheets API

### Configuração do Google Sheets

1. **Siga o guia completo** em `GOOGLE_SHEETS_SETUP.md`
2. **Configure as credenciais** no arquivo `config.py`
3. **Compartilhe sua planilha** com o email da conta de serviço

### Passos para Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/Adriano-Fructuoso/Dashboard-Financeiro.git
cd Dashboard-Financeiro
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

5. **Configure as credenciais**
   - Edite `config.py` com suas configurações
   - Configure o `GOOGLE_SPREADSHEET_ID`

6. **Execute o aplicativo**
```bash
streamlit run app.py
```

7. **Acesse no navegador**
```
http://localhost:8501
```

## 🎯 Como Usar

### Primeiro Acesso
1. Acesse o dashboard no navegador
2. Clique em "Nova Conta" para criar seu usuário
3. Defina um nome de usuário e senha
4. Sistema criará automaticamente sua aba no Google Sheets
5. Faça login com suas credenciais

### Adicionando Lançamentos
1. Vá para "➕ Novo Lançamento"
2. Preencha os campos:
   - **Data**: Data do lançamento
   - **Descrição**: Descrição detalhada
   - **Tipo**: Receita ou Despesa
   - **Categoria**: Categoria pré-definida
   - **Valor**: Valor em reais
3. Clique em "Adicionar Lançamento"
4. Dados são salvos automaticamente na sua aba

### Visualizando Relatórios
1. **Resumo**: Visão geral das finanças
2. **Relatórios Mensais**: Análises detalhadas por mês
3. **Gerenciar Dados**: Exportar e gerenciar dados

### Filtros Disponíveis
- **Período**: Último mês, 3 meses, 6 meses, ano atual
- **Mês específico**: Seleção de mês específico
- **Categorias**: Filtro por categorias específicas

## 📁 Estrutura do Projeto

```
dashboard-financeiro/
├── app.py                 # Aplicação principal
├── config.py             # Configurações e credenciais
├── requirements.txt       # Dependências
├── README.md             # Documentação
├── GOOGLE_SHEETS_SETUP.md # Guia de configuração
├── data/                 # Dados dos usuários
│   ├── usuarios.json     # Usuários cadastrados
│   └── dados_*.csv       # Backup local dos dados
├── finance/              # Módulos de lógica
│   ├── __init__.py
│   ├── core.py          # Lógica de negócio
│   └── charts.py        # Geração de gráficos
└── utils/               # Utilitários
    ├── __init__.py
    └── google_sheets.py # Integração Google Sheets
```

## 🔧 Configuração

### Google Sheets Setup
1. **Crie um projeto** no Google Cloud Console
2. **Ative a Google Sheets API**
3. **Crie credenciais** de conta de serviço
4. **Compartilhe sua planilha** com o email da conta de serviço
5. **Configure o SPREADSHEET_ID** no `config.py`

### Estrutura da Planilha
- **Cada usuário tem sua própria aba**
- **Colunas padrão**: Data, Descrição, Categoria, Tipo, Valor
- **Sistema cria abas automaticamente** para novos usuários
- **Sincronização automática** entre aplicação e planilha

### Variáveis de Configuração
```python
# config.py
USE_GOOGLE_SHEETS = True
GOOGLE_SPREADSHEET_ID = "seu-spreadsheet-id"
GOOGLE_SHEET_NAME = "Adriano"  # Aba padrão
```

## 📊 Funcionalidades Detalhadas

### Sistema Multi-Usuário
- **Múltiplos usuários** com dados completamente isolados
- **Autenticação segura** com nome/senha
- **Criação automática** de abas no Google Sheets
- **Privacidade total** - cada usuário só vê seus dados

### Gestão de Dados
- **CRUD completo** (Criar, Ler, Atualizar, Deletar)
- **Validação de dados** em tempo real
- **Sincronização automática** com Google Sheets
- **Backup local** em arquivos CSV
- **Exportação** de dados para análise externa

### Análises Financeiras
- **Saldo em tempo real** com histórico
- **Categorização inteligente** de gastos
- **Tendências mensais** e sazonais
- **Comparativos** entre períodos
- **Relatórios avançados** com gráficos

## 🚀 Deploy

### Local
```bash
streamlit run app.py
```

### Heroku
1. Crie um arquivo `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Configure as variáveis de ambiente no Heroku:
   - `GOOGLE_SPREADSHEET_ID`
   - `GOOGLE_CREDENTIALS_JSON`

### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🔒 Segurança

- **Isolamento de Dados**: Cada usuário só acessa seus próprios dados
- **Autenticação**: Sistema de login/cadastro
- **Privacidade**: Nenhum usuário pode ver dados de outros
- **Backup**: Dados sincronizados automaticamente no Google Sheets

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Para dúvidas ou problemas:
- Abra uma issue no GitHub
- Consulte a documentação em `GOOGLE_SHEETS_SETUP.md`

## 🔄 Changelog

### v2.0.0 - Sistema Multi-Usuário com Google Sheets
- ✅ Sistema completo de login/cadastro
- ✅ Isolamento de dados por usuário
- ✅ Integração com Google Sheets por aba
- ✅ Interface moderna e responsiva
- ✅ Relatórios avançados
- ✅ Sistema de backup automático
- ✅ Sincronização em tempo real

### v1.0.0 - Versão Inicial
- ✅ Dashboard básico
- ✅ CRUD de lançamentos
- ✅ Gráficos simples
- ✅ Integração CSV

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Adriano Fructuoso**
- GitHub: [@Adriano-Fructuoso](https://github.com/Adriano-Fructuoso)
- LinkedIn: [Adriano Fructuoso](https://linkedin.com/in/adriano-fructuoso)

## 🙏 Agradecimentos

- **Streamlit** pela excelente framework
- **Pandas** pela manipulação de dados
- **Matplotlib** pelos gráficos
- **Comunidade Python** pelo suporte

## 📞 Suporte

Se você encontrar algum problema ou tiver sugestões:

1. **Issues**: Abra uma issue no GitHub
2. **Discussions**: Use as discussions para perguntas
3. **Email**: Entre em contato diretamente

---

⭐ **Se este projeto te ajudou, considere dar uma estrela!**

## 🔄 Integração Google Sheets

### Vantagens
- ✅ **Sincronização Automática**: Dados sempre atualizados
- ✅ **Backup na Nuvem**: Segurança dos dados
- ✅ **Acesso Multiplataforma**: Use de qualquer lugar
- ✅ **Colaboração**: Compartilhe com outros usuários
- ✅ **Histórico**: Versionamento automático

### Configuração
1. Siga o guia [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md)
2. Configure as variáveis de ambiente
3. Teste a conexão com `test_google_sheets.py`
4. Migre dados existentes com `migrate_to_sheets.py`

## 🛠️ Desenvolvimento

### Estrutura de Dados
```python
# Colunas padrão
COLUNAS_PADRAO = ['Data', 'Descrição', 'Categoria', 'Tipo', 'Valor']
TIPOS_VALIDOS = ['Receita', 'Despesa']
```

### Adicionando Novas Funcionalidades
1. Implemente a lógica em `finance/core.py`
2. Crie visualizações em `finance/charts.py`
3. Adicione interface em `app.py`
4. Atualize documentação

## 🔒 Segurança

- Credenciais do Google Sheets protegidas
- Validação de dados em todas as operações
- Tratamento de erros robusto
- Logs detalhados para auditoria

## 📈 Performance

- Carregamento otimizado de dados
- Cache inteligente de gráficos
- Validação eficiente de dados
- Interface responsiva

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🆘 Suporte

- 📖 **Documentação**: [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md)
- 🧪 **Testes**: `streamlit run test_google_sheets.py`
- 🐛 **Issues**: Abra uma issue no GitHub

---

**Desenvolvido com ❤️ para controle financeiro eficiente!**
