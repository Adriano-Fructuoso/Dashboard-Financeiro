"""	•	O que vai aqui:
Toda a lógica principal de manipulação dos dados financeiros.
	•	Responsabilidades:
	•	Funções para: adicionar lançamento, remover, editar, listar, buscar por período/categoria, salvar e carregar CSV.
	•	Isola as regras do negócio e evita poluir o app.py.
	•	Exemplo de funções que terão aqui:
	•	adicionar_lancamento()
	•	listar_lancamentos()
	•	salvar_dados()
	•	carregar_dados()
	•	filtrar_por_categoria() """

# finance/core.py

import pandas as pd
from datetime import datetime
import os

def carregar_dados(data_path):
    """
    Carrega os dados financeiros do arquivo CSV.
    Retorna um DataFrame pandas.
    """
    if os.path.exists(data_path):
        df = pd.read_csv(data_path, parse_dates=['Data'])
    else:
        # Se não existir, retorna um DataFrame vazio com colunas padrão
        colunas = pd.Index(['Data', 'Descrição', 'Categoria', 'Tipo', 'Valor'])
        df = pd.DataFrame(columns=colunas)
    return df

def salvar_dados(df, data_path):
    """
    Salva o DataFrame no arquivo CSV.
    """
    df.to_csv(data_path, index=False)

def adicionar_lancamento(data, descricao, categoria, tipo, valor, data_path):
    """
    Adiciona um novo lançamento (receita ou despesa).
    """
    df = carregar_dados(data_path)
    novo = {
        'Data': pd.to_datetime(data),
        'Descrição': descricao,
        'Categoria': categoria,
        'Tipo': tipo,
        'Valor': float(valor)
    }
    df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
    salvar_dados(df, data_path)

def listar_lancamentos(data_path):
    """
    Retorna todos os lançamentos como DataFrame.
    """
    return carregar_dados(data_path)

def remover_lancamento(indice, data_path):
    """
    Remove um lançamento pelo índice (linha) no DataFrame.
    """
    df = carregar_dados(data_path)
    df = df.drop(indice).reset_index(drop=True)
    salvar_dados(df, data_path)

def editar_lancamento(indice, data, descricao, categoria, tipo, valor, data_path):
    """
    Edita um lançamento existente pelo índice (linha).
    """
    df = carregar_dados(data_path)
    df.at[indice, 'Data'] = pd.to_datetime(data)
    df.at[indice, 'Descrição'] = descricao
    df.at[indice, 'Categoria'] = categoria
    df.at[indice, 'Tipo'] = tipo
    df.at[indice, 'Valor'] = float(valor)
    salvar_dados(df, data_path)

def filtrar_por_categoria(categoria, data_path):
    """
    Filtra os lançamentos pela categoria.
    """
    df = carregar_dados(data_path)
    return df[df['Categoria'] == categoria]

def buscar_por_periodo(data_inicio, data_fim, data_path):
    """
    Filtra os lançamentos dentro de um período.
    """
    df = carregar_dados(data_path)
    mask = (df['Data'] >= pd.to_datetime(data_inicio)) & (df['Data'] <= pd.to_datetime(data_fim))
    return df[mask]

def calcular_somatorio_geral(df):
    """
    Calcula o somatório geral de receitas, despesas e saldo.
    Retorna um dicionário com os valores.
    """
    receitas = df[df['Tipo'] == 'Receita']['Valor'].sum()
    despesas = df[df['Tipo'] == 'Despesa']['Valor'].sum()
    saldo = receitas - despesas
    
    return {
        'receitas': receitas,
        'despesas': despesas,
        'saldo': saldo
    }

def calcular_somatorio_por_categoria(df):
    """
    Calcula o somatório por categoria separando receitas e despesas.
    Retorna dois dicionários: um para receitas e outro para despesas.
    """
    receitas_por_categoria = df[df['Tipo'] == 'Receita'].groupby('Categoria')['Valor'].sum().to_dict()
    despesas_por_categoria = df[df['Tipo'] == 'Despesa'].groupby('Categoria')['Valor'].sum().to_dict()
    
    return receitas_por_categoria, despesas_por_categoria

# Outras funções podem ser adicionadas depois (por exemplo, somatório por mês, categorias, etc.)

