"""
Módulo Core - Lógica de Negócio do Dashboard Financeiro
Versão Otimizada - Performance e Eficiência Melhoradas
Suporte a PostgreSQL/Supabase
"""

import pandas as pd
from datetime import datetime, timedelta
import os
from typing import Dict, List, Optional, Tuple, Union
import logging
from utils.database import DatabaseManager

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constantes
COLUNAS_PADRAO = ['Data', 'Descrição', 'Categoria', 'Tipo', 'Valor']
TIPOS_VALIDOS = ['Receita', 'Despesa']

class FinanceiroError(Exception):
    """Exceção personalizada para erros financeiros"""
    pass

def carregar_dados(data_path: Optional[str] = None, usuario: Optional[str] = None) -> pd.DataFrame:
    """
    Carrega dados financeiros do banco de dados PostgreSQL.
    
    Args:
        data_path: Caminho para o arquivo CSV (mantido para compatibilidade, mas não usado)
        usuario: Nome do usuário para buscar dados específicos
        
    Returns:
        DataFrame pandas com os dados financeiros
    """
    try:
        if not usuario:
            logger.warning("Usuário não fornecido, retornando DataFrame vazio")
            return criar_dataframe_vazio()
        
        with DatabaseManager() as db:
            # Buscar usuário pelo nome
            user_data = db.get_user_by_name(usuario)
            if not user_data:
                logger.warning(f"Usuário '{usuario}' não encontrado")
                return criar_dataframe_vazio()
            
            # Buscar lançamentos do usuário
            df = db.get_lancamentos_by_user(user_data['id'])
            
            # Renomear colunas para manter compatibilidade
            if not df.empty:
                df = df.rename(columns={
                    'data': 'Data',
                    'descricao': 'Descrição',
                    'categoria': 'Categoria',
                    'tipo': 'Tipo',
                    'valor': 'Valor'
                })
            
            logger.info(f"Dados carregados do banco para usuário '{usuario}': {len(df)} registros")
            return df
            
    except Exception as e:
        logger.error(f"Erro ao carregar dados: {e}")
        return criar_dataframe_vazio()

def criar_dataframe_vazio() -> pd.DataFrame:
    """Cria um DataFrame vazio com estrutura padrão"""
    return pd.DataFrame(columns=pd.Index(COLUNAS_PADRAO))

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
    Salva DataFrame no banco de dados PostgreSQL.
    
    Args:
        df: DataFrame a ser salvo (não usado diretamente, mantido para compatibilidade)
        data_path: Caminho do arquivo (não usado, mantido para compatibilidade)
        usuario: Nome do usuário
        
    Returns:
        True se salvou com sucesso, False caso contrário
    """
    try:
        if not usuario:
            raise FinanceiroError("Usuário não fornecido")
        
        with DatabaseManager() as db:
            # Buscar usuário pelo nome
            user_data = db.get_user_by_name(usuario)
            if not user_data:
                raise FinanceiroError(f"Usuário '{usuario}' não encontrado")
            
            logger.info(f"Dados já estão salvos no banco para usuário '{usuario}'")
            return True
            
    except Exception as e:
        logger.error(f"Erro ao salvar dados: {e}")
        raise FinanceiroError(f"Erro ao salvar dados: {e}")

def validar_lancamento(data: Union[str, datetime], descricao: str, categoria: str, 
                      tipo: str, valor: Union[str, float]) -> Tuple[bool, str]:
    """
    Valida dados de um lançamento financeiro.
    
    Args:
        data: Data do lançamento
        descricao: Descrição do lançamento
        categoria: Categoria do lançamento
        tipo: Tipo (Receita ou Despesa)
        valor: Valor do lançamento
        
    Returns:
        Tupla (é_válido, mensagem_erro)
    """
    try:
        # Validar data
        if isinstance(data, str):
            datetime.strptime(data, '%Y-%m-%d')
        elif not isinstance(data, datetime):
            return False, "Data inválida"
        
        # Validar descrição
        if not descricao or len(descricao.strip()) == 0:
            return False, "Descrição é obrigatória"
        
        # Validar categoria
        if not categoria or len(categoria.strip()) == 0:
            return False, "Categoria é obrigatória"
        
        # Validar tipo
        if tipo not in TIPOS_VALIDOS:
            return False, f"Tipo deve ser um dos seguintes: {', '.join(TIPOS_VALIDOS)}"
        
        # Validar valor
        try:
            valor_float = float(valor)
            if valor_float < 0:
                return False, "Valor deve ser positivo"
        except (ValueError, TypeError):
            return False, "Valor deve ser um número válido"
        
        return True, ""
        
    except Exception as e:
        return False, f"Erro na validação: {str(e)}"

def adicionar_lancamento(data: Union[str, datetime], descricao: str, categoria: str, 
                        tipo: str, valor: Union[str, float], data_path: Optional[str] = None, 
                        usuario: Optional[str] = None) -> bool:
    """
    Adiciona um novo lançamento financeiro ao banco de dados.
    
    Args:
        data: Data do lançamento
        descricao: Descrição do lançamento
        categoria: Categoria do lançamento
        tipo: Tipo (Receita ou Despesa)
        valor: Valor do lançamento
        data_path: Caminho do arquivo (não usado, mantido para compatibilidade)
        usuario: Nome do usuário
        
    Returns:
        True se adicionou com sucesso, False caso contrário
    """
    try:
        if not usuario:
            raise FinanceiroError("Usuário não fornecido")
        
        # Validar dados
        is_valid, error_msg = validar_lancamento(data, descricao, categoria, tipo, valor)
        if not is_valid:
            raise FinanceiroError(error_msg)
        
        # Converter data para string se necessário
        if isinstance(data, datetime):
            data_str = data.strftime('%Y-%m-%d')
        else:
            data_str = str(data)
        
        # Converter valor para float
        valor_float = float(valor)
        
        with DatabaseManager() as db:
            # Buscar usuário pelo nome
            user_data = db.get_user_by_name(usuario)
            if not user_data:
                raise FinanceiroError(f"Usuário '{usuario}' não encontrado")
            
            # Adicionar lançamento
            success = db.add_lancamento(
                user_data['id'], data_str, descricao, categoria, tipo, valor_float
            )
            
            if success:
                logger.info(f"Lançamento adicionado com sucesso para usuário '{usuario}'")
                return True
            else:
                raise FinanceiroError("Erro ao adicionar lançamento no banco")
                
    except Exception as e:
        logger.error(f"Erro ao adicionar lançamento: {e}")
        raise FinanceiroError(f"Erro ao adicionar lançamento: {e}")

def listar_lancamentos(data_path: Optional[str] = None, usuario: Optional[str] = None) -> pd.DataFrame:
    """
    Lista todos os lançamentos de um usuário.
    
    Args:
        data_path: Caminho do arquivo (não usado, mantido para compatibilidade)
        usuario: Nome do usuário
        
    Returns:
        DataFrame com os lançamentos
    """
    return carregar_dados(data_path, usuario)

def remover_lancamento(indice: int, data_path: Optional[str] = None, usuario: Optional[str] = None) -> bool:
    """
    Remove um lançamento pelo índice.
    
    Args:
        indice: Índice do lançamento (não usado diretamente, mantido para compatibilidade)
        data_path: Caminho do arquivo (não usado, mantido para compatibilidade)
        usuario: Nome do usuário
        
    Returns:
        True se removeu com sucesso, False caso contrário
    """
    try:
        if not usuario:
            raise FinanceiroError("Usuário não fornecido")
        
        # Para manter compatibilidade, vamos buscar o lançamento pelo índice
        # Primeiro, carregar todos os lançamentos
        df = carregar_dados(data_path, usuario)
        
        if df.empty or indice >= len(df):
            raise FinanceiroError("Índice inválido")
        
        # Buscar o ID do lançamento no banco
        with DatabaseManager() as db:
            user_data = db.get_user_by_name(usuario)
            if not user_data:
                raise FinanceiroError(f"Usuário '{usuario}' não encontrado")
            
            # Buscar todos os lançamentos ordenados por data (mais recente primeiro)
            lancamentos = db.filter_lancamentos(user_data['id'])
            
            if indice < len(lancamentos):
                lancamento_id = lancamentos.iloc[indice]['id']
                success = db.delete_lancamento(lancamento_id)
                
                if success:
                    logger.info(f"Lançamento {lancamento_id} removido com sucesso")
                    return True
                else:
                    raise FinanceiroError("Erro ao remover lançamento no banco")
            else:
                raise FinanceiroError("Índice inválido")
                
    except Exception as e:
        logger.error(f"Erro ao remover lançamento: {e}")
        raise FinanceiroError(f"Erro ao remover lançamento: {e}")

def editar_lancamento(indice: int, data: Union[str, datetime], descricao: str, 
                     categoria: str, tipo: str, valor: Union[str, float], data_path: Optional[str] = None,
                     usuario: Optional[str] = None) -> bool:
    """
    Edita um lançamento existente.
    
    Args:
        indice: Índice do lançamento
        data: Nova data do lançamento
        descricao: Nova descrição do lançamento
        categoria: Nova categoria do lançamento
        tipo: Novo tipo (Receita ou Despesa)
        valor: Novo valor do lançamento
        data_path: Caminho do arquivo (não usado, mantido para compatibilidade)
        usuario: Nome do usuário
        
    Returns:
        True se editou com sucesso, False caso contrário
    """
    try:
        if not usuario:
            raise FinanceiroError("Usuário não fornecido")
        
        # Validar dados
        is_valid, error_msg = validar_lancamento(data, descricao, categoria, tipo, valor)
        if not is_valid:
            raise FinanceiroError(error_msg)
        
        # Converter data para string se necessário
        if isinstance(data, datetime):
            data_str = data.strftime('%Y-%m-%d')
        else:
            data_str = str(data)
        
        # Converter valor para float
        valor_float = float(valor)
        
        with DatabaseManager() as db:
            user_data = db.get_user_by_name(usuario)
            if not user_data:
                raise FinanceiroError(f"Usuário '{usuario}' não encontrado")
            
            # Buscar todos os lançamentos ordenados por data (mais recente primeiro)
            lancamentos = db.filter_lancamentos(user_data['id'])
            
            if indice < len(lancamentos):
                lancamento_id = lancamentos.iloc[indice]['id']
                success = db.update_lancamento(
                    lancamento_id, data_str, descricao, categoria, tipo, valor_float
                )
                
                if success:
                    logger.info(f"Lançamento {lancamento_id} editado com sucesso")
                    return True
                else:
                    raise FinanceiroError("Erro ao editar lançamento no banco")
            else:
                raise FinanceiroError("Índice inválido")
                
    except Exception as e:
        logger.error(f"Erro ao editar lançamento: {e}")
        raise FinanceiroError(f"Erro ao editar lançamento: {e}")

def filtrar_por_categoria(categoria: str, data_path: Optional[str] = None, usuario: Optional[str] = None) -> pd.DataFrame:
    """
    Filtra lançamentos por categoria.
    
    Args:
        categoria: Categoria para filtrar
        data_path: Caminho do arquivo (não usado, mantido para compatibilidade)
        usuario: Nome do usuário
        
    Returns:
        DataFrame filtrado
    """
    try:
        if not usuario:
            return pd.DataFrame(columns=pd.Index(COLUNAS_PADRAO))
        
        with DatabaseManager() as db:
            user_data = db.get_user_by_name(usuario)
            if not user_data:
                return pd.DataFrame(columns=pd.Index(COLUNAS_PADRAO))
            
            df = db.filter_lancamentos(user_data['id'], categoria=categoria)
            
            # Renomear colunas para manter compatibilidade
            if not df.empty:
                df = df.rename(columns={
                    'data': 'Data',
                    'descricao': 'Descrição',
                    'categoria': 'Categoria',
                    'tipo': 'Tipo',
                    'valor': 'Valor'
                })
            
            return df
            
    except Exception as e:
        logger.error(f"Erro ao filtrar por categoria: {e}")
        return pd.DataFrame(columns=pd.Index(COLUNAS_PADRAO))

def buscar_por_periodo(data_inicio: Union[str, datetime], data_fim: Union[str, datetime], 
                      data_path: Optional[str] = None, usuario: Optional[str] = None) -> pd.DataFrame:
    """
    Busca lançamentos por período.
    
    Args:
        data_inicio: Data de início do período
        data_fim: Data de fim do período
        data_path: Caminho do arquivo (não usado, mantido para compatibilidade)
        usuario: Nome do usuário
        
    Returns:
        DataFrame filtrado
    """
    try:
        if not usuario:
            return pd.DataFrame(columns=pd.Index(COLUNAS_PADRAO))
        
        # Converter datas para string se necessário
        if isinstance(data_inicio, datetime):
            data_inicio_str = data_inicio.strftime('%Y-%m-%d')
        else:
            data_inicio_str = str(data_inicio)
        
        if isinstance(data_fim, datetime):
            data_fim_str = data_fim.strftime('%Y-%m-%d')
        else:
            data_fim_str = str(data_fim)
        
        with DatabaseManager() as db:
            user_data = db.get_user_by_name(usuario)
            if not user_data:
                return pd.DataFrame(columns=pd.Index(COLUNAS_PADRAO))
            
            df = db.filter_lancamentos(
                user_data['id'], 
                data_inicio=data_inicio_str, 
                data_fim=data_fim_str
            )
            
            # Renomear colunas para manter compatibilidade
            if not df.empty:
                df = df.rename(columns={
                    'data': 'Data',
                    'descricao': 'Descrição',
                    'categoria': 'Categoria',
                    'tipo': 'Tipo',
                    'valor': 'Valor'
                })
            
            return df
            
    except Exception as e:
        logger.error(f"Erro ao buscar por período: {e}")
        return pd.DataFrame(columns=pd.Index(COLUNAS_PADRAO))

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

