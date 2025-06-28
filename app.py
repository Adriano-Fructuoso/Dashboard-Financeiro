""" app.py
	•	O que vai aqui:
O ponto de entrada da aplicação Streamlit.
	•	Responsabilidades:
	•	Montar a interface do dashboard (usando streamlit).
	•	Chamar funções que vêm da pasta finance/ para manipular e exibir os dados.
	•	Exibir tabelas, gráficos e formulários para o usuário interagir.
	•	Não deve ter lógica pesada, só orquestra o que está vindo de outros arquivos.
	•	Exemplo:
	•	Recebe dados de finance/core.py
	•	Monta gráficos usando funções de finance/charts.py """

# app.py

import streamlit as st
from finance.core import (
    carregar_dados,
    salvar_dados,
    adicionar_lancamento,
    listar_lancamentos,
    remover_lancamento,
    editar_lancamento,
    filtrar_por_categoria,
    buscar_por_periodo,
    calcular_somatorio_geral,
    calcular_somatorio_por_categoria
)
from finance.charts import grafico_despesas_por_categoria, grafico_receitas_por_categoria, grafico_saldo_ao_longo_do_tempo
import pandas as pd
from streamlit import column_config
import os
import json

# ==============================
# INÍCIO DO DASHBOARD FINANCEIRO
# ==============================

# Título e introdução
st.title("Dashboard Financeiro Pessoal")
st.write("Bem-vindo! Use o menu ao lado para navegar pelo seu financeiro.")

# Sidebar para navegação e formulário de novos lançamentos
menu = st.sidebar.selectbox("Selecione uma opção:", ["Resumo", "Novo Lançamento", "Relatórios"])

# --- LOGIN SIMPLES ---
USUARIOS_PATH = "data/usuarios.json"
# Carregar usuários do arquivo, se existir
if os.path.exists(USUARIOS_PATH):
    with open(USUARIOS_PATH, "r") as f:
        USUARIOS = json.load(f)
else:
    USUARIOS = {"Adriano": "142536"}
    with open(USUARIOS_PATH, "w") as f:
        json.dump(USUARIOS, f)

if "usuario_logado" not in st.session_state:
    st.title("Login")
    aba = st.radio("Escolha uma opção:", ["Entrar", "Criar nova conta"])
    if aba == "Entrar":
        usuario = st.text_input("Nome de usuário")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if usuario and senha:
                if usuario in USUARIOS and senha == USUARIOS[usuario]:
                    st.session_state["usuario_logado"] = usuario
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos")
            else:
                st.warning("Preencha usuário e senha.")
        st.stop()
    else:
        novo_usuario = st.text_input("Novo nome de usuário")
        nova_senha = st.text_input("Nova senha", type="password")
        if st.button("Criar conta"):
            if not novo_usuario or not nova_senha:
                st.warning("Preencha usuário e senha.")
            elif novo_usuario in USUARIOS:
                st.error("Usuário já existe!")
            else:
                USUARIOS[novo_usuario] = nova_senha
                with open(USUARIOS_PATH, "w") as f:
                    json.dump(USUARIOS, f)
                st.session_state["usuario_logado"] = novo_usuario
                st.success("Conta criada e login realizado!")
                st.rerun()
        st.stop()

usuario = st.session_state["usuario_logado"]
DATA_PATH = f"data/dados_{usuario}.csv"

if menu == "Resumo":
    st.header("Resumo Financeiro")
    
    # Carrega os dados
    df = carregar_dados(DATA_PATH)
    
    # Garantir que as colunas de filtro sejam categóricas
    df['Categoria'] = df['Categoria'].astype('category')
    df['Tipo'] = df['Tipo'].astype('category')
    
    # Calcula o somatório geral
    somatorio = calcular_somatorio_geral(df)
    
    # Calcula o total da categoria 'Investimentos'
    total_investimentos = float(df[df['Categoria'] == 'Investimentos']['Valor'].sum())
    
    # Exibe o somatório geral em cards
    st.subheader("📊 Resumo Geral")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="💰 Total de Receitas",
            value=f"R$ {somatorio['receitas']:,.2f}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="💸 Total de Despesas",
            value=f"R$ {somatorio['despesas']:,.2f}",
            delta=None
        )
    
    with col3:
        saldo_color = "normal" if somatorio['saldo'] >= 0 else "inverse"
        st.metric(
            label="💳 Saldo",
            value=f"R$ {somatorio['saldo']:,.2f}",
            delta=None,
            delta_color=saldo_color
        )
    
    # Linha separada para investimentos
    st.markdown("")
    col_inv = st.columns(1)
    with col_inv[0]:
        st.metric(
            label="📈 Investimentos",
            value=f"R$ {total_investimentos:,.2f}",
            delta=None
        )
    
    # Botão para mostrar/ocultar filtro de categoria
    if st.button("Filtrar categoria"):
        if st.session_state.get('filtro_categoria_aberto', False):
            st.session_state['filtro_categoria_aberto'] = False
        else:
            st.session_state['filtro_categoria_aberto'] = True

    if st.session_state.get('filtro_categoria_aberto', False):
        categorias_unicas = sorted(df['Categoria'].unique())
        # Estado para selecionar todas
        if 'todas_categorias_selecionadas' not in st.session_state:
            st.session_state['todas_categorias_selecionadas'] = True
        if st.button(
            "Selecionar todas" if not st.session_state['todas_categorias_selecionadas'] else "Desmarcar todas",
            key='btn_todas_categorias'):
            st.session_state['todas_categorias_selecionadas'] = not st.session_state['todas_categorias_selecionadas']
            st.rerun()
        if st.session_state['todas_categorias_selecionadas']:
            categorias_selecionadas = st.multiselect(
                "Selecione as categorias:",
                options=categorias_unicas,
                default=categorias_unicas,
                key='multiselect_categorias'
            )
        else:
            categorias_selecionadas = st.multiselect(
                "Selecione as categorias:",
                options=categorias_unicas,
                default=[],
                key='multiselect_categorias'
            )
        if not categorias_selecionadas:
            categorias_selecionadas = categorias_unicas  # Se nada selecionado, mostra tudo
    else:
        categorias_selecionadas = sorted(df['Categoria'].unique())

    df_filtrado = df[df['Categoria'].isin(categorias_selecionadas)]

    # Formatar valores numéricos e datas para exibição
    df_exibir = pd.DataFrame(df_filtrado)
    if 'Valor' in df_exibir.columns:
        df_exibir['Valor'] = df_exibir['Valor'].apply(lambda x: f"R$ {x:,.2f}")
    if 'Data' in df_exibir.columns:
        df_exibir['Data'] = pd.to_datetime(df_exibir['Data']).dt.strftime('%d/%m/%Y')
    df_exibir = df_exibir.rename(columns={
        "Data": "Data",
        "Descrição": "Descrição",
        "Categoria": "Categoria",
        "Tipo": "Tipo",
        "Valor": "Valor"
    })
    st.subheader("📋 Todos os Lançamentos")
    st.dataframe(
        df_exibir,
        use_container_width=True,
        hide_index=True
    )

    # --- Exclusão ---
    if st.button("🗑️ Excluir lançamento"):
        if st.session_state.get('excluir_aberto', False):
            st.session_state['excluir_aberto'] = False
        else:
            st.session_state['excluir_aberto'] = True

    if st.session_state.get('excluir_aberto', False) and len(df) > 0:
        opcoes_excluir = [
            f"{str(row['Data'])[:10]} | {row['Descrição']} | {row['Categoria']} | {row['Tipo']} | R$ {row['Valor']:,.2f}"
            for _, row in df.reset_index().iterrows()
        ]
        idx_excluir = st.selectbox(
            "Selecione um lançamento para excluir:",
            options=range(len(opcoes_excluir)),
            format_func=lambda i: opcoes_excluir[i],
            key='excluir_idx'
        )
        if st.button("Confirmar exclusão", key='confirmar_excluir'):
            remover_lancamento(idx_excluir, DATA_PATH)
            st.success("Lançamento excluído!")
            del st.session_state['excluir_aberto']
            st.rerun()

    # --- Edição ---
    if st.button("✏️ Editar lançamento"):
        if st.session_state.get('editar_aberto', False):
            st.session_state['editar_aberto'] = False
            if 'editar_idx' in st.session_state:
                del st.session_state['editar_idx']
        else:
            st.session_state['editar_aberto'] = True

    if st.session_state.get('editar_aberto', False) and len(df) > 0:
        opcoes_edit = [
            f"{str(row['Data'])[:10]} | {row['Descrição']} | {row['Categoria']} | {row['Tipo']} | R$ {row['Valor']:,.2f}"
            for _, row in df.reset_index().iterrows()
        ]
        idx_edit = st.selectbox(
            "Selecione um lançamento para editar:",
            options=range(len(opcoes_edit)),
            format_func=lambda i: opcoes_edit[i],
            key='editar_idx_selectbox'
        )
        if st.button("Editar este lançamento", key="confirmar_editar"):
            st.session_state['editar_idx'] = idx_edit

    # Formulário de edição
    if st.session_state.get('editar_aberto', False) and 'editar_idx' in st.session_state:
        editar_idx = st.session_state['editar_idx']
        row = df.iloc[editar_idx]
        st.markdown("---")
        st.subheader("Editar lançamento")
        with st.form("form_editar_lancamento"):
            data_edit = st.date_input("Data", pd.to_datetime(row['Data']))
            descricao_edit = st.text_input("Descrição", row['Descrição'])
            categoria_edit = st.text_input("Categoria", row['Categoria'])
            tipo_edit = st.selectbox("Tipo", ["Receita", "Despesa"], index=0 if row['Tipo']=="Receita" else 1)
            valor_edit = st.number_input("Valor", min_value=0.0, step=0.01, value=float(row['Valor']))
            submit_edit = st.form_submit_button("Salvar alterações")
            if submit_edit:
                editar_lancamento(editar_idx, data_edit, descricao_edit, categoria_edit, tipo_edit, valor_edit, DATA_PATH)
                st.success("Lançamento editado com sucesso!")
                del st.session_state['editar_aberto']
                del st.session_state['editar_idx']
                st.rerun()
    
    # Gráficos um abaixo do outro, ocupando toda a largura
    st.subheader("📈 Análise por Categoria")
    st.write("**Receitas por categoria**")
    fig_receitas = grafico_receitas_por_categoria(df)
    st.pyplot(fig_receitas, use_container_width=True)
    st.write("**Despesas por categoria**")
    fig_despesas = grafico_despesas_por_categoria(df)
    st.pyplot(fig_despesas, use_container_width=True)

elif menu == "Novo Lançamento":
    st.header("Adicionar novo lançamento")

    # Listas fixas de categorias por tipo
    categorias_receita = [
        "Salário",
        "Mesada",
        "Investimentos",
        "Venda de Bens",
        "Transferências Recebidas",
        "Outros Pagamentos Recebidos"
    ]
    categorias_despesa = [
        "Alimentação",
        "Moradia",
        "Comunicação",
        "Cartão de Crédito",
        "Educação",
        "Saúde",
        "Lazer & Diversão",
        "Transferências Enviadas",
        "Outros Pagamentos"
    ]

    # Campo Tipo fora do form para atualização dinâmica
    tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
    if tipo == "Receita":
        categorias = categorias_receita
    else:
        categorias = categorias_despesa

    with st.form("form_lancamento"):
        data = st.date_input("Data")
        descricao = st.text_input("Descrição")
        categoria = st.selectbox("Categoria", categorias)
        valor = st.number_input("Valor", min_value=0.0, step=0.01)
        submit = st.form_submit_button("Adicionar")
        if submit:
            adicionar_lancamento(data, descricao, categoria, tipo, valor, DATA_PATH)
            st.success("Lançamento adicionado!")

elif menu == "Relatórios":
    st.header("Relatórios avançados (em breve)")
    # Aqui podem entrar gráficos de saldo, metas, exportações, etc.

# ==============================
# FIM DO DASHBOARD
# ==============================

# Observações:
# - Toda lógica pesada fica em finance/core.py (salvar, carregar, filtrar dados).
# - Toda lógica de gráficos fica em finance/charts.py.
# - O app.py apenas chama essas funções e monta a interface.