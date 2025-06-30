"""
Configurações do Dashboard Financeiro
"""

import os
from typing import Optional

# Configurações do Google Sheets
USE_GOOGLE_SHEETS = os.getenv('USE_GOOGLE_SHEETS', 'false').lower() == 'true'
GOOGLE_SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID', '')
GOOGLE_SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME', 'Lancamentos')
GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'google-credentials.json')

# Configurações de dados
DEFAULT_CSV_FILE = 'data/dados_Adriano.csv'

# Configurações da aplicação
APP_TITLE = "📊 Dashboard Financeiro"
APP_ICON = "💰"

# Categorias padrão
CATEGORIAS_RECEITA = [
    "Salário",
    "Freelance", 
    "Investimentos",
    "Vendas",
    "Outros"
]

CATEGORIAS_DESPESA = [
    "Alimentação",
    "Transporte",
    "Moradia",
    "Saúde",
    "Educação",
    "Lazer",
    "Vestuário",
    "Contas",
    "Outros"
]

def get_data_source() -> str:
    """Retorna a fonte de dados atual"""
    if USE_GOOGLE_SHEETS and GOOGLE_SPREADSHEET_ID:
        return f"Google Sheets ({GOOGLE_SPREADSHEET_ID})"
    else:
        return f"CSV ({DEFAULT_CSV_FILE})"

def is_google_sheets_enabled() -> bool:
    """Verifica se o Google Sheets está habilitado e configurado"""
    return USE_GOOGLE_SHEETS and bool(GOOGLE_SPREADSHEET_ID) and os.path.exists(GOOGLE_CREDENTIALS_FILE)

def get_spreadsheet_url() -> Optional[str]:
    """Retorna a URL da planilha do Google Sheets"""
    if GOOGLE_SPREADSHEET_ID:
        return f"https://docs.google.com/spreadsheets/d/{GOOGLE_SPREADSHEET_ID}"
    return None 