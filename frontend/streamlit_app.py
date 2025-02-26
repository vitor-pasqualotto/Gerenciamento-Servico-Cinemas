import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"

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

def show_servicos():
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE_URL}/servicos/", headers=headers)
        if response.status_code == 200:
            servicos = response.json()
            st.write("### Lista de Serviços")
            st.table(servicos)
        else:
            st.error("Erro ao buscar serviços.")
    else:
        st.error("Usuário não autenticado.")

def cadastrar_servico():
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


# ============ APLICAÇÃO PRINCIPAL ============

def main():
    
    st.title("Dashboard - Gestão de Serviços de Limpeza para Cinemas")

    # Se não houver token, exibe tela de login
    if "token" not in st.session_state:
        login()
    else:
        # Tenta obter dados do usuário atual
        user = get_current_user()
        if not user:
            st.error("Não foi possível obter informações do usuário.")
            st.stop()

        # Exibe quem está logado
        st.sidebar.write(f"Bem-vindo, {user['nome']} ({user['tipo_usuario']})")

        # Verifica tipo de usuário e chama o menu apropriado
        if user["tipo_usuario"] == "Admin":
            admin_menu()
        elif user["tipo_usuario"] == "Gerente":
            gerente_menu()
        elif user["tipo_usuario"] == "Representante":
            representante_menu()
        elif user["tipo_usuario"] == "Encarregado":
            encarregado_menu()
        else:
            st.error("Tipo de usuário desconhecido.")

if __name__ == "__main__":
    main()
