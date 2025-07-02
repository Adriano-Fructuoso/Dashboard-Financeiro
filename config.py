"""
Configurações do Dashboard Financeiro
"""

import os
from typing import Optional

# Configurações do Supabase/PostgreSQL
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')
DATABASE_URL = os.getenv('DATABASE_URL', '')

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
    if SUPABASE_URL and SUPABASE_KEY:
        return f"Supabase ({SUPABASE_URL})"
    elif DATABASE_URL:
        return "PostgreSQL"
    else:
        return "Configuração de banco não encontrada"

def is_database_configured() -> bool:
    """Verifica se o banco de dados está configurado"""
    return bool(SUPABASE_URL and SUPABASE_KEY) or bool(DATABASE_URL) 