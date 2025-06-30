import os
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from typing import List

# Escopos necessários para acessar e editar planilhas
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Nome do arquivo de credenciais (agora lido da variável de ambiente)
CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'google-credentials.json')

# Nome da aba padrão
SHEET_NAME = 'Lancamentos'


def get_gspread_client():
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    return gspread.authorize(creds)


def ensure_user_sheet_exists(spreadsheet_id: str, user_sheet_name: str):
    client = get_gspread_client()
    spreadsheet = client.open_by_key(spreadsheet_id)
    try:
        # Tenta acessar a aba existente
        spreadsheet.worksheet(user_sheet_name)
        # Se chegou aqui, a aba existe
        return
    except gspread.exceptions.WorksheetNotFound:
        # Só cria a aba se ela não existir
        try:
            sheet = spreadsheet.add_worksheet(title=user_sheet_name, rows=1000, cols=5)
            sheet.append_row(['Data', 'Descrição', 'Categoria', 'Tipo', 'Valor'])
        except Exception as e:
            # Se der erro ao criar (ex: aba já existe), ignora
            print(f"Aviso: Não foi possível criar a aba '{user_sheet_name}': {e}")
            pass


def read_sheet_as_dataframe(spreadsheet_id: str, sheet_name: str) -> pd.DataFrame:
    client = get_gspread_client()
    sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
    data = sheet.get_all_records()
    if not data:
        return pd.DataFrame(columns=pd.Index(['Data', 'Descrição', 'Categoria', 'Tipo', 'Valor']))
    df = pd.DataFrame(data)
    # Converter coluna Data para datetime se existir
    if 'Data' in df.columns:
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    return df


def write_dataframe_to_sheet(df: pd.DataFrame, spreadsheet_id: str, sheet_name: str):
    client = get_gspread_client()
    spreadsheet = client.open_by_key(spreadsheet_id)
    try:
        sheet = spreadsheet.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=5)
        sheet.append_row(['Data', 'Descrição', 'Categoria', 'Tipo', 'Valor'])
    # Selecionar apenas as colunas padrão
    colunas_padrao = ['Data', 'Descrição', 'Categoria', 'Tipo', 'Valor']
    df_to_write = df.copy()
    df_to_write = df_to_write[[col for col in colunas_padrao if col in df_to_write.columns]]
    # Limpar a aba antes de escrever
    sheet.clear()
    # Escrever cabeçalho e dados
    values = [df_to_write.columns.values.tolist()] + df_to_write.fillna('').astype(str).values.tolist()
    sheet.update('A1', values) 