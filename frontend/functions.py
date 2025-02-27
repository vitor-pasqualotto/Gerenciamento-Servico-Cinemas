import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"

# ============ LOGIN ============

def login():
    st.sidebar.header("Login")
    email = st.sidebar.text_input("Email")
    senha = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Entrar"):
        data = {"username": email, "password": senha}
        response = requests.post(f"{API_BASE_URL}/token", data=data)
        if response.status_code == 200:
            st.session_state.token = response.json().get("access_token")
            st.sidebar.success("Login efetuado com sucesso!")
        else:
            st.sidebar.error("Erro no login. Verifique suas credenciais.")

def get_current_user():
    token = st.session_state.get("token")
    if not token:
        return None
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/usuarios/me", headers=headers)
    if response.status_code == 200:
        return response.json()
    return None 

# ============ AÇÕES DISPONÍVEIS ============
# READ
def show_usuarios(): 
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE_URL}/usuarios/", headers=headers)

        if response.status_code == 200:
            registros = response.json()
            st.write("- Lista de Usuários")
            st.table(registros)

        else:
            st.error("Erro ao buscar serviços.")

    else:
        st.error("Usuário não autenticado.")

def show_empresas(): 
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE_URL}/empresas/", headers=headers)

        if response.status_code == 200:
            registros = response.json()
            st.write("- Lista de Empresas")
            st.table(registros)

        else:
            st.error("Erro ao buscar serviços.")

    else:
        st.error("Usuário não autenticado.")

def show_cinemas(): 
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE_URL}/cinemas/", headers=headers)

        if response.status_code == 200:
            registros = response.json()
            st.write("- Lista de Cinemas")
            st.table(registros)

        else:
            st.error("Erro ao buscar serviços.")

    else:
        st.error("Usuário não autenticado.")

def show_salas():
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE_URL}/salas/", headers=headers)

        if response.status_code == 200:
            registros = response.json()
            st.write("- Lista de Salas")
            st.table(registros)

        else:
            st.error("Erro ao buscar serviços.")

    else:
        st.error("Usuário não autenticado.")

def show_servicos(): 
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE_URL}/salas/", headers=headers)

        if response.status_code == 200:
            registros = response.json()
            st.write("- Lista de Salas")
            st.table(registros)

        else:
            st.error("Erro ao buscar serviços.")

    else:
        st.error("Usuário não autenticado.")

def show_historico_status(): 
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE_URL}/historico_status/", headers=headers)

        if response.status_code == 200:
            registros = response.json()
            st.write("- Lista de Salas")
            st.table(registros)

        else:
            st.error("Erro ao buscar serviços.")

    else:
        st.error("Usuário não autenticado.")

# CREATE
def create_usuario():
    token = st.session_state.get("token")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
        }

    # Recuperando todas as empresas para adicionar do dropdown
    response = requests.get(f"{API_BASE_URL}/empresas/", headers=headers)
    if response.status_code == 200:
        empresas = response.json()
        dict_empresas = {empresa['id']: empresa['nome'] for empresa in empresas}
        options_empresa = []
        for id, nome in dict_empresas.items():
            options_empresa.append(nome)

    # Recuperando todas os cinemas da empresa selecionada

    options_tipo = ["Gerente", "Representante", "Encarregado"]

    st.header("Registrar Novo Usuário")
    nome_usuario = st.text_input("Nome do Usuário")
    email = st.text_input("Email Usuário")
    senha = st.text_input("Senha Usuário", type='password')
    tipo_usuario = st.selectbox("Tipo de Usuário", options=options_tipo)

    if tipo_usuario == "Encarregado":
        empresa = None
        cinema = None

    elif tipo_usuario == "Representante":
        empresa = st.selectbox("Empresa", options=options_empresa)

        if empresa:
            # Setando ID da empresa selecionada
            for id, nome in dict_empresas.items():
                if nome == empresa:
                    empresa = id
                    st.write(empresa)
        cinema = None

    else:
        empresa = st.selectbox("Empresa", options=options_empresa)

        if empresa:
            # Setando ID da empresa selecionada
            for id, nome in dict_empresas.items():
                if nome == empresa:
                    empresa = id
                    st.write(empresa)

            # Recuperando todas os cinemas da empresa selecionada
            response = requests.get(f"{API_BASE_URL}/cinemas/", headers=headers)
            if response.status_code == 200:
                cinemas = response.json()
                dict_cinemas = {cinema['id']: cinema['nome'] for cinema in cinemas if cinema['empresa_id'] == empresa}
                options_cinema = []
                for id, nome in dict_cinemas.items():
                    options_cinema.append(nome) 

            cinema = st.selectbox("Cinema", options=options_cinema)

        if cinema:
            # Setando ID da empresa selecionada
            for id, nome in dict_cinemas.items():
                if nome == cinema:
                    cinema = id
                    st.write(cinema)

    if st.button("Registrar"):
        
        payload = {
            "nome": nome_usuario,
            "email": email,
            "senha": senha,
            "tipo_usuario": tipo_usuario,
            "empresa_id": empresa,
            "cinema_id": cinema
        }

        response = requests.post(f"{API_BASE_URL}/usuarios/", json=payload, headers=headers)
        if response.status_code == 200:
            st.success("Usuário registrado com sucesso!")
        else:
            st.error("Erro ao registrar o usuário.")

def create_servico():
    """
    Exemplo de função para cadastrar um serviço.
    Útil para Encarregado (mas Admin pode ver, se desejar).
    """
    st.header("Registrar Novo Serviço")
    encarregado_id = st.number_input("ID do Encarregado", min_value=1, step=1)
    sala_id = st.number_input("ID da Sala", min_value=1, step=1)
    tipo_servico = st.text_input("Tipo de Serviço")
    observacoes = st.text_area("Observações")

    if st.button("Registrar"):
        token = st.session_state.get("token")
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "encarregado_id": encarregado_id,
            "sala_id": sala_id,
            "tipo_servico": tipo_servico,
            "observacoes": observacoes
        }
        response = requests.post(f"{API_BASE_URL}/servicos/", json=payload, headers=headers)
        if response.status_code == 200:
            st.success("Serviço registrado com sucesso!")
        else:
            st.error("Erro ao registrar o serviço.")

# ============ MENUS POR TIPO DE USUÁRIO ============

def admin_menu():
    st.sidebar.subheader("Menu Admin")
    opcao = st.sidebar.selectbox("Opções", ["Gerenciar Usuários", "Ver Serviços", "Cadastrar Serviço", "Relatórios"])
    if opcao == "Gerenciar Usuários":
        st.write("Tela de gerenciamento de usuários (em desenvolvimento).")
    elif opcao == "Ver Serviços":
        show_servicos()
    elif opcao == "Cadastrar Serviço":
        cadastrar_servico()
    elif opcao == "Relatórios":
        st.write("Tela de relatórios (em desenvolvimento).")


def gerente_menu():
    st.sidebar.subheader("Menu Gerente")
    opcao = st.sidebar.selectbox("Opções", ["Ver Serviços", "Cadastrar Serviço"])
    if opcao == "Ver Serviços":
        show_servicos()
    elif opcao == "Cadastrar Serviço":
        cadastrar_servico()


def representante_menu():
    st.sidebar.subheader("Menu Representante")
    opcao = st.sidebar.selectbox("Opções", ["Ver Serviços"])
    if opcao == "Ver Serviços":
        show_servicos()


def encarregado_menu():
    st.sidebar.subheader("Menu Encarregado")
    opcao = st.sidebar.selectbox("Opções", ["Ver Serviços", "Cadastrar Serviço"])
    if opcao == "Ver Serviços":
        show_servicos()
    elif opcao == "Cadastrar Serviço":
        cadastrar_servico()