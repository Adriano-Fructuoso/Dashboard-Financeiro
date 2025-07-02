"""
Configurações do Dashboard Financeiro
"""

import os
from typing import Optional

# Configurações do Supabase/PostgreSQL
def get_supabase_config():
    """Obtém configurações do Supabase com fallback"""
    try:
        import streamlit as st
        return {
            'SUPABASE_URL': st.secrets.get("SUPABASE", {}).get("SUPABASE_URL") or os.getenv('SUPABASE_URL', ''),
            'SUPABASE_KEY': st.secrets.get("SUPABASE", {}).get("SUPABASE_KEY") or os.getenv('SUPABASE_KEY', ''),
            'SUPABASE_SERVICE_KEY': st.secrets.get("SUPABASE", {}).get("SUPABASE_SERVICE_KEY") or os.getenv('SUPABASE_SERVICE_KEY', '')
        }
    except:
        # Fallback para variáveis de ambiente (desenvolvimento local)
        return {
            'SUPABASE_URL': os.getenv('SUPABASE_URL', ''),
            'SUPABASE_KEY': os.getenv('SUPABASE_KEY', ''),
            'SUPABASE_SERVICE_KEY': os.getenv('SUPABASE_SERVICE_KEY', '')
        }

# Configurações iniciais (serão atualizadas quando necessário)
config = get_supabase_config()
SUPABASE_URL = config['SUPABASE_URL']
SUPABASE_KEY = config['SUPABASE_KEY']
SUPABASE_SERVICE_KEY = config['SUPABASE_SERVICE_KEY']

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