"""
Gerenciador de Banco de Dados - PostgreSQL/Supabase
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor, RealDictRow
import pandas as pd
from typing import Optional, List, Dict, Any, Union
import logging
from datetime import datetime
import hashlib
from supabase import create_client, Client

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gerenciador de conexão e operações com banco de dados"""
    
    def __init__(self):
        self.connection = None
        self.supabase_client = None
        self.use_supabase = False
        self.connect()
    
    def connect(self):
        """Estabelece conexão com o banco de dados"""
        try:
            # Importar configurações do config.py
            from config import get_supabase_config
            
            # Obter configurações atualizadas
            config = get_supabase_config()
            SUPABASE_URL = config['SUPABASE_URL']
            SUPABASE_KEY = config['SUPABASE_KEY']
            
            # Tentar conectar via Supabase primeiro
            if SUPABASE_URL and SUPABASE_KEY:
                self.supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
                self.use_supabase = True
                logger.info("Conectado ao Supabase via cliente oficial")
                return
            
            # Tentar conectar via DATABASE_URL (para PostgreSQL local)
            database_url = os.getenv('DATABASE_URL')
            if database_url:
                self.connection = psycopg2.connect(database_url)
                logger.info("Conectado ao banco via DATABASE_URL")
                return
            
            # Fallback para variáveis individuais
            host = os.getenv('DB_HOST', 'localhost')
            port = os.getenv('DB_PORT', '5432')
            database = os.getenv('DB_NAME', 'dashboard_financeiro')
            user = os.getenv('DB_USER', 'postgres')
            password = os.getenv('DB_PASSWORD', '')
            
            self.connection = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
            logger.info("Conectado ao banco via variáveis individuais")
            
        except Exception as e:
            logger.error(f"Erro ao conectar ao banco: {e}")
            raise
    
    def disconnect(self):
        """Fecha a conexão com o banco"""
        if self.connection:
            self.connection.close()
            logger.info("Conexão com banco fechada")
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Executa uma query e retorna os resultados como lista de dicionários"""
        if self.use_supabase and self.supabase_client:
            # Para Supabase, usar o cliente oficial
            try:
                # Executar query via Supabase
                result = self.supabase_client.rpc('exec_sql', {'query': query, 'params': params or ()})
                return result.data if hasattr(result, 'data') and result.data else []
            except Exception as e:
                logger.error(f"Erro ao executar query no Supabase: {e}")
                raise
        else:
            # Para PostgreSQL local
            if not self.connection:
                raise Exception("Conexão com banco não estabelecida")
                
            try:
                with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query, params)
                    if query.strip().upper().startswith('SELECT'):
                        result = cursor.fetchall()
                        # Converter RealDictRow para dict
                        return [dict(row) for row in result]
                    else:
                        self.connection.commit()
                        return []
            except Exception as e:
                logger.error(f"Erro ao executar query: {e}")
                if self.connection:
                    self.connection.rollback()
                raise
    
    def get_user_by_name(self, nome: str) -> Optional[Dict[str, Any]]:
        """Busca usuário pelo nome"""
        if self.use_supabase and self.supabase_client:
            try:
                result = self.supabase_client.table('usuarios').select('*').eq('nome', nome).execute()
                return result.data[0] if result.data else None
            except Exception as e:
                logger.error(f"Erro ao buscar usuário no Supabase: {e}")
                return None
        else:
            query = "SELECT * FROM usuarios WHERE nome = %s"
            result = self.execute_query(query, (nome,))
            return result[0] if result else None
    
    def create_user(self, nome: str, senha: str) -> bool:
        """Cria um novo usuário"""
        try:
            # Hash da senha
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            
            if self.use_supabase and self.supabase_client:
                result = self.supabase_client.table('usuarios').insert({
                    'nome': nome,
                    'senha_hash': senha_hash
                }).execute()
                success = len(result.data) > 0
            else:
                query = "INSERT INTO usuarios (nome, senha_hash) VALUES (%s, %s)"
                self.execute_query(query, (nome, senha_hash))
                success = True
            
            if success:
                logger.info(f"Usuário '{nome}' criado com sucesso")
                return True
            else:
                logger.error(f"Erro ao criar usuário '{nome}'")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {e}")
            return False
    
    def verify_user_password(self, nome: str, senha: str) -> bool:
        """Verifica se a senha do usuário está correta"""
        try:
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            
            if self.use_supabase and self.supabase_client:
                result = self.supabase_client.table('usuarios').select('id').eq('nome', nome).eq('senha_hash', senha_hash).execute()
                return len(result.data) > 0
            else:
                query = "SELECT id FROM usuarios WHERE nome = %s AND senha_hash = %s"
                result = self.execute_query(query, (nome, senha_hash))
                return len(result) > 0
                
        except Exception as e:
            logger.error(f"Erro ao verificar senha: {e}")
            return False
    
    def get_lancamentos_by_user(self, usuario_id: int) -> pd.DataFrame:
        """Busca todos os lançamentos de um usuário"""
        if self.use_supabase and self.supabase_client:
            try:
                result = self.supabase_client.table('transacoes').select('data,descricao,categoria,tipo,valor').eq('usuario_id', usuario_id).order('data', desc=True).execute()
                
                if result.data:
                    df = pd.DataFrame(result.data)
                    df['data'] = pd.to_datetime(df['data'])
                    return df
                else:
                    return pd.DataFrame(columns=pd.Index(['data', 'descricao', 'categoria', 'tipo', 'valor']))
            except Exception as e:
                logger.error(f"Erro ao buscar transações no Supabase: {e}")
                return pd.DataFrame(columns=pd.Index(['data', 'descricao', 'categoria', 'tipo', 'valor']))
        else:
            query = """
            SELECT data, descricao, categoria, tipo, valor 
            FROM transacoes 
            WHERE usuario_id = %s 
            ORDER BY data DESC
            """
            result = self.execute_query(query, (usuario_id,))
            
            if result:
                df = pd.DataFrame(result)
                df['data'] = pd.to_datetime(df['data'])
                return df
            else:
                return pd.DataFrame(columns=pd.Index(['data', 'descricao', 'categoria', 'tipo', 'valor']))
    
    def add_lancamento(self, usuario_id: int, data: str, descricao: str, 
                      categoria: str, tipo: str, valor: float) -> bool:
        """Adiciona um novo lançamento"""
        try:
            if self.use_supabase and self.supabase_client:
                result = self.supabase_client.table('transacoes').insert({
                    'usuario_id': usuario_id,
                    'data': data,
                    'descricao': descricao,
                    'categoria': categoria,
                    'tipo': tipo,
                    'valor': valor
                }).execute()
                success = len(result.data) > 0
            else:
                query = """
                INSERT INTO transacoes (usuario_id, data, descricao, categoria, tipo, valor)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                self.execute_query(query, (usuario_id, data, descricao, categoria, tipo, valor))
                success = True
            
            if success:
                logger.info(f"Transação adicionada para usuário {usuario_id}")
                return True
            else:
                logger.error(f"Erro ao adicionar transação para usuário {usuario_id}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao adicionar transação: {e}")
            return False
    
    def update_lancamento(self, lancamento_id: int, data: str, descricao: str,
                         categoria: str, tipo: str, valor: float) -> bool:
        """Atualiza um lançamento existente"""
        try:
            if self.use_supabase and self.supabase_client:
                result = self.supabase_client.table('transacoes').update({
                    'data': data,
                    'descricao': descricao,
                    'categoria': categoria,
                    'tipo': tipo,
                    'valor': valor
                }).eq('id', lancamento_id).execute()
                success = len(result.data) > 0
            else:
                query = """
                UPDATE transacoes 
                SET data = %s, descricao = %s, categoria = %s, tipo = %s, valor = %s
                WHERE id = %s
                """
                self.execute_query(query, (data, descricao, categoria, tipo, valor, lancamento_id))
                success = True
            
            if success:
                logger.info(f"Transação {lancamento_id} atualizada")
                return True
            else:
                logger.error(f"Erro ao atualizar transação {lancamento_id}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao atualizar transação: {e}")
            return False
    
    def delete_lancamento(self, lancamento_id: int) -> bool:
        """Remove um lançamento"""
        try:
            if self.use_supabase and self.supabase_client:
                result = self.supabase_client.table('transacoes').delete().eq('id', lancamento_id).execute()
                success = len(result.data) > 0
            else:
                query = "DELETE FROM transacoes WHERE id = %s"
                self.execute_query(query, (lancamento_id,))
                success = True
            
            if success:
                logger.info(f"Transação {lancamento_id} removida")
                return True
            else:
                logger.error(f"Erro ao remover transação {lancamento_id}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao remover transação: {e}")
            return False
    
    def get_lancamento_by_id(self, lancamento_id: int) -> Optional[Dict[str, Any]]:
        """Busca um lançamento específico pelo ID"""
        if self.use_supabase and self.supabase_client:
            try:
                result = self.supabase_client.table('transacoes').select('*').eq('id', lancamento_id).execute()
                return result.data[0] if result.data else None
            except Exception as e:
                logger.error(f"Erro ao buscar transação no Supabase: {e}")
                return None
        else:
            query = "SELECT * FROM transacoes WHERE id = %s"
            result = self.execute_query(query, (lancamento_id,))
            return result[0] if result else None
    
    def filter_lancamentos(self, usuario_id: int, data_inicio: Optional[str] = None, 
                          data_fim: Optional[str] = None, categoria: Optional[str] = None, 
                          tipo: Optional[str] = None) -> pd.DataFrame:
        """Filtra lançamentos por critérios"""
        if self.use_supabase and self.supabase_client:
            try:
                query = self.supabase_client.table('transacoes').select('*').eq('usuario_id', usuario_id)
                
                if data_inicio:
                    query = query.gte('data', data_inicio)
                if data_fim:
                    query = query.lte('data', data_fim)
                if categoria:
                    query = query.eq('categoria', categoria)
                if tipo:
                    query = query.eq('tipo', tipo)
                
                result = query.order('data', desc=True).execute()
                
                if result.data:
                    df = pd.DataFrame(result.data)
                    df['data'] = pd.to_datetime(df['data'])
                    return df
                else:
                    return pd.DataFrame(columns=pd.Index(['data', 'descricao', 'categoria', 'tipo', 'valor']))
            except Exception as e:
                logger.error(f"Erro ao filtrar transações no Supabase: {e}")
                return pd.DataFrame(columns=pd.Index(['data', 'descricao', 'categoria', 'tipo', 'valor']))
        else:
            query = "SELECT * FROM transacoes WHERE usuario_id = %s"
            params: List[Union[int, str]] = [usuario_id]
            
            if data_inicio:
                query += " AND data >= %s"
                params.append(data_inicio)
            
            if data_fim:
                query += " AND data <= %s"
                params.append(data_fim)
            
            if categoria:
                query += " AND categoria = %s"
                params.append(categoria)
            
            if tipo:
                query += " AND tipo = %s"
                params.append(tipo)
            
            query += " ORDER BY data DESC"
            
            result = self.execute_query(query, tuple(params))
            
            if result:
                df = pd.DataFrame(result)
                df['data'] = pd.to_datetime(df['data'])
                return df
            else:
                return pd.DataFrame(columns=pd.Index(['data', 'descricao', 'categoria', 'tipo', 'valor']))
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect() 