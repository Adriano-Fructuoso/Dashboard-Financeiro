"""
Módulo Charts - Visualizações do Dashboard Financeiro
Versão Otimizada - Gráficos Modernos e Atraentes
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Optional
import seaborn as sns
from matplotlib.figure import Figure

# Configurar estilo dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Cores personalizadas
CORES = {
    'receitas': '#2ecc71',
    'despesas': '#e74c3c',
    'saldo': '#3498db',
    'investimentos': '#f39c12',
    'background': '#f8f9fa',
    'grid': '#e9ecef'
}

def configurar_estilo_grafico():
    """Configura o estilo padrão dos gráficos"""
    plt.rcParams['figure.facecolor'] = CORES['background']
    plt.rcParams['axes.facecolor'] = CORES['background']
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
    plt.rcParams['grid.color'] = CORES['grid']
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10

def grafico_despesas_por_categoria(df: pd.DataFrame) -> Figure:
    """
    Gera um gráfico de pizza moderno mostrando o total de despesas por categoria.
    
    Args:
        df: DataFrame com os dados
        
    Returns:
        Figura matplotlib pronta para exibição
    """
    configurar_estilo_grafico()
    
    despesas = df[df['Tipo'] == 'Despesa']
    
    if despesas.empty:
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.text(0.5, 0.5, 'Nenhuma despesa registrada\nAdicione despesas para ver o gráfico', 
                ha='center', va='center', transform=ax.transAxes, 
                fontsize=16, color='gray', weight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Despesas por Categoria', fontsize=18, weight='bold', pad=20)
        return fig
    
    # Agrupar e calcular totais
    categorias = despesas.groupby('Categoria')['Valor'].sum()
    categorias = categorias[categorias > 0.0]
    
    if len(categorias) == 0:
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.text(0.5, 0.5, 'Nenhuma despesa válida encontrada', 
                ha='center', va='center', transform=ax.transAxes, 
                fontsize=16, color='gray', weight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Despesas por Categoria', fontsize=18, weight='bold', pad=20)
        return fig
    
    # Ordenar por valor
    categorias = categorias.sort_values(ascending=False)
    valor_total = categorias.sum()
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Cores do gráfico
    cores = plt.cm.viridis(np.linspace(0, 1, len(categorias)))
    
    # Criar gráfico de pizza
    wedges, texts, autotexts = ax.pie(
        categorias.values,
        labels=categorias.index.tolist(),
        autopct=lambda pct: f"{pct:.1f}%\nR$ {pct * valor_total / 100:,.0f}" if pct > 5 else '',
        startangle=90,
        colors=cores,
        textprops={'fontsize': 11, 'weight': 'bold'},
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )
    
    # Configurar texto das porcentagens
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_weight('bold')
    
    # Título
    ax.set_title(f'Despesas por Categoria\nTotal: R$ {valor_total:,.2f}', 
                fontsize=18, weight='bold', pad=20)
    
    # Adicionar legenda
    ax.legend(wedges, [f"{cat}: R$ {val:,.2f}" for cat, val in categorias.items()],
             title="Categorias", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.tight_layout()
    return fig

def grafico_receitas_por_categoria(df: pd.DataFrame) -> Figure:
    """
    Gera um gráfico de pizza moderno mostrando o total de receitas por categoria.
    
    Args:
        df: DataFrame com os dados
        
    Returns:
        Figura matplotlib pronta para exibição
    """
    configurar_estilo_grafico()
    
    receitas = df[df['Tipo'] == 'Receita']
    
    if receitas.empty:
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.text(0.5, 0.5, 'Nenhuma receita registrada\nAdicione receitas para ver o gráfico', 
                ha='center', va='center', transform=ax.transAxes, 
                fontsize=16, color='gray', weight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Receitas por Categoria', fontsize=18, weight='bold', pad=20)
        return fig
    
    # Agrupar e calcular totais
    categorias = receitas.groupby('Categoria')['Valor'].sum()
    categorias = categorias[categorias > 0.0]
    
    if len(categorias) == 0:
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.text(0.5, 0.5, 'Nenhuma receita válida encontrada', 
                ha='center', va='center', transform=ax.transAxes, 
                fontsize=16, color='gray', weight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Receitas por Categoria', fontsize=18, weight='bold', pad=20)
        return fig
    
    # Ordenar por valor
    categorias = categorias.sort_values(ascending=False)
    valor_total = categorias.sum()
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Cores do gráfico
    cores = plt.cm.plasma(np.linspace(0, 1, len(categorias)))
    
    # Criar gráfico de pizza
    wedges, texts, autotexts = ax.pie(
        categorias.values,
        labels=categorias.index.tolist(),
        autopct=lambda pct: f"{pct:.1f}%\nR$ {pct * valor_total / 100:,.0f}" if pct > 5 else '',
        startangle=90,
        colors=cores,
        textprops={'fontsize': 11, 'weight': 'bold'},
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )
    
    # Configurar texto das porcentagens
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_weight('bold')
    
    # Título
    ax.set_title(f'Receitas por Categoria\nTotal: R$ {valor_total:,.2f}', 
                fontsize=18, weight='bold', pad=20)
    
    # Adicionar legenda
    ax.legend(wedges, [f"{cat}: R$ {val:,.2f}" for cat, val in categorias.items()],
             title="Categorias", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.tight_layout()
    return fig

def grafico_saldo_ao_longo_do_tempo(df: pd.DataFrame) -> Figure:
    """
    Gera um gráfico de linha moderno mostrando o saldo acumulado ao longo do tempo.
    
    Args:
        df: DataFrame com os dados
        
    Returns:
        Figura matplotlib pronta para exibição
    """
    configurar_estilo_grafico()
    
    if df.empty:
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.text(0.5, 0.5, 'Nenhum lançamento registrado\nAdicione lançamentos para ver o gráfico', 
                ha='center', va='center', transform=ax.transAxes, 
                fontsize=16, color='gray', weight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Evolução do Saldo ao Longo do Tempo', fontsize=18, weight='bold', pad=20)
        return fig
    
    # Preparar dados
    df_sorted = df.sort_values('Data').copy()
    df_sorted['Valor Ajustado'] = df_sorted.apply(
        lambda row: row['Valor'] if row['Tipo'] == 'Receita' else -row['Valor'],
        axis=1
    )
    df_sorted['Saldo Acumulado'] = df_sorted['Valor Ajustado'].cumsum()
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Gráfico principal
    ax.plot(df_sorted['Data'], df_sorted['Saldo Acumulado'], 
            marker='o', linewidth=3, markersize=6, color=CORES['saldo'], 
            label='Saldo Acumulado')
    
    # Adicionar linha horizontal em y=0
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.7, linewidth=1)
    
    # Configurar eixos
    ax.set_xlabel('Data', fontsize=12, weight='bold')
    ax.set_ylabel('Saldo Acumulado (R$)', fontsize=12, weight='bold')
    ax.set_title('Evolução do Saldo ao Longo do Tempo', fontsize=18, weight='bold', pad=20)
    
    # Rotacionar labels do eixo x
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    
    # Grid
    ax.grid(True, alpha=0.3)
    
    # Adicionar anotações para pontos importantes
    saldo_atual = df_sorted['Saldo Acumulado'].iloc[-1]
    ax.annotate(f'Saldo Atual: R$ {saldo_atual:,.2f}', 
                xy=(df_sorted['Data'].iloc[-1], saldo_atual),
                xytext=(10, 10), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    # Configurar layout
    plt.tight_layout()
    return fig

def grafico_evolucao_mensal(df: pd.DataFrame, meses: int = 6) -> plt.Figure:
    """
    Gera um gráfico de barras empilhadas mostrando a evolução mensal.
    
    Args:
        df: DataFrame com os dados
        meses: Número de meses para analisar
        
    Returns:
        Figura matplotlib pronta para exibição
    """
    configurar_estilo_grafico()
    
    if df.empty:
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.text(0.5, 0.5, 'Nenhum lançamento registrado\nAdicione lançamentos para ver o gráfico', 
                ha='center', va='center', transform=ax.transAxes, 
                fontsize=16, color='gray', weight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Evolução Mensal', fontsize=18, weight='bold', pad=20)
        return fig
    
    # Preparar dados mensais
    df_copy = df.copy()
    df_copy['Mes_Ano'] = df_copy['Data'].dt.to_period('M')
    
    # Obter últimos N meses
    meses_unicos = sorted(df_copy['Mes_Ano'].unique(), reverse=True)[:meses]
    
    if not meses_unicos:
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.text(0.5, 0.5, 'Dados insuficientes para análise mensal', 
                ha='center', va='center', transform=ax.transAxes, 
                fontsize=16, color='gray', weight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Evolução Mensal', fontsize=18, weight='bold', pad=20)
        return fig
    
    # Calcular dados para cada mês
    dados_mensais = []
    for mes in reversed(meses_unicos):  # Ordem cronológica
        dados_mes = df_copy[df_copy['Mes_Ano'] == mes]
        receitas = dados_mes[dados_mes['Tipo'] == 'Receita']['Valor'].sum()
        despesas = dados_mes[dados_mes['Tipo'] == 'Despesa']['Valor'].sum()
        dados_mensais.append({
            'Mes': str(mes),
            'Receitas': receitas,
            'Despesas': despesas,
            'Saldo': receitas - despesas
        })
    
    df_mensal = pd.DataFrame(dados_mensais)
    
    # Criar figura
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
    
    # Gráfico 1: Receitas vs Despesas
    x = range(len(df_mensal))
    width = 0.35
    
    bars1 = ax1.bar([i - width/2 for i in x], df_mensal['Receitas'], width, 
                    label='Receitas', color=CORES['receitas'], alpha=0.8)
    bars2 = ax1.bar([i + width/2 for i in x], df_mensal['Despesas'], width, 
                    label='Despesas', color=CORES['despesas'], alpha=0.8)
    
    ax1.set_xlabel('Mês', fontsize=12, weight='bold')
    ax1.set_ylabel('Valor (R$)', fontsize=12, weight='bold')
    ax1.set_title('Receitas vs Despesas por Mês', fontsize=16, weight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(df_mensal['Mes'], rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Adicionar valores nas barras
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'R$ {height:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'R$ {height:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    # Gráfico 2: Saldo mensal
    bars3 = ax2.bar(x, df_mensal['Saldo'], color=[CORES['receitas'] if s >= 0 else CORES['despesas'] for s in df_mensal['Saldo']], alpha=0.8)
    
    ax2.set_xlabel('Mês', fontsize=12, weight='bold')
    ax2.set_ylabel('Saldo (R$)', fontsize=12, weight='bold')
    ax2.set_title('Saldo Mensal', fontsize=16, weight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(df_mensal['Mes'], rotation=45)
    ax2.axhline(y=0, color='red', linestyle='--', alpha=0.7)
    ax2.grid(True, alpha=0.3)
    
    # Adicionar valores nas barras
    for bar in bars3:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'R$ {height:,.0f}', ha='center', va='bottom' if height >= 0 else 'top', fontweight='bold')
    
    plt.tight_layout()
    return fig

def grafico_distribuicao_categorias(df: pd.DataFrame) -> plt.Figure:
    """
    Gera um gráfico de barras horizontais mostrando a distribuição por categoria.
    
    Args:
        df: DataFrame com os dados
        
    Returns:
        Figura matplotlib pronta para exibição
    """
    configurar_estilo_grafico()
    
    if df.empty:
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.text(0.5, 0.5, 'Nenhum lançamento registrado\nAdicione lançamentos para ver o gráfico', 
                ha='center', va='center', transform=ax.transAxes, 
                fontsize=16, color='gray', weight='bold')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Distribuição por Categoria', fontsize=18, weight='bold', pad=20)
        return fig
    
    # Preparar dados
    receitas = df[df['Tipo'] == 'Receita'].groupby('Categoria')['Valor'].sum().sort_values(ascending=True)
    despesas = df[df['Tipo'] == 'Despesa'].groupby('Categoria')['Valor'].sum().sort_values(ascending=True)
    
    # Criar figura
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
    
    # Gráfico de receitas
    if not receitas.empty:
        bars1 = ax1.barh(range(len(receitas)), receitas, color=CORES['receitas'], alpha=0.8)
        ax1.set_yticks(range(len(receitas)))
        ax1.set_yticklabels(receitas.index)
        ax1.set_xlabel('Valor (R$)', fontsize=12, weight='bold')
        ax1.set_title('Receitas por Categoria', fontsize=16, weight='bold')
        ax1.grid(True, alpha=0.3, axis='x')
        
        # Adicionar valores nas barras
        for i, bar in enumerate(bars1):
            width = bar.get_width()
            ax1.text(width, bar.get_y() + bar.get_height()/2,
                    f'R$ {width:,.0f}', ha='left', va='center', fontweight='bold')
    else:
        ax1.text(0.5, 0.5, 'Nenhuma receita registrada', 
                ha='center', va='center', transform=ax1.transAxes, 
                fontsize=14, color='gray')
        ax1.set_title('Receitas por Categoria', fontsize=16, weight='bold')
    
    # Gráfico de despesas
    if not despesas.empty:
        bars2 = ax2.barh(range(len(despesas)), despesas, color=CORES['despesas'], alpha=0.8)
        ax2.set_yticks(range(len(despesas)))
        ax2.set_yticklabels(despesas.index)
        ax2.set_xlabel('Valor (R$)', fontsize=12, weight='bold')
        ax2.set_title('Despesas por Categoria', fontsize=16, weight='bold')
        ax2.grid(True, alpha=0.3, axis='x')
        
        # Adicionar valores nas barras
        for i, bar in enumerate(bars2):
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height()/2,
                    f'R$ {width:,.0f}', ha='left', va='center', fontweight='bold')
    else:
        ax2.text(0.5, 0.5, 'Nenhuma despesa registrada', 
                ha='center', va='center', transform=ax2.transAxes, 
                fontsize=14, color='gray')
        ax2.set_title('Despesas por Categoria', fontsize=16, weight='bold')
    
    plt.tight_layout()
    return fig
