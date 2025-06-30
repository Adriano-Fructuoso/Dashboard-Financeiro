""" 
Dashboard Financeiro Pessoal - Versão Otimizada
Interface moderna e eficiente para controle financeiro pessoal
"""

import streamlit as st
from finance.core import (
    carregar_dados, salvar_dados, adicionar_lancamento, listar_lancamentos,
    remover_lancamento, editar_lancamento, filtrar_por_categoria,
    buscar_por_periodo, calcular_somatorio_geral, calcular_somatorio_por_categoria,
    calcular_evolucao_mensal, comparar_meses, obter_top_categorias_mes, calcular_media_mensal
)
from finance.charts import grafico_despesas_por_categoria, grafico_receitas_por_categoria, grafico_saldo_ao_longo_do_tempo
import pandas as pd
import os
import json
from datetime import datetime, timedelta
from config import USE_GOOGLE_SHEETS, GOOGLE_SPREADSHEET_ID

# ==============================
# CONFIGURAÇÕES E CONSTANTES
# ==============================

# Configurações da página
PAGE_CONFIG = {
    "page_title": "Dashboard Financeiro",
    "page_icon": "💰",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Cores e temas
COLORS = {
    "primary": "#1f77b4",
    "success": "#2ecc71", 
    "warning": "#f39c12",
    "danger": "#e74c3c",
    "info": "#3498db",
    "light": "#ecf0f1",
    "dark": "#2c3e50"
}

# Categorias pré-definidas
CATEGORIAS = {
    "Receita": [
        "Salário", "Mesada", "Investimentos", "Venda de Bens",
        "Transferências Recebidas", "Outros Pagamentos Recebidos"
    ],
    "Despesa": [
        "Alimentação", "Moradia", "Comunicação", "Cartão de Crédito",
        "Educação", "Saúde", "Lazer & Diversão", "Transferências Enviadas",
        "Outros Pagamentos"
    ]
}

# ==============================
# FUNÇÕES AUXILIARES
# ==============================

def aplicar_css_personalizado():
    """Aplica CSS personalizado para melhorar a aparência"""
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .success-card {
        border-left-color: #2ecc71;
    }
    .warning-card {
        border-left-color: #f39c12;
    }
    .danger-card {
        border-left-color: #e74c3c;
    }
    .stButton > button {
        border-radius: 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    .grupo-card {
        display: inline-block;
        width: 180px;
        height: 120px;
        margin: 0 20px 30px 0;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        text-align: center;
        cursor: pointer;
        font-size: 1.2rem;
        font-weight: bold;
        transition: 0.2s;
        border: 3px solid transparent;
    }
    .grupo-card.selected {
        border: 3px solid #764ba2;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .grupo-card.receita {
        background: #eafaf1;
        color: #27ae60;
    }
    .grupo-card.despesa {
        background: #fbeee6;
        color: #e74c3c;
    }
    .grupo-card:hover {
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        transform: translateY(-2px) scale(1.04);
    }
    </style>
    """, unsafe_allow_html=True)

def criar_arquivo_inicial_usuario(usuario):
    """Cria arquivo CSV inicial para novo usuário ou aba no Google Sheets"""
    try:
        if USE_GOOGLE_SHEETS and GOOGLE_SPREADSHEET_ID:
            from utils.google_sheets import ensure_user_sheet_exists
            ensure_user_sheet_exists(GOOGLE_SPREADSHEET_ID, usuario)
            return True
        else:
            data_path = f"data/dados_{usuario}.csv"
            colunas = pd.Index(['Data', 'Descrição', 'Categoria', 'Tipo', 'Valor'])
            df_inicial = pd.DataFrame(columns=colunas)
            salvar_dados(df_inicial, data_path, usuario)
            return True
    except Exception as e:
        st.error(f"Erro ao criar arquivo inicial: {e}")
        return False

def carregar_usuarios():
    """Carrega usuários do arquivo JSON"""
    usuarios_path = "data/usuarios.json"
    if os.path.exists(usuarios_path):
        with open(usuarios_path, "r") as f:
            return json.load(f)
    else:
        usuarios_padrao = {"Adriano": "142536"}
        with open(usuarios_path, "w") as f:
            json.dump(usuarios_padrao, f)
        return usuarios_padrao

def salvar_usuarios(usuarios):
    """Salva usuários no arquivo JSON"""
    with open("data/usuarios.json", "w") as f:
        json.dump(usuarios, f)

def formatar_moeda(valor):
    """Formata valor como moeda brasileira"""
    return f"R$ {valor:,.2f}"

def criar_metric_card(label, value, delta=None, delta_color="normal"):
    """Cria um card de métrica personalizado"""
    color_class = ""
    if delta_color == "inverse":
        color_class = "danger-card"
    elif delta_color == "normal" and delta and delta > 0:
        color_class = "success-card"
    elif delta_color == "normal" and delta and delta < 0:
        color_class = "warning-card"
    
    st.markdown(f"""
    <div class="metric-card {color_class}">
        <h3 style="margin: 0; color: #2c3e50; font-size: 0.9rem;">{label}</h3>
        <h2 style="margin: 0.5rem 0; color: #1f77b4; font-size: 1.8rem;">{value}</h2>
        {f'<p style="margin: 0; color: {"#2ecc71" if delta > 0 else "#e74c3c"}; font-size: 0.8rem;">{delta}</p>' if delta else ''}
    </div>
    """, unsafe_allow_html=True)

# ==============================
# INTERFACE DE LOGIN
# ==============================

def mostrar_tela_login():
    """Exibe tela de login e cadastro de usuário"""
    st.title("🔐 Login no Dashboard Financeiro")
    aba = st.radio("Acesso", ["Entrar", "Criar Conta"], horizontal=True)

    if aba == "Entrar":
        usuario = st.text_input("Nome de usuário", key="login_usuario")
        if st.button("Entrar", use_container_width=True):
            if not usuario or not usuario.strip():
                st.warning("Digite um nome de usuário válido.")
                return
            # Tenta carregar dados da aba do usuário
            if USE_GOOGLE_SHEETS and GOOGLE_SPREADSHEET_ID:
                from utils.google_sheets import get_gspread_client
                try:
                    client = get_gspread_client()
                    spreadsheet = client.open_by_key(GOOGLE_SPREADSHEET_ID)
                    try:
                        spreadsheet.worksheet(usuario)
                        st.session_state["usuario_logado"] = usuario
                        st.success(f"Bem-vindo, {usuario}!")
                        st.rerun()
                    except Exception:
                        st.error("Usuário não encontrado. Faça o cadastro primeiro.")
                        return
                except Exception as e:
                    st.error(f"Erro ao acessar Google Sheets: {e}")
                    return
            else:
                # CSV: verifica se arquivo existe
                data_path = f"data/dados_{usuario}.csv"
                if os.path.exists(data_path):
                    st.session_state["usuario_logado"] = usuario
                    st.success(f"Bem-vindo, {usuario}!")
                    st.rerun()
                else:
                    st.error("Usuário não encontrado. Faça o cadastro primeiro.")
                    return
    else:
        usuario = st.text_input("Nome de usuário para cadastro", key="cadastro_usuario")
        if st.button("Criar Conta", use_container_width=True):
            if not usuario or not usuario.strip():
                st.warning("Digite um nome de usuário válido.")
                return
            # Verifica se já existe aba/usuário
            if USE_GOOGLE_SHEETS and GOOGLE_SPREADSHEET_ID:
                from utils.google_sheets import get_gspread_client
                try:
                    client = get_gspread_client()
                    spreadsheet = client.open_by_key(GOOGLE_SPREADSHEET_ID)
                    try:
                        spreadsheet.worksheet(usuario)
                        st.error("Usuário já existe. Escolha outro nome.")
                        return
                    except Exception:
                        # Não existe, pode criar
                        criado = criar_arquivo_inicial_usuario(usuario)
                        if criado:
                            st.success(f"Conta criada para {usuario}! Faça login para acessar.")
                        else:
                            st.error("Erro ao criar conta. Tente novamente.")
                except Exception as e:
                    st.error(f"Erro ao acessar Google Sheets: {e}")
                    return
            else:
                # CSV: verifica se arquivo existe
                data_path = f"data/dados_{usuario}.csv"
                if os.path.exists(data_path):
                    st.error("Usuário já existe. Escolha outro nome.")
                    return
                criado = criar_arquivo_inicial_usuario(usuario)
                if criado:
                    st.success(f"Conta criada para {usuario}! Faça login para acessar.")
                else:
                    st.error("Erro ao criar conta. Tente novamente.")

# ==============================
# DASHBOARD PRINCIPAL
# ==============================

def inicializar_dashboard():
    """Inicializa o dashboard com configurações básicas"""
    st.set_page_config(
        page_title="Dashboard Financeiro",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    aplicar_css_personalizado()
    
    # Header principal - só exibe se o usuário estiver logado
    if "usuario_logado" in st.session_state:
        st.markdown(f"""
        <div class="main-header">
            <h1>💰 Dashboard Financeiro Pessoal</h1>
            <p>Bem-vindo, <strong>{st.session_state['usuario_logado']}</strong>! 💪</p>
        </div>
        """, unsafe_allow_html=True)

def mostrar_sidebar():
    """Configura e exibe a sidebar"""
    with st.sidebar:
        st.markdown("### 🧭 Navegação")
        menu = st.selectbox(
            "Escolha uma seção:",
            ["📊 Resumo", "➕ Novo Lançamento", "📈 Relatórios Mensais", "📋 Gerenciar Dados"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("🔄 Atualizar Dados", use_container_width=True):
            sincronizar_dados()
            st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 Sair", use_container_width=True):
            # Limpar completamente a session_state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    return menu

def sincronizar_dados():
    """Sincroniza dados da session_state com arquivo CSV ou Google Sheets"""
    try:
        usuario = st.session_state["usuario_logado"]
        
        if USE_GOOGLE_SHEETS and GOOGLE_SPREADSHEET_ID:
            df_atual = carregar_dados(usuario=usuario)
        else:
            data_path = f"data/dados_{usuario}.csv"
            df_atual = carregar_dados(data_path, usuario)
        
        st.session_state['df_dados'] = df_atual
        st.success("✅ Dados atualizados!")
        return True
    except Exception as e:
        st.error(f"Erro na sincronização: {e}")
        return False

def mostrar_resumo():
    """Exibe a página de resumo"""
    st.header("📊 Resumo Financeiro")
    
    df = st.session_state['df_dados']
    
    if len(df) > 0:
        df['Categoria'] = df['Categoria'].astype('category')
        df['Tipo'] = df['Tipo'].astype('category')
    
    # Métricas principais
    somatorio = calcular_somatorio_geral(df)
    total_investimentos = float(df[df['Categoria'] == 'Investimentos']['Valor'].sum())
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        criar_metric_card("💰 Receitas", formatar_moeda(somatorio['receitas']))
    
    with col2:
        criar_metric_card("💸 Despesas", formatar_moeda(somatorio['despesas']))
    
    with col3:
        saldo_color = "normal" if somatorio['saldo'] >= 0 else "inverse"
        criar_metric_card("💳 Saldo", formatar_moeda(somatorio['saldo']), delta_color=saldo_color)
    
    with col4:
        criar_metric_card("📈 Investimentos", formatar_moeda(total_investimentos))
    
    # Filtros e visualização de dados
    mostrar_filtros_e_dados(df)
    
    # Gráficos
    if len(df) > 0:
        mostrar_graficos(df)

def mostrar_filtros_e_dados(df):
    """Exibe filtros e tabela de dados"""
    st.markdown("---")
    st.subheader("📅 Filtros e Visualização")
    
    # Filtros em colunas
    col1, col2 = st.columns([1, 1])
    
    with col1:
        periodo = st.selectbox(
            "📅 Período:",
            ["Todos os dados", "Último mês", "Últimos 3 meses", "Últimos 6 meses", "Este ano", "Período personalizado"]
        )
    
    with col2:
        if len(df) > 0:
            meses_disponiveis = sorted(df['Data'].dt.to_period('M').unique(), reverse=True)
            meses_opcoes = [str(mes) for mes in meses_disponiveis]
            meses_opcoes.insert(0, "Todos os meses")
            mes_selecionado = st.selectbox("📆 Mês específico:", meses_opcoes)
        else:
            mes_selecionado = "Todos os meses"
    
    # Aplicar filtros
    df_filtrado = aplicar_filtros(df, periodo, mes_selecionado)
    
    # Exibir dados
    if len(df_filtrado) > 0:
        st.dataframe(
            formatar_dataframe_exibicao(df_filtrado),
            use_container_width=True,
            hide_index=True
        )
        
        # Ações CRUD
        mostrar_acoes_crud(df_filtrado)
    else:
        st.info("📝 Nenhum lançamento encontrado. Adicione novos lançamentos para começar!")

def aplicar_filtros(df, periodo, mes_selecionado):
    """Aplica filtros temporais aos dados"""
    if len(df) == 0:
        return df
    
    data_min = df['Data'].min()
    data_max = df['Data'].max()
    
    # Aplicar filtro de período
    if periodo == "Período personalizado":
        col1, col2 = st.columns([1, 1])
        with col1:
            data_inicio = st.date_input("Data de início", data_min)
        with col2:
            data_fim = st.date_input("Data de fim", data_max)
    elif periodo == "Último mês":
        data_fim = data_max
        data_inicio = data_fim - pd.DateOffset(months=1)
    elif periodo == "Últimos 3 meses":
        data_fim = data_max
        data_inicio = data_fim - pd.DateOffset(months=3)
    elif periodo == "Últimos 6 meses":
        data_fim = data_max
        data_inicio = data_fim - pd.DateOffset(months=6)
    elif periodo == "Este ano":
        data_inicio = pd.Timestamp(data_max.year, 1, 1)
        data_fim = data_max
    else:  # Todos os dados
        data_inicio = data_min
        data_fim = data_max
    
    df_filtrado = df[(df['Data'] >= data_inicio) & (df['Data'] <= data_fim)]
    
    # Aplicar filtro de mês específico
    if mes_selecionado != "Todos os meses":
        mes_periodo = pd.Period(mes_selecionado)
        df_filtrado = df_filtrado[df_filtrado['Data'].dt.to_period('M') == mes_periodo]
    
    return df_filtrado

def formatar_dataframe_exibicao(df):
    """Formata DataFrame para exibição"""
    df_exibir = df.copy()
    if len(df_exibir) > 0:
        df_exibir['Valor'] = df_exibir['Valor'].apply(formatar_moeda)
        df_exibir['Data'] = pd.to_datetime(df_exibir['Data']).dt.strftime('%d/%m/%Y')
    return df_exibir

def mostrar_acoes_crud(df):
    """Exibe ações CRUD para os dados"""
    st.subheader("🔧 Ações")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("✏️ Editar Lançamento", use_container_width=True):
            st.session_state['modo_edicao'] = True
    
    with col2:
        if st.button("🗑️ Excluir Lançamento", use_container_width=True):
            st.session_state['modo_exclusao'] = True
    
    with col3:
        if st.button("🔄 Atualizar Dados", use_container_width=True):
            sincronizar_dados()
            st.success("✅ Dados atualizados!")
            st.rerun()
    
    # Interface de edição
    if st.session_state.get('modo_edicao', False):
        mostrar_interface_edicao(df)
    
    # Interface de exclusão
    if st.session_state.get('modo_exclusao', False):
        mostrar_interface_exclusao(df)

def mostrar_interface_edicao(df):
    """Exibe interface para editar lançamento"""
    st.subheader("✏️ Editar Lançamento")
    
    if 'indice_edicao' not in st.session_state:
        indices = list(range(len(df)))
        indice = st.selectbox("Selecione o lançamento para editar:", indices, format_func=lambda x: f"{x+1} - {df.iloc[x]['Descrição']} ({df.iloc[x]['Data'].strftime('%d/%m/%Y')})")
        st.session_state['indice_edicao'] = indice
    
    if 'indice_edicao' in st.session_state:
        indice = st.session_state['indice_edicao']
        lancamento = df.iloc[indice]
        
        with st.form("form_edicao"):
            col1, col2 = st.columns([1, 1])
            with col1:
                data = st.date_input("📅 Data", value=lancamento['Data'].date())
                if isinstance(data, datetime):
                    data_lanc = data
                else:
                    data_lanc = datetime.combine(data, datetime.min.time())
                descricao = st.text_input("📝 Descrição", value=lancamento['Descrição'])
            with col2:
                categoria = st.selectbox("🏷️ Categoria", CATEGORIAS[lancamento['Tipo']], index=CATEGORIAS[lancamento['Tipo']].index(lancamento['Categoria']))
                valor = st.number_input("💰 Valor", min_value=0.0, step=0.01, value=float(lancamento['Valor']))
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.form_submit_button("💾 Salvar Alterações", use_container_width=True):
                    if descricao and descricao.strip():  # Validar que descrição não está vazia
                        usuario = st.session_state["usuario_logado"]
                        data_path = f"data/dados_{usuario}.csv"
                        editar_lancamento(indice, data_lanc, descricao, categoria, lancamento['Tipo'], valor, data_path, usuario)
                        sincronizar_dados()
                        st.success("✅ Lançamento editado com sucesso!")
                        del st.session_state['modo_edicao']
                        del st.session_state['indice_edicao']
                        st.rerun()
                    else:
                        st.warning("⚠️ A descrição não pode estar vazia")
            with col2:
                if st.form_submit_button("❌ Cancelar", use_container_width=True):
                    del st.session_state['modo_edicao']
                    del st.session_state['indice_edicao']
                    st.rerun()

def mostrar_interface_exclusao(df):
    """Exibe interface para excluir lançamento"""
    st.subheader("🗑️ Excluir Lançamento")
    
    if 'indice_exclusao' not in st.session_state:
        indices = list(range(len(df)))
        indice = st.selectbox("Selecione o lançamento para excluir:", indices, format_func=lambda x: f"{x+1} - {df.iloc[x]['Descrição']} ({df.iloc[x]['Data'].strftime('%d/%m/%Y')})")
        st.session_state['indice_exclusao'] = indice
    
    if 'indice_exclusao' in st.session_state:
        indice = st.session_state['indice_exclusao']
        lancamento = df.iloc[indice]
        
        st.warning(f"⚠️ Tem certeza que deseja excluir o lançamento: **{lancamento['Descrição']}** ({lancamento['Data'].strftime('%d/%m/%Y')})?")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("✅ Confirmar Exclusão", use_container_width=True):
                usuario = st.session_state["usuario_logado"]
                data_path = f"data/dados_{usuario}.csv"
                remover_lancamento(indice, data_path, usuario)
                sincronizar_dados()
                st.success("✅ Lançamento excluído com sucesso!")
                del st.session_state['modo_exclusao']
                del st.session_state['indice_exclusao']
                st.rerun()
        with col2:
            if st.button("❌ Cancelar", use_container_width=True):
                del st.session_state['modo_exclusao']
                del st.session_state['indice_exclusao']
                st.rerun()

def mostrar_graficos(df):
    """Exibe gráficos de análise"""
    st.markdown("---")
    st.subheader("📈 Análise Visual")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**💰 Receitas por Categoria**")
        fig_receitas = grafico_receitas_por_categoria(df)
        st.pyplot(fig_receitas, use_container_width=True)
    
    with col2:
        st.markdown("**💸 Despesas por Categoria**")
        fig_despesas = grafico_despesas_por_categoria(df)
        st.pyplot(fig_despesas, use_container_width=True)
    
    # Gráfico de saldo ao longo do tempo
    st.markdown("**📊 Evolução do Saldo**")
    fig_saldo = grafico_saldo_ao_longo_do_tempo(df)
    st.pyplot(fig_saldo, use_container_width=True)

def mostrar_novo_lancamento():
    """Exibe interface para adicionar novo lançamento"""
    st.header("➕ Novo Lançamento")
    
    # Seleção do grupo (Receita/Despesa)
    if 'grupo_lancamento' not in st.session_state:
        st.session_state['grupo_lancamento'] = None
    
    grupo = st.session_state['grupo_lancamento']
    
    if grupo is None:
        st.info("Selecione o tipo de lançamento:")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("💰 Receita", use_container_width=True, type="primary"):
                st.session_state['grupo_lancamento'] = 'Receita'
                st.rerun()
        with col2:
            if st.button("💸 Despesa", use_container_width=True, type="secondary"):
                st.session_state['grupo_lancamento'] = 'Despesa'
                st.rerun()
    elif grupo in CATEGORIAS:
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; background-color: {'#d4edda' if grupo=='Receita' else '#f8d7da'}; 
                    border-radius: 10px; margin-bottom: 20px;">
            <h3 style="margin: 0; color: {'#155724' if grupo=='Receita' else '#721c24'};">
            {'💰' if grupo=='Receita' else '💸'} {grupo}
        </div>
        """, unsafe_allow_html=True)
        with st.form("form_novo_lancamento"):
            col1, col2 = st.columns([1, 1])
            with col1:
                data = st.date_input("📅 Data", value=datetime.now())
                if isinstance(data, datetime):
                    data_lanc = data
                else:
                    data_lanc = datetime.combine(data, datetime.min.time())
                descricao = st.text_input("📝 Descrição")
            with col2:
                categoria = st.selectbox("🏷️ Categoria", CATEGORIAS[grupo], key="categoria_lancamento")
                valor = st.number_input("💰 Valor", min_value=0.0, step=0.01, help="Digite o valor do lançamento")
            if st.form_submit_button("➕ Adicionar Lançamento", use_container_width=True):
                if descricao and valor > 0 and categoria:
                    usuario = st.session_state["usuario_logado"]
                    data_path = f"data/dados_{usuario}.csv"
                    adicionar_lancamento(data_lanc, descricao, categoria, grupo, valor, data_path, usuario)
                    sincronizar_dados()
                    st.success("✅ Lançamento adicionado com sucesso!")
                    st.session_state['grupo_lancamento'] = None
                else:
                    st.warning("⚠️ Preencha todos os campos obrigatórios")
    else:
        st.info("Selecione primeiro se é Receita ou Despesa para continuar.")

def mostrar_relatorios_mensais():
    """Exibe relatórios mensais"""
    st.header("📈 Relatórios Mensais")
    
    df = st.session_state['df_dados']
    
    if len(df) == 0:
        st.info("📝 Adicione lançamentos para ver os relatórios mensais.")
        return
    
    # Preparar dados
    df['Ano'] = df['Data'].dt.year
    df['Mes'] = df['Data'].dt.month
    df['Mes_Ano'] = df['Data'].dt.to_period('M')
    
    meses_disponiveis = sorted(df['Mes_Ano'].unique(), reverse=True)
    
    # Comparativo mensal
    st.subheader("📊 Comparativo Mensal")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        mes1 = st.selectbox("Primeiro mês:", meses_disponiveis, format_func=lambda x: str(x))
    
    with col2:
        mes2 = st.selectbox("Segundo mês:", meses_disponiveis, format_func=lambda x: str(x))
    
    # Exibir comparação
    comparacao = None
    if mes1 is not None and mes2 is not None:
        comparacao = comparar_meses(df, mes1, mes2)
    
    if comparacao:
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            criar_metric_card(
                f"Receitas {mes1}",
                formatar_moeda(comparacao['mes1']['receitas']),
                f"R$ {comparacao['diferenca']['receitas']:,.2f}" if mes1 != mes2 else None
            )
        
        with col2:
            criar_metric_card(
                f"Despesas {mes1}",
                formatar_moeda(comparacao['mes1']['despesas']),
                f"R$ {comparacao['diferenca']['despesas']:,.2f}" if mes1 != mes2 else None
            )
        
        with col3:
            criar_metric_card(
                f"Saldo {mes1}",
                formatar_moeda(comparacao['mes1']['saldo']),
                f"R$ {comparacao['diferenca']['saldo']:,.2f}" if mes1 != mes2 else None
            )
    
    # Evolução mensal
    st.subheader("📈 Evolução dos Últimos 6 Meses")
    
    df_evolucao = calcular_evolucao_mensal(df, 6)
    
    if len(df_evolucao) > 0:
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(12, 6))
        x = range(len(df_evolucao))
        
        ax.plot(x, df_evolucao['Receitas'], marker='o', label='Receitas', linewidth=2, color='#2ecc71')
        ax.plot(x, df_evolucao['Despesas'], marker='s', label='Despesas', linewidth=2, color='#e74c3c')
        ax.plot(x, df_evolucao['Saldo'], marker='^', label='Saldo', linewidth=2, color='#3498db')
        
        ax.set_xlabel('Mês')
        ax.set_ylabel('Valor (R$)')
        ax.set_title('Evolução Financeira Mensal')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xticks(x)
        ax.set_xticklabels(df_evolucao['Mes'], rotation=45)
        
        st.pyplot(fig)
        
        # Médias mensais
        medias = calcular_media_mensal(df, 6)
        if medias:
            st.subheader("📊 Médias dos Últimos 6 Meses")
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                criar_metric_card("Receitas Média", formatar_moeda(medias['receitas_media']))
            with col2:
                criar_metric_card("Despesas Média", formatar_moeda(medias['despesas_media']))
            with col3:
                criar_metric_card("Saldo Média", formatar_moeda(medias['saldo_media']))

def mostrar_gerenciar_dados():
    """Exibe interface para gerenciar dados"""
    st.header("📋 Gerenciar Dados")
    
    df = st.session_state['df_dados']
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Estatísticas")
        if len(df) > 0:
            st.metric("Total de Lançamentos", len(df))
            st.metric("Primeiro Lançamento", df['Data'].min().strftime('%d/%m/%Y'))
            st.metric("Último Lançamento", df['Data'].max().strftime('%d/%m/%Y'))
            st.metric("Categorias Únicas", df['Categoria'].nunique())
        else:
            st.info("Nenhum dado disponível")
    
    with col2:
        st.subheader("🔧 Ações")
        
        if st.button("📥 Exportar Dados (CSV)", use_container_width=True):
            csv = df.to_csv(index=False)
            st.download_button(
                label="💾 Download CSV",
                data=csv,
                file_name=f"dados_financeiros_{st.session_state['usuario_logado']}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        if st.button("🗑️ Limpar Todos os Dados", use_container_width=True):
            if st.checkbox("Confirmo que quero apagar todos os dados"):
                usuario = st.session_state["usuario_logado"]
                data_path = f"data/dados_{usuario}.csv"
                df_vazio = pd.DataFrame(columns=pd.Index(['Data', 'Descrição', 'Categoria', 'Tipo', 'Valor']))
                salvar_dados(df_vazio, data_path, usuario)
                sincronizar_dados()
                st.success("✅ Todos os dados foram removidos!")
                st.rerun()

# ==============================
# FLUXO PRINCIPAL
# ==============================

def main():
    """Função principal do aplicativo"""
    # Verificar login primeiro
    if "usuario_logado" not in st.session_state:
        mostrar_tela_login()
        return  # Importante: retorna aqui para não executar o resto
    
    # Só inicializa o dashboard se o usuário estiver logado
    inicializar_dashboard()
    
    # Configurar sidebar e obter menu selecionado
    menu = mostrar_sidebar()
    
    # Verificar se precisa recarregar dados
    usuario_atual = st.session_state["usuario_logado"]
    
    # Se não há dados ou se o usuário mudou, recarregar
    if ('df_dados' not in st.session_state or 
        'usuario_anterior' not in st.session_state or 
        st.session_state['usuario_anterior'] != usuario_atual):
        
        try:
            if USE_GOOGLE_SHEETS and GOOGLE_SPREADSHEET_ID:
                st.session_state['df_dados'] = carregar_dados(usuario=usuario_atual)
            else:
                data_path = f"data/dados_{usuario_atual}.csv"
                st.session_state['df_dados'] = carregar_dados(data_path, usuario_atual)
            
            # Marcar o usuário atual para evitar recargas desnecessárias
            st.session_state['usuario_anterior'] = usuario_atual
            
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
            st.session_state['df_dados'] = pd.DataFrame(columns=pd.Index(['Data', 'Descrição', 'Categoria', 'Tipo', 'Valor']))
    
    # Navegar para a página selecionada
    if menu == "📊 Resumo":
        mostrar_resumo()
    elif menu == "➕ Novo Lançamento":
        mostrar_novo_lancamento()
    elif menu == "📈 Relatórios Mensais":
        mostrar_relatorios_mensais()
    elif menu == "📋 Gerenciar Dados":
        mostrar_gerenciar_dados()

if __name__ == "__main__":
    main()