"""
Módulo Core - Lógica de Negócio do Dashboard Financeiro
Versão Otimizada - Performance e Eficiência Melhoradas
Suporte a Google Sheets e CSV
"""

import pandas as pd
from datetime import datetime, timedelta
import os
from typing import Dict, List, Optional, Tuple, Union
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constantes
COLUNAS_PADRAO = ['Data', 'Descrição', 'Categoria', 'Tipo', 'Valor']
TIPOS_VALIDOS = ['Receita', 'Despesa']

# Configuração do backend de dados
USE_GOOGLE_SHEETS = os.getenv('USE_GOOGLE_SHEETS', 'false').lower() == 'true'
GOOGLE_SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID', '')
GOOGLE_SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME', 'Lancamentos')

class FinanceiroError(Exception):
    """Exceção personalizada para erros financeiros"""
    pass

def carregar_dados(data_path: Optional[str] = None, usuario: Optional[str] = None) -> pd.DataFrame:
    """
    Carrega dados financeiros do arquivo CSV ou Google Sheets com validação.
    
    Args:
        data_path: Caminho para o arquivo CSV (opcional se usando Google Sheets)
        usuario: Nome do usuário para usar como nome da aba no Google Sheets
        
    Returns:
        DataFrame pandas com os dados financeiros
    """
    try:
        if USE_GOOGLE_SHEETS and GOOGLE_SPREADSHEET_ID:
            logger.info(f"Carregando dados do Google Sheets: {GOOGLE_SPREADSHEET_ID}")
            try:
                from utils.google_sheets import read_sheet_as_dataframe, ensure_user_sheet_exists
                
                # Usar nome do usuário como nome da aba, ou padrão se não fornecido
                sheet_name = usuario if usuario else GOOGLE_SHEET_NAME
                
                # Garantir que a aba existe
                ensure_user_sheet_exists(GOOGLE_SPREADSHEET_ID, sheet_name)
                
                df = read_sheet_as_dataframe(GOOGLE_SPREADSHEET_ID, sheet_name)
                logger.info(f"Dados carregados do Google Sheets (aba {sheet_name}): {len(df)} registros")
            except ImportError:
                logger.warning("Módulo Google Sheets não disponível, usando CSV")
                df = _carregar_csv(data_path)
            except Exception as e:
                logger.error(f"Erro ao carregar do Google Sheets: {e}")
                logger.info("Fallback para CSV")
                df = _carregar_csv(data_path)
        else:
            df = _carregar_csv(data_path)
        
        # Validar estrutura do DataFrame
        if not all(col in df.columns for col in COLUNAS_PADRAO):
            logger.warning("Estrutura do arquivo inválida. Criando novo DataFrame.")
            return criar_dataframe_vazio()
        
        # Validar tipos de dados
        df = validar_e_corrigir_dados(df)
        
        return df
            
    except Exception as e:
        logger.error(f"Erro ao carregar dados: {e}")
        return criar_dataframe_vazio()

def _carregar_csv(data_path: Optional[str]) -> pd.DataFrame:
    """Carrega dados do arquivo CSV"""
    if data_path and os.path.exists(data_path):
        logger.info(f"Carregando dados de: {data_path}")
        df = pd.read_csv(data_path, parse_dates=['Data'])
        logger.info(f"Dados carregados com sucesso: {len(df)} registros")
        return df
    else:
        logger.info("Arquivo não existe. Criando DataFrame vazio.")
        return criar_dataframe_vazio()

def criar_dataframe_vazio() -> pd.DataFrame:
    """Cria um DataFrame vazio com estrutura padrão"""
    return pd.DataFrame(columns=COLUNAS_PADRAO)

def validar_e_corrigir_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Valida e corrige dados do DataFrame.
    
    Args:
        df: DataFrame a ser validado
        
    Returns:
        DataFrame corrigido
    """
    df_clean = df.copy()
    
    # Converter Data para datetime se necessário
    if 'Data' in df_clean.columns:
        df_clean['Data'] = pd.to_datetime(df_clean['Data'], errors='coerce')
        # Remover linhas com datas inválidas
        df_clean = df_clean.dropna(subset=['Data'])
    
    # Validar Tipo
    if 'Tipo' in df_clean.columns:
        df_clean = df_clean[df_clean['Tipo'].isin(TIPOS_VALIDOS)]
    
    # Validar Valor
    if 'Valor' in df_clean.columns:
        df_clean['Valor'] = pd.to_numeric(df_clean['Valor'], errors='coerce')
        df_clean = df_clean.dropna(subset=['Valor'])
        df_clean = df_clean[df_clean['Valor'] >= 0]  # Valores não negativos
    
    return df_clean

def salvar_dados(df: pd.DataFrame, data_path: Optional[str] = None, usuario: Optional[str] = None) -> bool:
    """
    Salva DataFrame no arquivo CSV ou Google Sheets com validação.
    
    Args:
        df: DataFrame a ser salvo
        data_path: Caminho do arquivo (opcional se usando Google Sheets)
        usuario: Nome do usuário para usar como nome da aba no Google Sheets
        
    Returns:
        True se salvou com sucesso, False caso contrário
    """
    try:
        # Validar DataFrame antes de salvar
        if not isinstance(df, pd.DataFrame):
            raise FinanceiroError("Dados inválidos: não é um DataFrame")
        
        if not all(col in df.columns for col in COLUNAS_PADRAO):
            raise FinanceiroError("Estrutura do DataFrame inválida")
        
        if USE_GOOGLE_SHEETS and GOOGLE_SPREADSHEET_ID:
            logger.info(f"Salvando dados no Google Sheets: {GOOGLE_SPREADSHEET_ID}")
            try:
                from utils.google_sheets import write_dataframe_to_sheet, ensure_user_sheet_exists
                
                # Usar nome do usuário como nome da aba, ou padrão se não fornecido
                sheet_name = usuario if usuario else GOOGLE_SHEET_NAME
                
                # Garantir que a aba existe
                ensure_user_sheet_exists(GOOGLE_SPREADSHEET_ID, sheet_name)
                
                write_dataframe_to_sheet(df, GOOGLE_SPREADSHEET_ID, sheet_name)
                logger.info(f"Dados salvos no Google Sheets (aba {sheet_name}) com sucesso: {len(df)} registros")
                return True
            except ImportError:
                logger.warning("Módulo Google Sheets não disponível, salvando em CSV")
                return _salvar_csv(df, data_path)
            except Exception as e:
                logger.error(f"Erro ao salvar no Google Sheets: {e}")
                logger.info("Fallback para CSV")
                return _salvar_csv(df, data_path)
        else:
            return _salvar_csv(df, data_path)
            
    except Exception as e:
        logger.error(f"Erro ao salvar dados: {e}")
        raise FinanceiroError(f"Erro ao salvar dados: {e}")

def _salvar_csv(df: pd.DataFrame, data_path: Optional[str]) -> bool:
    """Salva DataFrame no arquivo CSV"""
    if not data_path:
        logger.error("Caminho do arquivo não fornecido")
        return False
        
    try:
        # Garantir que o diretório existe
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        
        # Salvar o DataFrame
        df.to_csv(data_path, index=False)
        
        # Verificar se o arquivo foi criado
        if os.path.exists(data_path):
            logger.info(f"Dados salvos com sucesso em: {data_path}")
            logger.info(f"Total de registros salvos: {len(df)}")
            return True
        else:
            logger.error(f"Arquivo não foi criado em: {data_path}")
            return False
            
    except Exception as e:
        logger.error(f"Erro ao salvar CSV: {e}")
        return False

def validar_lancamento(data: Union[str, datetime], descricao: str, categoria: str, 
                      tipo: str, valor: Union[str, float]) -> Dict:
    """
    Valida dados de um lançamento antes de adicionar.
    
    Args:
        data: Data do lançamento
        descricao: Descrição do lançamento
        categoria: Categoria do lançamento
        tipo: Tipo (Receita/Despesa)
        valor: Valor do lançamento
        
    Returns:
        Dicionário com dados validados
        
    Raises:
        FinanceiroError: Se os dados são inválidos
    """
    # Validar data
    try:
        data_validada = pd.to_datetime(data)
        if data_validada > datetime.now() + timedelta(days=1):  # Permite lançamentos futuros de até 1 dia
            raise FinanceiroError("Data não pode ser muito futura")
    except:
        raise FinanceiroError("Data inválida")
    
    # Validar descrição
    if not descricao or not descricao.strip():
        raise FinanceiroError("Descrição é obrigatória")
    
    # Validar categoria
    if not categoria or not categoria.strip():
        raise FinanceiroError("Categoria é obrigatória")
    
    # Validar tipo
    if tipo not in TIPOS_VALIDOS:
        raise FinanceiroError(f"Tipo deve ser um dos seguintes: {TIPOS_VALIDOS}")
    
    # Validar valor
    try:
        valor_validado = float(valor)
        if valor_validado <= 0:
            raise FinanceiroError("Valor deve ser maior que zero")
    except:
        raise FinanceiroError("Valor inválido")
    
    return {
        'Data': data_validada,
        'Descrição': descricao.strip(),
        'Categoria': categoria.strip(),
        'Tipo': tipo,
        'Valor': valor_validado
    }

def adicionar_lancamento(data: Union[str, datetime], descricao: str, categoria: str, 
                        tipo: str, valor: Union[str, float], data_path: Optional[str] = None, 
                        usuario: Optional[str] = None) -> bool:
    """
    Adiciona um novo lançamento com validação completa.
    
    Args:
        data: Data do lançamento
        descricao: Descrição do lançamento
        categoria: Categoria do lançamento
        tipo: Tipo (Receita/Despesa)
        valor: Valor do lançamento
        data_path: Caminho do arquivo CSV (opcional se usando Google Sheets)
        usuario: Nome do usuário para usar como nome da aba no Google Sheets
        
    Returns:
        True se adicionou com sucesso
        
    Raises:
        FinanceiroError: Se os dados são inválidos
    """
    try:
        # Validar dados
        dados_validados = validar_lancamento(data, descricao, categoria, tipo, valor)
        
        logger.info(f"Adicionando lançamento: {dados_validados['Descrição']} - {dados_validados['Categoria']} - {dados_validados['Tipo']} - R$ {dados_validados['Valor']}")
        
        # Carregar dados existentes
        df = carregar_dados(data_path, usuario)
        
        # Adicionar novo lançamento
        novo_registro = pd.DataFrame([dados_validados])
        df = pd.concat([df, novo_registro], ignore_index=True)
        
        # Salvar dados
        if salvar_dados(df, data_path, usuario):
            logger.info("Lançamento adicionado com sucesso!")
            return True
        else:
            raise FinanceiroError("Erro ao salvar dados")
        
    except Exception as e:
        logger.error(f"Erro ao adicionar lançamento: {e}")
        raise FinanceiroError(f"Erro ao adicionar lançamento: {e}")

def listar_lancamentos(data_path: Optional[str] = None, usuario: Optional[str] = None) -> pd.DataFrame:
    """
    Retorna todos os lançamentos como DataFrame.
    
    Args:
        data_path: Caminho do arquivo CSV (opcional se usando Google Sheets)
        usuario: Nome do usuário para usar como nome da aba no Google Sheets
        
    Returns:
        DataFrame com todos os lançamentos
    """
    return carregar_dados(data_path, usuario)

def remover_lancamento(indice: int, data_path: Optional[str] = None, usuario: Optional[str] = None) -> bool:
    """
    Remove um lançamento pelo índice com validação.
    
    Args:
        indice: Índice do lançamento a ser removido
        data_path: Caminho do arquivo CSV (opcional se usando Google Sheets)
        usuario: Nome do usuário para usar como nome da aba no Google Sheets
        
    Returns:
        True se removeu com sucesso
        
    Raises:
        FinanceiroError: Se o índice é inválido
    """
    try:
        logger.info(f"Removendo lançamento no índice: {indice}")
        
        df = carregar_dados(data_path, usuario)
        
        if indice < 0 or indice >= len(df):
            raise FinanceiroError(f"Índice {indice} inválido. Total de registros: {len(df)}")
        
        # Remover lançamento
        df = df.drop(indice).reset_index(drop=True)
        
        # Salvar dados
        if salvar_dados(df, data_path, usuario):
            logger.info(f"Lançamento removido. Novo total: {len(df)} registros")
            return True
        else:
            raise FinanceiroError("Erro ao salvar dados após remoção")
            
    except Exception as e:
        logger.error(f"Erro ao remover lançamento: {e}")
        raise FinanceiroError(f"Erro ao remover lançamento: {e}")

def editar_lancamento(indice: int, data: Union[str, datetime], descricao: str, 
                     categoria: str, tipo: str, valor: Union[str, float], data_path: Optional[str] = None,
                     usuario: Optional[str] = None) -> bool:
    """
    Edita um lançamento existente com validação completa.
    
    Args:
        indice: Índice do lançamento a ser editado
        data: Nova data
        descricao: Nova descrição
        categoria: Nova categoria
        tipo: Novo tipo
        valor: Novo valor
        data_path: Caminho do arquivo CSV (opcional se usando Google Sheets)
        usuario: Nome do usuário para usar como nome da aba no Google Sheets
        
    Returns:
        True se editou com sucesso
        
    Raises:
        FinanceiroError: Se os dados são inválidos
    """
    try:
        # Validar dados
        dados_validados = validar_lancamento(data, descricao, categoria, tipo, valor)
        
        logger.info(f"Editando lançamento no índice: {indice}")
        logger.info(f"Novos dados: {dados_validados['Descrição']} - {dados_validados['Categoria']} - {dados_validados['Tipo']} - R$ {dados_validados['Valor']}")
        
        df = carregar_dados(data_path, usuario)
        
        if indice < 0 or indice >= len(df):
            raise FinanceiroError(f"Índice {indice} inválido. Total de registros: {len(df)}")
        
        # Atualizar dados
        for col, valor in dados_validados.items():
            df.at[indice, col] = valor
        
        # Salvar dados
        if salvar_dados(df, data_path, usuario):
            logger.info(f"Lançamento editado. Total de registros: {len(df)}")
            return True
        else:
            raise FinanceiroError("Erro ao salvar dados após edição")
            
    except Exception as e:
        logger.error(f"Erro ao editar lançamento: {e}")
        raise FinanceiroError(f"Erro ao editar lançamento: {e}")

def filtrar_por_categoria(categoria: str, data_path: Optional[str] = None, usuario: Optional[str] = None) -> pd.DataFrame:
    """
    Filtra lançamentos por categoria.
    
    Args:
        categoria: Categoria para filtrar
        data_path: Caminho do arquivo CSV (opcional se usando Google Sheets)
        usuario: Nome do usuário para usar como nome da aba no Google Sheets
        
    Returns:
        DataFrame filtrado
    """
    df = carregar_dados(data_path, usuario)
    return df[df['Categoria'] == categoria]

def buscar_por_periodo(data_inicio: Union[str, datetime], data_fim: Union[str, datetime], 
                      data_path: Optional[str] = None, usuario: Optional[str] = None) -> pd.DataFrame:
    """
    Filtra lançamentos por período.
    
    Args:
        data_inicio: Data de início
        data_fim: Data de fim
        data_path: Caminho do arquivo CSV (opcional se usando Google Sheets)
        usuario: Nome do usuário para usar como nome da aba no Google Sheets
        
    Returns:
        DataFrame filtrado
    """
    df = carregar_dados(data_path, usuario)
    
    # Converter datas
    data_inicio = pd.to_datetime(data_inicio)
    data_fim = pd.to_datetime(data_fim)
    
    # Filtrar por período
    mask = (df['Data'] >= data_inicio) & (df['Data'] <= data_fim)
    return df[mask]

def calcular_somatorio_geral(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calcula somatório geral de receitas, despesas e saldo.
    
    Args:
        df: DataFrame com os dados
        
    Returns:
        Dicionário com receitas, despesas e saldo
    """
    if df.empty:
        return {'receitas': 0.0, 'despesas': 0.0, 'saldo': 0.0}
    
    receitas = df[df['Tipo'] == 'Receita']['Valor'].sum()
    despesas = df[df['Tipo'] == 'Despesa']['Valor'].sum()
    saldo = receitas - despesas
    
    return {
        'receitas': float(receitas),
        'despesas': float(despesas),
        'saldo': float(saldo)
    }

def calcular_somatorio_por_categoria(df: pd.DataFrame) -> Tuple[Dict[str, float], Dict[str, float]]:
    """
    Calcula somatório por categoria separando receitas e despesas.
    
    Args:
        df: DataFrame com os dados
        
    Returns:
        Tupla com (receitas_por_categoria, despesas_por_categoria)
    """
    if df.empty:
        return {}, {}
    
    receitas_por_categoria = df[df['Tipo'] == 'Receita'].groupby('Categoria')['Valor'].sum().to_dict()
    despesas_por_categoria = df[df['Tipo'] == 'Despesa'].groupby('Categoria')['Valor'].sum().to_dict()
    
    return receitas_por_categoria, despesas_por_categoria

def calcular_evolucao_mensal(df: pd.DataFrame, meses: int = 6) -> pd.DataFrame:
    """
    Calcula evolução financeira dos últimos N meses.
    
    Args:
        df: DataFrame com os dados
        meses: Número de meses para analisar
        
    Returns:
        DataFrame com receitas, despesas e saldo por mês
    """
    if df.empty:
        return pd.DataFrame()
    
    # Adicionar colunas de mês e ano
    df_copy = df.copy()
    df_copy['Ano'] = df_copy['Data'].dt.year
    df_copy['Mes'] = df_copy['Data'].dt.month
    df_copy['Mes_Ano'] = df_copy['Data'].dt.to_period('M')
    
    # Obter últimos N meses
    meses_unicos = sorted(df_copy['Mes_Ano'].unique(), reverse=True)[:meses]
    
    if not meses_unicos:
        return pd.DataFrame()
    
    # Calcular totais por mês
    evolucao = []
    for mes in reversed(meses_unicos):  # Ordem cronológica
        dados_mes = df_copy[df_copy['Mes_Ano'] == mes]
        
        receitas = dados_mes[dados_mes['Tipo'] == 'Receita']['Valor'].sum()
        despesas = dados_mes[dados_mes['Tipo'] == 'Despesa']['Valor'].sum()
        saldo = receitas - despesas
        
        evolucao.append({
            'Mes': str(mes),
            'Receitas': float(receitas),
            'Despesas': float(despesas),
            'Saldo': float(saldo)
        })
    
    return pd.DataFrame(evolucao)

def comparar_meses(df: pd.DataFrame, mes1: pd.Period, mes2: pd.Period) -> Optional[Dict]:
    """
    Compara dois meses específicos.
    
    Args:
        df: DataFrame com os dados
        mes1: Primeiro mês para comparação
        mes2: Segundo mês para comparação
        
    Returns:
        Dicionário com comparação ou None se não houver dados
    """
    if df.empty:
        return None
    
    # Adicionar coluna de mês/ano
    df_copy = df.copy()
    df_copy['Mes_Ano'] = df_copy['Data'].dt.to_period('M')
    
    # Filtrar dados dos meses
    dados_mes1 = df_copy[df_copy['Mes_Ano'] == mes1]
    dados_mes2 = df_copy[df_copy['Mes_Ano'] == mes2]
    
    if dados_mes1.empty and dados_mes2.empty:
        return None
    
    # Calcular totais
    def calcular_totais_mes(dados_mes):
        if dados_mes.empty:
            return {'receitas': 0.0, 'despesas': 0.0, 'saldo': 0.0}
        
        receitas = dados_mes[dados_mes['Tipo'] == 'Receita']['Valor'].sum()
        despesas = dados_mes[dados_mes['Tipo'] == 'Despesa']['Valor'].sum()
        saldo = receitas - despesas
        
        return {
            'receitas': float(receitas),
            'despesas': float(despesas),
            'saldo': float(saldo)
        }
    
    totais_mes1 = calcular_totais_mes(dados_mes1)
    totais_mes2 = calcular_totais_mes(dados_mes2)
    
    # Calcular diferenças
    diferenca = {
        'receitas': totais_mes1['receitas'] - totais_mes2['receitas'],
        'despesas': totais_mes1['despesas'] - totais_mes2['despesas'],
        'saldo': totais_mes1['saldo'] - totais_mes2['saldo']
    }
    
    return {
        'mes1': totais_mes1,
        'mes2': totais_mes2,
        'diferenca': diferenca
    }

def obter_top_categorias_mes(df: pd.DataFrame, mes: pd.Period, tipo: str, top_n: int = 5) -> Dict[str, float]:
    """
    Obtém as top categorias de um mês específico.
    
    Args:
        df: DataFrame com os dados
        mes: Mês para análise
        tipo: Tipo (Receita/Despesa)
        top_n: Número de categorias a retornar
        
    Returns:
        Dicionário com categoria: valor
    """
    if df.empty or tipo not in TIPOS_VALIDOS:
        return {}
    
    # Adicionar coluna de mês/ano
    df_copy = df.copy()
    df_copy['Mes_Ano'] = df_copy['Data'].dt.to_period('M')
    
    # Filtrar dados do mês e tipo
    dados_mes = df_copy[(df_copy['Mes_Ano'] == mes) & (df_copy['Tipo'] == tipo)]
    
    if dados_mes.empty:
        return {}
    
    # Agrupar por categoria e somar valores
    top_categorias = dados_mes.groupby('Categoria')['Valor'].sum().sort_values(ascending=False).head(top_n)
    
    return top_categorias.to_dict()

def calcular_media_mensal(df: pd.DataFrame, meses: int = 6) -> Optional[Dict[str, float]]:
    """
    Calcula médias mensais dos últimos N meses.
    
    Args:
        df: DataFrame com os dados
        meses: Número de meses para calcular a média
        
    Returns:
        Dicionário com médias ou None se não houver dados
    """
    df_evolucao = calcular_evolucao_mensal(df, meses)
    
    if df_evolucao.empty:
        return None
    
    return {
        'receitas_media': float(df_evolucao['Receitas'].mean()),
        'despesas_media': float(df_evolucao['Despesas'].mean()),
        'saldo_media': float(df_evolucao['Saldo'].mean())
    }

def obter_estatisticas_gerais(df: pd.DataFrame) -> Dict:
    """
    Obtém estatísticas gerais dos dados.
    
    Args:
        df: DataFrame com os dados
        
    Returns:
        Dicionário com estatísticas
    """
    if df.empty:
        return {
            'total_lancamentos': 0,
            'primeiro_lancamento': None,
            'ultimo_lancamento': None,
            'categorias_unicas': 0,
            'periodo_dias': 0
        }
    
    return {
        'total_lancamentos': len(df),
        'primeiro_lancamento': df['Data'].min(),
        'ultimo_lancamento': df['Data'].max(),
        'categorias_unicas': df['Categoria'].nunique(),
        'periodo_dias': (df['Data'].max() - df['Data'].min()).days
    }

