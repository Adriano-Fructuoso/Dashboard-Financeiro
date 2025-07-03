#!/usr/bin/env python3
"""
Script para testar múltiplos usuários - adiciona 10 lançamentos em cada aba
"""

import pandas as pd
import os
from datetime import datetime, timedelta
import random
from utils.google_sheets import read_sheet_as_dataframe, write_dataframe_to_sheet, ensure_user_sheet_exists

def gerar_lancamentos_teste(usuario, quantidade=10):
    """Gera lançamentos de teste para um usuário específico"""
    
    # Categorias de teste
    categorias_receita = ["Salário", "Freelance", "Investimentos", "Venda de Bens", "Mesada"]
    categorias_despesa = ["Alimentação", "Moradia", "Educação", "Lazer & Diversão", "Transporte", "Saúde"]
    
    # Descrições de teste
    descricoes_receita = [
        f"Salário {usuario}", f"Freela {usuario}", f"Dividendos {usuario}", 
        f"Venda {usuario}", f"Mesada {usuario}", f"Bônus {usuario}"
    ]
    
    descricoes_despesa = [
        f"Almoço {usuario}", f"Aluguel {usuario}", f"Faculdade {usuario}", 
        f"Cinema {usuario}", f"Uber {usuario}", f"Farmácia {usuario}",
        f"Supermercado {usuario}", f"Academia {usuario}", f"Netflix {usuario}"
    ]
    
    lancamentos = []
    
    # Gerar datas dos últimos 30 dias
    data_final = datetime.now()
    data_inicial = data_final - timedelta(days=30)
    
    for i in range(quantidade):
        # Data aleatória nos últimos 30 dias
        dias_aleatorios = random.randint(0, 30)
        data = data_inicial + timedelta(days=dias_aleatorios)
        
        # Decidir se é receita ou despesa (60% despesa, 40% receita)
        if random.random() < 0.6:
            tipo = "Despesa"
            categoria = random.choice(categorias_despesa)
            descricao = random.choice(descricoes_despesa)
            valor = round(random.uniform(10, 500), 2)
        else:
            tipo = "Receita"
            categoria = random.choice(categorias_receita)
            descricao = random.choice(descricoes_receita)
            valor = round(random.uniform(100, 5000), 2)
        
        lancamento = {
            "Data": data.strftime("%Y-%m-%d"),
            "Descrição": f"{descricao} #{i+1}",
            "Categoria": categoria,
            "Tipo": tipo,
            "Valor": valor
        }
        
        lancamentos.append(lancamento)
    
    return lancamentos

def testar_usuario(usuario, quantidade=10):
    """Testa adicionar lançamentos para um usuário específico"""
    
    spreadsheet_id = os.getenv('GOOGLE_SPREADSHEET_ID', '')
    if not spreadsheet_id:
        print(f"❌ Erro: GOOGLE_SPREADSHEET_ID não configurado")
        return False
    
    try:
        print(f"\n👤 Testando usuário: {usuario}")
        print("-" * 40)
        
        # Garantir que a aba existe
        ensure_user_sheet_exists(spreadsheet_id, usuario)
        print(f"✅ Aba '{usuario}' verificada")
        
        # Ler dados existentes
        df_existente = read_sheet_as_dataframe(spreadsheet_id, usuario)
        registros_antes = len(df_existente)
        print(f"📊 Registros existentes: {registros_antes}")
        
        # Gerar novos lançamentos
        lancamentos_novos = gerar_lancamentos_teste(usuario, quantidade)
        df_novos = pd.DataFrame(lancamentos_novos)
        
        # Converter Data para datetime
        df_novos['Data'] = pd.to_datetime(df_novos['Data'])
        
        # Combinar dados existentes com novos dados
        if len(df_existente) > 0:
            df_combinado = pd.concat([df_existente, df_novos], ignore_index=True)
            # Remover duplicatas baseadas em Data, Descrição e Valor
            df_combinado = df_combinado.drop_duplicates(subset=['Data', 'Descrição', 'Valor'], keep='first')
        else:
            df_combinado = df_novos
        
        # Salvar na planilha
        write_dataframe_to_sheet(df_combinado, spreadsheet_id, usuario)
        
        registros_depois = len(df_combinado)
        novos_adicionados = registros_depois - registros_antes
        
        print(f"✅ {novos_adicionados} novos lançamentos adicionados")
        print(f"📈 Total de registros: {registros_depois}")
        
        # Mostrar alguns exemplos dos novos lançamentos
        print(f"📋 Exemplos dos novos lançamentos:")
        for i, lancamento in enumerate(lancamentos_novos[:3]):
            print(f"   {i+1}. {lancamento['Data']} - {lancamento['Descrição']} ({lancamento['Tipo']}) - R$ {lancamento['Valor']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar usuário {usuario}: {e}")
        return False

def main():
    """Função principal para testar múltiplos usuários"""
    
    # Lista de usuários para testar
    usuarios_teste = ["Teste2", "teste3", "teste4", "Blabla", "João", "Maria", "Pedro"]
    
    print("🧪 Iniciando teste de múltiplos usuários...")
    print("=" * 60)
    
    resultados = {}
    
    for usuario in usuarios_teste:
        sucesso = testar_usuario(usuario, quantidade=10)
        resultados[usuario] = sucesso
    
    # Resumo dos resultados
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    sucessos = sum(resultados.values())
    total = len(resultados)
    
    for usuario, sucesso in resultados.items():
        status = "✅ SUCESSO" if sucesso else "❌ FALHOU"
        print(f"👤 {usuario:10} - {status}")
    
    print(f"\n📈 Resultado: {sucessos}/{total} usuários testados com sucesso")
    
    if sucessos == total:
        print("🎉 Todos os testes passaram! Sistema funcionando perfeitamente.")
    else:
        print("⚠️ Alguns testes falharam. Verifique os logs acima.")
    
    print(f"\n🔗 Acesse a planilha: https://docs.google.com/spreadsheets/d/{os.getenv('GOOGLE_SPREADSHEET_ID')}")

if __name__ == "__main__":
    main() 