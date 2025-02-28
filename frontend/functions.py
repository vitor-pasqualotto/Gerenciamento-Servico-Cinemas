from PIL import Image
from backend import auth, models
from fastapi import Depends
import streamlit as st
import requests
import os

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
    if token:
        headers = {"Authorization": f"Bearer {token}"}

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
                        
            cinema = None

        else:
            empresa = st.selectbox("Empresa", options=options_empresa)

            if empresa:
                # Setando ID da empresa selecionada
                for id, nome in dict_empresas.items():
                    if nome == empresa:
                        empresa = id
                        
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
    
    else:
        st.error("Usuário não autenticado.")

def create_empresa():
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}

    st.header("Registrar Nova Empresa")

    nome_empresa = st.text_input("Nome da Empresa")
    cnpj = st.text_input("CNPJ da Empresa", placeholder="XX.XXX.XXX/0001-XX")
    contato = st.text_input("Email da Empresa", placeholder="exemplo@dominio.com")

    if nome_empresa and cnpj and contato:

        if st.button("Registrar"):
            token = st.session_state.get("token")
            headers = {"Authorization": f"Bearer {token}"}
            payload = {
                "nome": nome_empresa,
                "cnpj": cnpj,
                "contato": contato
            }
            response = requests.post(f"{API_BASE_URL}/empresas/", json=payload, headers=headers)

            if response.status_code == 200:
                st.success("Empresa registrada com sucesso!")

            else:
                st.error("Erro ao registrar a empresa.")

def create_cinema():
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        # Recuperando todas as empresas para adicionar no dropdown
        response = requests.get(f"{API_BASE_URL}/empresas/", headers=headers)
        if response.status_code == 200:
            empresas = response.json()
            dict_empresas = {empresa['id']: empresa['nome'] for empresa in empresas}
            options_empresa = []
            for id, nome in dict_empresas.items():
                options_empresa.append(nome)

        st.header("Registrar Novo Cinema")

        nome_cinema = st.text_input("Nome do Cinema")
        endereco = st.text_input("Endereço do Cinema")
        empresa = st.selectbox("Selecione a Empresa", options=options_empresa)

        if empresa:
            # Setando ID da empresa selecionada
            for id, nome in dict_empresas.items():
                if nome == empresa:
                    empresa = id

            if nome_cinema and endereco and empresa:

                if st.button("Registrar"):
                    token = st.session_state.get("token")
                    headers = {"Authorization": f"Bearer {token}"}
                    payload = {
                        "nome": nome_cinema,
                        "endereco": endereco,
                        "empresa_id": empresa
                    }
                    response = requests.post(f"{API_BASE_URL}/cinemas/", json=payload, headers=headers)

                    if response.status_code == 200:
                        st.success("Cinema registrado com sucesso!")

                    else:
                        st.error("Erro ao registrar o cinema.")

def create_sala():
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        # Recuperando todas as empresas para adicionar do dropdown
        response = requests.get(f"{API_BASE_URL}/empresas/", headers=headers)
        if response.status_code == 200:
            empresas = response.json()
            dict_empresas = {empresa['id']: empresa['nome'] for empresa in empresas}
            options_empresa = []
            for id, nome in dict_empresas.items():
                options_empresa.append(nome)

        st.header("Registrar Novo Cinema")

        nome_sala = st.text_input("Nome da Sala")
        empresa = st.selectbox("Empresa", options=options_empresa)

        if empresa:
            # Setando ID da empresa selecionada
            for id, nome in dict_empresas.items():
                if nome == empresa:
                    empresa = id

            # Recuperando todas as empresas para adicionar no dropdown
            response = requests.get(f"{API_BASE_URL}/cinemas/", headers=headers)
            if response.status_code == 200:
                cinemas = response.json()
                dict_cinemas = {cinema['id']: cinema['nome'] for cinema in cinemas if cinemas['empresa_id'] == empresa}
                options_cinema = []
                for id, nome in dict_cinemas.items():
                    options_cinema.append(nome)

            cinema = st.selectbox("Cinema", options=options_cinema)

            if cinema:
                # Setando ID da cinema selecionada
                for id, nome in dict_cinemas.items():
                    if nome == cinema:
                        cinema = id

                if nome_sala and empresa and cinema:

                    if st.button("Registrar"):
                        token = st.session_state.get("token")
                        headers = {"Authorization": f"Bearer {token}"}
                        payload = {
                            "nome": nome_sala,
                            "cinema_id": cinema
                        }
                        response = requests.post(f"{API_BASE_URL}/salas/", json=payload, headers=headers)

                        if response.status_code == 200:
                            st.success("Sala registrada com sucesso!")

                        else:
                            st.error("Erro ao registrar a sala.")

# ========== Criação def necessário para create_serviço =============

def save_uploaded_file(uploaded_file, folder="static/uploads/"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = os.path.join(folder, uploaded_file.name)

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path

# ===================================================================

def create_servico(current_user: models.Usuario = Depends(auth.get_current_user)):
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}

        # Recuperando todas as empresas para adicionar do dropdown
        response = requests.get(f"{API_BASE_URL}/empresas/", headers=headers)
        if response.status_code == 200:
            empresas = response.json()
            dict_empresas = {empresa['id']: empresa['nome'] for empresa in empresas}
            options_empresa = []
            for id, nome in dict_empresas.items():
                options_empresa.append(nome)
    
    st.header("Registrar Novo Serviço")

    encarregado_id = requests.get(f"{API_BASE_URL}/usuarios/me", headers=headers).json()["id"]
    tipo_servico = st.selectbox("Tipo de Serviço", options=["bla", "bla bla"])
    empresa = st.selectbox("Empresa", options=options_empresa)

    if empresa:
        
        # Setando ID da empresa selecionada
        for id, nome in dict_empresas.items():
            if nome == empresa:
                empresa = id

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

            response = requests.get(f"{API_BASE_URL}/salas/", headers=headers)
            if response.status_code == 200:
                salas = response.json()
                dict_salas = {sala['id']: sala['nome'] for sala in salas if sala['cinema_id'] == cinema}
                options_sala = []
                for id, nome in dict_salas.items():
                    options_sala.append(nome)

            sala = st.selectbox("Sala", options=options_sala)
            
            if sala:
                # Setando ID da cinema selecionada
                for id, nome in dict_salas.items():
                    if nome == sala:
                        sala = id

                uploaded_files = st.file_uploader("Envie as Fotos", accept_multiple_files=True)
                
                if uploaded_files:
                    st.write(f"Foram carregadas {len(uploaded_files)} imagens.")

                    fotos_urls = []

                    for uploaded_file in uploaded_files:
                        file_path = save_uploaded_file(uploaded_file)
                        image = Image.open(file_path)
                        st.image(image, caption=uploaded_file.name, use_container_width=True)
                        fotos_urls.append(file_path)

                    observacoes = st.text_area("Observações")

                    if encarregado_id and tipo_servico and empresa and sala and fotos_urls and observacoes:

                        if st.button("Registrar"):
                            token = st.session_state.get("token")
                            headers = {"Authorization": f"Bearer {token}"}
                            payload = {
                                "encarregado_id": encarregado_id,
                                "sala_id": sala,
                                "tipo_servico": tipo_servico,
                                "observacoes": observacoes,
                                "fotos_urls": fotos_urls
                            }
                
                            response = requests.post(f"{API_BASE_URL}/servicos/", json=payload, headers=headers)
                            if response.status_code == 200:
                                st.success("Serviço registrado com sucesso!")
                            else:
                                st.error("Erro ao registrar o serviço.")

# UPDATE
