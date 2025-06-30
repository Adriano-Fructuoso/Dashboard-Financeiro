# 💰 Dashboard Financeiro Pessoal

Um dashboard moderno e eficiente para controle financeiro pessoal, desenvolvido com Python e Streamlit. Agora com suporte a **Google Sheets** como banco de dados!

![Dashboard Financeiro](https://img.shields.io/badge/Status-Produção-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.46+-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚀 Características

### ✨ Interface Moderna
- **Design responsivo** e intuitivo
- **Tema personalizado** com cores atrativas
- **Navegação fluida** com sidebar organizada
- **Cards de métricas** visuais e informativos

### 📊 Funcionalidades Principais
- **Sistema de login** com múltiplos usuários
- **Gestão completa** de receitas e despesas
- **Categorização automática** de lançamentos
- **Filtros avançados** por período e categoria
- **Relatórios mensais** com comparações
- **Gráficos interativos** e informativos

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
- **Persistência segura** em arquivos CSV
- **Logging detalhado** para debugging

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+** - Linguagem principal
- **Streamlit** - Framework web para dashboards
- **Pandas** - Manipulação e análise de dados
- **Matplotlib** - Geração de gráficos
- **Seaborn** - Estilização de gráficos
- **NumPy** - Computação numérica

## 📦 Instalação

### Pré-requisitos
- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

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

5. **Execute o aplicativo**
```bash
streamlit run app.py
```

6. **Acesse no navegador**
```
http://localhost:8501
```

## 🎯 Como Usar

### Primeiro Acesso
1. Acesse o dashboard no navegador
2. Clique em "Nova Conta" para criar seu usuário
3. Defina um nome de usuário e senha
4. Faça login com suas credenciais

### Adicionando Lançamentos
1. Vá para "➕ Novo Lançamento"
2. Preencha os campos:
   - **Data**: Data do lançamento
   - **Descrição**: Descrição detalhada
   - **Tipo**: Receita ou Despesa
   - **Categoria**: Categoria pré-definida
   - **Valor**: Valor em reais
3. Clique em "Adicionar Lançamento"

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
├── requirements.txt       # Dependências
├── README.md             # Documentação
├── data/                 # Dados dos usuários
│   ├── usuarios.json     # Usuários cadastrados
│   └── dados_*.csv       # Dados financeiros por usuário
├── finance/              # Módulos de lógica
│   ├── __init__.py
│   ├── core.py          # Lógica de negócio
│   └── charts.py        # Geração de gráficos
└── utils/               # Utilitários
    └── __init__.py
```

## 🔧 Configuração

### Variáveis de Ambiente
O projeto não requer variáveis de ambiente especiais, mas você pode configurar:

```bash
# Porta do Streamlit (opcional)
export STREAMLIT_SERVER_PORT=8501

# Configurações de cache (opcional)
export STREAMLIT_CACHE_TTL=3600
```

### Personalização
- **Cores**: Edite o dicionário `COLORS` em `app.py`
- **Categorias**: Modifique `CATEGORIAS` em `app.py`
- **Gráficos**: Ajuste estilos em `finance/charts.py`

## 📊 Funcionalidades Detalhadas

### Sistema de Usuários
- **Múltiplos usuários** com dados isolados
- **Autenticação simples** com nome/senha
- **Criação automática** de arquivos de dados
- **Persistência** em arquivo JSON

### Gestão de Dados
- **CRUD completo** (Criar, Ler, Atualizar, Deletar)
- **Validação de dados** em tempo real
- **Backup automático** em arquivos CSV
- **Exportação** de dados para análise externa

### Análises Financeiras
- **Saldo em tempo real** com histórico
- **Categorização inteligente** de gastos
- **Tendências mensais** e sazonais
- **Comparativos** entre períodos

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

2. Configure as variáveis de ambiente no Heroku

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

## 🤝 Contribuindo

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. Abra um **Pull Request**

### Padrões de Código
- Use **type hints** em todas as funções
- Documente funções com **docstrings**
- Siga o padrão **PEP 8**
- Teste suas mudanças antes de submeter

## 📝 Changelog

### v2.0.0 (Atual)
- ✨ Interface completamente redesenhada
- 🚀 Performance otimizada
- 📊 Gráficos modernos e interativos
- 🔧 Validação robusta de dados
- 📱 Design responsivo
- 🎨 Tema personalizado

### v1.0.0
- 📊 Dashboard básico
- 👤 Sistema de login
- 💰 Gestão de receitas e despesas
- 📈 Gráficos simples

## 📄 Licença

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
