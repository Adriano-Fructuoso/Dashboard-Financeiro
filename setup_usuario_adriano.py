#!/usr/bin/env python3
"""
Script para configurar o usuário Adriano e seus dados no banco
Dashboard Financeiro - Setup de Produção
"""

import os
import sys
import pandas as pd
from datetime import datetime, timedelta
import hashlib

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import DatabaseManager
from config import SUPABASE_URL, SUPABASE_KEY

def criar_usuario_adriano():
    """Cria o usuário Adriano se não existir"""
    
    print("🔧 Configurando usuário Adriano...")
    
    db = DatabaseManager()
    
    # Verificar se o usuário já existe
    usuario = db.get_user_by_name('adriano')
    
    if usuario:
        print(f"✅ Usuário 'adriano' já existe (ID: {usuario['id']})")
        return usuario['id']
    else:
        # Criar usuário
        senha = "senha123"
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        
        try:
            if db.use_supabase and db.supabase_client:
                result = db.supabase_client.table('usuarios').insert({
                    'nome': 'adriano',
                    'senha_hash': senha_hash
                }).execute()
                
                if result.data:
                    user_id = result.data[0]['id']
                    print(f"✅ Usuário 'adriano' criado com sucesso (ID: {user_id})")
                    return user_id
                else:
                    print("❌ Erro ao criar usuário")
                    return None
            else:
                # Para PostgreSQL local
                query = "INSERT INTO usuarios (nome, senha_hash) VALUES (%s, %s) RETURNING id"
                result = db.execute_query(query, ('adriano', senha_hash))
                if result:
                    user_id = result[0]['id']
                    print(f"✅ Usuário 'adriano' criado com sucesso (ID: {user_id})")
                    return user_id
                else:
                    print("❌ Erro ao criar usuário")
                    return None
                    
        except Exception as e:
            print(f"❌ Erro ao criar usuário: {e}")
            return None

def gerar_dados_exemplo():
    """Gera dados de exemplo para o usuário Adriano"""
    
    print("📊 Gerando dados de exemplo...")
    
    # Dados de exemplo
    dados = [
        # Receitas
        {'data': '2025-01-15', 'descricao': 'Salário Janeiro', 'categoria': 'Salário', 'tipo': 'Receita', 'valor': 5000.00},
        {'data': '2025-01-20', 'descricao': 'Freelance Design', 'categoria': 'Freelance', 'tipo': 'Receita', 'valor': 800.00},
        {'data': '2025-02-15', 'descricao': 'Salário Fevereiro', 'categoria': 'Salário', 'tipo': 'Receita', 'valor': 5000.00},
        {'data': '2025-02-25', 'descricao': 'Dividendos', 'categoria': 'Investimentos', 'tipo': 'Receita', 'valor': 150.00},
        {'data': '2025-03-15', 'descricao': 'Salário Março', 'categoria': 'Salário', 'tipo': 'Receita', 'valor': 5000.00},
        {'data': '2025-03-28', 'descricao': 'Venda de equipamentos', 'categoria': 'Vendas', 'tipo': 'Receita', 'valor': 300.00},
        
        # Despesas
        {'data': '2025-01-05', 'descricao': 'Aluguel', 'categoria': 'Moradia', 'tipo': 'Despesa', 'valor': 1200.00},
        {'data': '2025-01-10', 'descricao': 'Supermercado', 'categoria': 'Alimentação', 'tipo': 'Despesa', 'valor': 450.00},
        {'data': '2025-01-12', 'descricao': 'Combustível', 'categoria': 'Transporte', 'tipo': 'Despesa', 'valor': 200.00},
        {'data': '2025-01-18', 'descricao': 'Academia', 'categoria': 'Saúde', 'tipo': 'Despesa', 'valor': 80.00},
        {'data': '2025-01-25', 'descricao': 'Cinema', 'categoria': 'Lazer', 'tipo': 'Despesa', 'valor': 60.00},
        {'data': '2025-02-05', 'descricao': 'Aluguel', 'categoria': 'Moradia', 'tipo': 'Despesa', 'valor': 1200.00},
        {'data': '2025-02-08', 'descricao': 'Supermercado', 'categoria': 'Alimentação', 'tipo': 'Despesa', 'valor': 380.00},
        {'data': '2025-02-15', 'descricao': 'Conta de luz', 'categoria': 'Contas', 'tipo': 'Despesa', 'valor': 120.00},
        {'data': '2025-02-20', 'descricao': 'Roupas', 'categoria': 'Vestuário', 'tipo': 'Despesa', 'valor': 250.00},
        {'data': '2025-02-28', 'descricao': 'Restaurante', 'categoria': 'Alimentação', 'tipo': 'Despesa', 'valor': 150.00},
        {'data': '2025-03-05', 'descricao': 'Aluguel', 'categoria': 'Moradia', 'tipo': 'Despesa', 'valor': 1200.00},
        {'data': '2025-03-10', 'descricao': 'Supermercado', 'categoria': 'Alimentação', 'tipo': 'Despesa', 'valor': 420.00},
        {'data': '2025-03-15', 'descricao': 'Combustível', 'categoria': 'Transporte', 'tipo': 'Despesa', 'valor': 180.00},
        {'data': '2025-03-20', 'descricao': 'Livros', 'categoria': 'Educação', 'tipo': 'Despesa', 'valor': 120.00},
        {'data': '2025-03-25', 'descricao': 'Bar com amigos', 'categoria': 'Lazer', 'tipo': 'Despesa', 'valor': 80.00},
    ]
    
    return dados

def inserir_dados_usuario(user_id: int):
    """Insere dados de exemplo para o usuário"""
    
    print(f"📝 Inserindo dados para usuário ID: {user_id}")
    
    db = DatabaseManager()
    dados = gerar_dados_exemplo()
    
    # Verificar se já existem dados
    lancamentos_existentes = db.get_lancamentos_by_user(user_id)
    
    if not lancamentos_existentes.empty:
        print(f"✅ Usuário já possui {len(lancamentos_existentes)} transações")
        return True
    
    # Inserir dados
    sucessos = 0
    for dado in dados:
        try:
            if db.use_supabase and db.supabase_client:
                result = db.supabase_client.table('transacoes').insert({
                    'usuario_id': user_id,
                    'data': dado['data'],
                    'descricao': dado['descricao'],
                    'categoria': dado['categoria'],
                    'tipo': dado['tipo'],
                    'valor': dado['valor']
                }).execute()
                
                if result.data:
                    sucessos += 1
            else:
                # Para PostgreSQL local
                query = """
                INSERT INTO transacoes (usuario_id, data, descricao, categoria, tipo, valor)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                db.execute_query(query, (
                    user_id, dado['data'], dado['descricao'], 
                    dado['categoria'], dado['tipo'], dado['valor']
                ))
                sucessos += 1
                
        except Exception as e:
            print(f"❌ Erro ao inserir transação: {e}")
    
    print(f"✅ {sucessos} transações inseridas com sucesso")
    return sucessos > 0

def main():
    """Função principal"""
    
    print("🚀 SETUP DO USUÁRIO ADRIANO - DASHBOARD FINANCEIRO")
    print("=" * 60)
    
    # Verificar configuração
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Configuração do Supabase não encontrada!")
        print("Configure as variáveis SUPABASE_URL e SUPABASE_KEY")
        return
    
    print(f"✅ Supabase configurado: {SUPABASE_URL}")
    
    try:
        # Criar usuário
        user_id = criar_usuario_adriano()
        
        if user_id:
            # Inserir dados
            inserir_dados_usuario(user_id)
            
            print("\n" + "=" * 60)
            print("🎉 SETUP CONCLUÍDO!")
            print("\n📋 CREDENCIAIS DE ACESSO:")
            print("👤 Usuário: adriano")
            print("🔑 Senha: senha123")
            print("\n🌐 Acesse: https://afinances.streamlit.app")
            
        else:
            print("❌ Erro ao criar usuário")
            
    except Exception as e:
        print(f"❌ Erro durante setup: {e}")

if __name__ == "__main__":
    main() 