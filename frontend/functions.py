from PIL import Image
#from backend import auth, models
from fastapi import Depends
import streamlit as st
import requests
import os

API_BASE_URL = "http://localhost:8000"

# ============ LOGIN ============

def login():
    st.sidebar.header("Login")

    if "email" not in st.session_state:
        st.session_state.email = ""

    if "senha" not in st.session_state:
        st.session_state.senha = ""

    email = st.sidebar.text_input("Email", value=st.session_state.email)
    senha = st.sidebar.text_input("Senha", type="password", value=st.session_state.senha)

    if st.sidebar.button("Entrar"): 
        data = {"username": email, "password": senha}
        response = requests.post(f"{API_BASE_URL}/token", data=data)
        
        if response.status_code == 200:
            st.session_state.token = response.json().get("access_token")
            st.session_state.email = email
            st.session_state.senha = senha
            st.sidebar.success("Login efetuado com sucesso!")

            # Força uma segunda execução
            st.rerun()

        else:
            st.sidebar.error("Erro no login. Verifique suas credenciais.")

@st.cache_data
def get_current_user():
    token = st.session_state.get("token")
    if not token:
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/usuarios/me", headers=headers)

    if response.status_code == 200:
        return response.json()
    
    return None 

# ============ CALLBACKS ============

def fetch_empresas():
    """Recupera todas as empresas e retorna um dicionário {id: nome}."""
    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.get(f"{API_BASE_URL}/empresas/", headers=headers)
    if response.status_code == 200:
        empresas = response.json()
        return {empresa['id']: empresa['nome'] for empresa in empresas}
    else:
        return {}

def fetch_cinemas(empresa_id):
    """Recupera todos os cinemas de uma empresa específica."""
    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.get(f"{API_BASE_URL}/cinemas/", headers=headers)
    if response.status_code == 200:
        cinemas = response.json()
        st.write("Resposta da API cinemas:", cinemas)  # Debug
        return {cinema['id']: cinema['nome'] for cinema in cinemas if cinema['empresa_id'] == empresa_id}
    else:
        st.error("Erro ao buscar cinemas!")
        return {}

def fetch_salas(cinema_id):
    """Recupera todas as salas de um cinema específico."""
    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.get(f"{API_BASE_URL}/salas/", headers=headers)
    if response.status_code == 200:
        salas = response.json()
        return {sala['id']: sala['nome'] for sala in salas if sala['cinema_id'] == cinema_id}
    else:
        return {}

def callback_empresas():
    st.session_state.empresas = fetch_empresas()

def callback_cinemas():
    st.session_state.cinemas = fetch_cinemas(st.session_state.empresa_id) 

def callback_salas():
    st.session_state.salas = fetch_salas(st.session_state.cinema_id)

# ============ AÇÕES DISPONÍVEIS ============

# READ
@st.cache_data
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

@st.cache_data
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

@st.cache_data
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

@st.cache_data
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

@st.cache_data
def show_servicos(): 
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE_URL}/servicos/", headers=headers)

        if response.status_code == 200:
            registros = response.json()
            st.write("- Lista de Serviços")
            st.table(registros)

        else:
            st.error("Erro ao buscar serviços.")

    else:
        st.error("Usuário não autenticado.")

@st.cache_data
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

    st.header("Registrar Novo Usuário")
    nome_usuario = st.text_input("Nome do Usuário")
    email = st.text_input("Email Usuário")
    senha = st.text_input("Senha Usuário", type='password')
    tipo_usuario = st.selectbox("Tipo de Usuário", ["Gerente", "Representante", "Encarregado"], key="tipo_usuario")
    
    if tipo_usuario in ["Gerente", "Representante"]:
        empresas = {0: "Selecionar"}
        empresas.update(st.session_state.empresas)
        empresa = st.selectbox("Empresa", options=list(empresas.keys()), key="empresa_id", format_func=lambda x: empresas[x], on_change=callback_cinemas, index=0)
        
        if tipo_usuario == "Gerente":
            cinemas = {0: "Selecionar"}
            cinemas.update(st.session_state.cinemas)
            cinema = st.selectbox("Cinema", options=list(cinemas.keys()), key="cinema_id", format_func=lambda x: cinemas[x], on_change=callback_salas, index=0)

        else:
            cinema = None

    else:
        empresa, cinema = None, None
    
    if st.button("Registrar"):
        token = st.session_state.get("token")
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"nome": nome_usuario, "email": email, "senha": senha, "tipo_usuario": tipo_usuario, "empresa_id": empresa, "cinema_id": cinema}
        response = requests.post(f"{API_BASE_URL}/usuarios/", json=payload, headers=headers)
        st.success("Usuário registrado com sucesso!") if response.status_code == 200 else st.error("Erro ao registrar o usuário.")



    """ 
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
"""
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
                dict_cinemas = {cinema['id']: cinema['nome'] for cinema in cinemas if cinema['empresa_id'] == empresa}
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

def create_servico():
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
def update_usuario():
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}

        # Recuperando todos os tipos de usuários para adicionar ao dropdown
        options_tipo = ["Gerente", "Representante", "Encarregado"]

        st.header("Editar Usuário")
        tipo_usuario = st.selectbox("Selecione o Tipo de Usuário", options=options_tipo)

        if tipo_usuario == "Encarregado":

            # Recuperando todos os usuários para adicionar do dropdown
            response = requests.get(f"{API_BASE_URL}/usuarios/", headers=headers)
            if response.status_code == 200:
                usuarios = response.json()
                usuarios_filtrados = [usuario for usuario in usuarios if usuario["tipo_usuario"] == "Encarregado"]
                dict_usuarios = {usuario['id']: usuario['nome'] for usuario in usuarios_filtrados}
                options_usuario = []
                for id, nome in dict_usuarios.items():
                    options_usuario.append(nome)

            usuario_id = st.selectbox("Selecione o Usuário", options=options_usuario)
            
            # Setando ID do usuário selecionado
            for id, nome in dict_usuarios.items():
                if nome == usuario_id:
                    usuario_id = id

            if usuario_id:
                nome_update = st.text_input("Digite o Nome Para Alteração")
                email_update = st.text_input("Digite o Email Para Alteração")
                senha_update = st.text_input("Digite a Senha Para Alteração", type="password")

        elif tipo_usuario == "Representante":

            # Recuperando todos os usuários para adicionar do dropdown
            response = requests.get(f"{API_BASE_URL}/usuarios/", headers=headers)
            if response.status_code == 200:
                usuarios = response.json()
                usuarios_filtrados = [usuario for usuario in usuarios if usuario["tipo_usuario"] == "Representante"]
                dict_usuarios = {usuario['id']: usuario['nome'] for usuario in usuarios_filtrados}
                options_usuario = []
                for id, nome in dict_usuarios.items():
                    options_usuario.append(nome)

            usuario_id = st.selectbox("Selecione o Usuário", options=options_usuario)

            # Setando ID do usuário selecionado
            for id, nome in dict_usuarios.items():
                if nome == usuario_id:
                    usuario_id = id

            if usuario_id:
                nome_update = st.text_input("Digite o Nome Para Alteração")
                email_update = st.text_input("Digite o Email Para Alteração")
                senha_update = st.text_input("Digite a Senha Para Alteração", type="password")
            

        else:

            # Recuperando todos os usuários para adicionar do dropdown
            response = requests.get(f"{API_BASE_URL}/usuarios/", headers=headers)
            if response.status_code == 200:
                usuarios = response.json()
                usuarios_filtrados = [usuario for usuario in usuarios if usuario["tipo_usuario"] == "Gerente"]
                dict_usuarios = {usuario['id']: usuario['nome'] for usuario in usuarios_filtrados}
                options_usuario = []
                for id, nome in dict_usuarios.items():
                    options_usuario.append(nome)

            usuario_id = st.selectbox("Selecione o Usuário", options=options_usuario)

            # Setando ID do usuário selecionado
            for id, nome in dict_usuarios.items():
                if nome == usuario_id:
                    usuario_id = id

            if usuario_id:
                nome_update = st.text_input("Digite o Nome Para Alteração")
                email_update = st.text_input("Digite o Email Para Alteração")
                senha_update = st.text_input("Digite a Senha Para Alteração", type="password")

                # Recuperando todas as empresas para adicionar do dropdown
                response = requests.get(f"{API_BASE_URL}/empresas/", headers=headers)
                if response.status_code == 200:
                    empresas = response.json()
                    dict_empresas = {empresa['id']: empresa['nome'] for empresa in empresas}
                    options_empresas = []
                    for id, nome in dict_empresas.items():
                        options_empresas.append(nome)

                empresa = st.selectbox("Escolha a Empresa Para Alteração", options=options_empresas)

                # Setando ID do usuário selecionado
                for id, nome in dict_empresas.items():
                    if nome == empresa:
                        empresa = id

        if st.button("Atualizar"):
            
            payload = {
                "nome": nome_update,
                "email": email_update,
                "senha": senha_update,
                "tipo_usuario": tipo_usuario,
                "empresa_id": empresa
            }

            response = requests.put(f"{API_BASE_URL}/usuarios/{usuario_id}", json=payload, headers=headers)
            if response.status_code == 200:
                st.success("Usuário Atualizado com sucesso!")

            else:
                st.error("Erro ao Atualizar o usuário.")
    
    else:
        st.error("Usuário não autenticado.")


def update_empresa():
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}

        st.header("Editar Empresa")

        # Recuperando todas as empresas para adicionar do dropdown
        response = requests.get(f"{API_BASE_URL}/empresas/", headers=headers)
        if response.status_code == 200:
            empresas = response.json()
            dict_empresas = {empresa['id']: empresa['nome'] for empresa in empresas}
            options_empresas = []
            for id, nome in dict_empresas.items():
                options_empresas.append(nome)

        empresa_id = st.selectbox("Escolha a Empresa Para Alteração", options=options_empresas)

        # Setando ID do usuário selecionado
        for id, nome in dict_empresas.items():
            if nome == empresa_id:
                empresa_id = id

        if empresa_id:
            nome = st.text_input("Digite o Nome da Empresa")
            cnpj = st.text_input("CNPJ da Empresa", placeholder="XX.XXX.XXX/0001-XX")
            contato = st.text_input("Email da Empresa", placeholder="exemplo@dominio.com")

        if empresa_id and cnpj and contato:

            if st.button("Registrar"):
                token = st.session_state.get("token")
                headers = {"Authorization": f"Bearer {token}"}
                payload = {
                    "nome": nome,
                    "cnpj": cnpj,
                    "contato": contato
                }
                response = requests.put(f"{API_BASE_URL}/empresas/{empresa_id}", json=payload, headers=headers)

                if response.status_code == 200:
                    st.success("Empresa Atualizada com sucesso!")

                else:
                    st.error("Erro ao Atualizar a empresa.")
    else:
        st.error("Usuário não autenticado.")

def update_cinema():
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}

        st.header("Editar Cinema")

        # Recuperando todas as empresas para adicionar do dropdown
        response = requests.get(f"{API_BASE_URL}/empresas/", headers=headers)
        if response.status_code == 200:
            empresas = response.json()
            dict_empresas = {empresa['id']: empresa['nome'] for empresa in empresas}
            options_empresas = []
            for id, nome in dict_empresas.items():
                options_empresas.append(nome)

        empresa_id = st.selectbox("Escolha a Empresa Para Alteração", options=options_empresas)

        # Setando ID do usuário selecionado
        for id, nome in dict_empresas.items():
            if nome == empresa_id:
                empresa_id = id

        if empresa_id:
            # Recuperando todas as empresas para adicionar do dropdown
            response = requests.get(f"{API_BASE_URL}/cinemas/", headers=headers)

            if response.status_code == 200:
                cinemas = response.json()
                cinemas_filtrados = [cinema for cinema in cinemas if cinema["empresa_id"] == empresa_id]
                dict_cinemas = {cinema['id']: cinema['nome'] for cinema in cinemas_filtrados}
                options_cinemas = []
                for id, nome in dict_cinemas.items():
                    options_cinemas.append(nome)

            cinema_id = st.selectbox("Escolha o Cinema", options=options_cinemas)

            # Setando ID do usuário selecionado
            for id, nome in dict_cinemas.items():
                if nome == cinema_id:
                    cinema_id = id
            
            if cinema_id:
                nome = st.text_input("Digite o Nome do Cinema")
                endereco = st.text_input("Digite o Endereço do Cinema")


            if empresa_id and cinema_id and nome and endereco:

                if st.button("Registrar"):
                    token = st.session_state.get("token")
                    headers = {"Authorization": f"Bearer {token}"}
                    payload = {
                        "nome": nome,
                        "endereco": endereco,
                        "empresa_id": empresa_id
                    }
                    response = requests.put(f"{API_BASE_URL}/cinemas/{cinema_id}", json=payload, headers=headers)

                    if response.status_code == 200:
                        st.success("Empresa Atualizada com sucesso!")

                    else:
                        st.error("Erro ao Atualizar a empresa.")
    else:
        st.error("Usuário não autenticado.")

def update_sala():
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}

        st.header("Editar Sala")

        # Recuperando todas as empresas para adicionar do dropdown
        response = requests.get(f"{API_BASE_URL}/cinemas/", headers=headers)

        if response.status_code == 200:
            cinemas = response.json()
            dict_cinemas = {cinema['id']: cinema['nome'] for cinema in cinemas}
            options_cinemas = []
            for id, nome in dict_cinemas.items():
                options_cinemas.append(nome)

        cinema_id = st.selectbox("Escolha o Cinema", options=options_cinemas)

        # Setando ID do usuário selecionado
        for id, nome in dict_cinemas.items():
            if nome == cinema_id:
                cinema_id = id

        # Recuperando todas as empresas para adicionar do dropdown
        response = requests.get(f"{API_BASE_URL}/salas/", headers=headers)
        if response.status_code == 200:
            salas = response.json()
            salas_filtradas = [sala for sala in salas if sala["cinema_id"] == cinema_id]
            dict_salas = {sala['id']: sala['nome'] for sala in salas_filtradas}
            options_salas = []
            for id, nome in dict_salas.items():
                options_salas.append(nome)

        sala_id = st.selectbox("Escolha a Empresa Para Alteração", options=options_salas)

        # Setando ID do usuário selecionado
        for id, nome in dict_salas.items():
            if nome == sala_id:
                sala_id = id

        if sala_id:
            nome = st.text_input("Digite o Nome da Sala")

        if cinema_id and sala_id and nome:

            if st.button("Registrar"):
                token = st.session_state.get("token")
                headers = {"Authorization": f"Bearer {token}"}
                payload = {
                    "nome": nome,
                    "ciniema_id": cinema_id
                }
                response = requests.put(f"{API_BASE_URL}/salas/{sala_id}", json=payload, headers=headers)

                if response.status_code == 200:
                    st.success("Sala Atualizada com sucesso!")

                else:
                    st.error("Erro ao Atualizar a Sala.")
    else:
        st.error("Usuário não autenticado.")

def update_servico():
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}

        st.header("Editar Serviço")

        # Recupera o Usuário atual
        current_user = get_current_user()

        # Identifica o Tipo de Usuário
        tipo_usuario = current_user.get("tipo_usuario")
        id_usuario = current_user.get("id")

        # Verificação do Tipo Usuário
        if tipo_usuario == "Encarregado":

            response = requests.get(f"{API_BASE_URL}/cinemas", headers=headers)

            # Recuperando Todos os Cinemas Para Adicionar ao Dropdown
            if response.status_code == 200:
                cinemas = response.json()
                dict_cinemas = {cinema['id']: cinema['nome'] for cinema in cinemas}
                options_cinemas = []
                for id, nome in dict_cinemas.items():
                    options_cinemas.append(nome)
                
                cinema_id = st.selectbox("Escolha o Serviço Para Alteração", options=options_cinemas)

                # Setando ID do cinema selecionado
                for id, nome in dict_cinemas.items():
                    if nome == cinema_id:
                        cinema_id = id

                if cinema_id:

                    # Recuperando Todas as Salas Para Adicionar ao Dropdown
                    response = requests.get(f"{API_BASE_URL}/salas/", headers=headers)
                    if response.status_code == 200:
                        salas = response.json()
                        salas_filtradas = [sala for sala in salas if sala["cinema_id"] == cinema_id]
                        dict_salas = {sala['id']: sala['nome'] for sala in salas_filtradas}
                        options_salas = []
                        for id, nome in dict_salas.items():
                            options_salas.append(nome)

                    sala_id = st.selectbox("Escolha a Empresa Para Alteração", options=options_salas)

                    # Setando ID do usuário selecionado
                    for id, nome in dict_salas.items():
                        if nome == sala_id:
                            sala_id = id

                    if sala_id:
                        # Recuperando todos os serviços RECUSADOS para a sala selecionada
                        response = requests.get(f"{API_BASE_URL}/servicos/", headers=headers)
                        
                        if response.status_code == 200:
                            servicos = response.json()

                            # Filtrar apenas serviços com status "Recusado" e da sala selecionada
                            servicos_filtrados = [servico for servico in servicos if servico["sala_id"] == sala_id and servico["status"] == "Recusado" and servico["encarregado_id"] == id_usuario]

                            # Criando um dicionário com ID e tipo do serviço
                            dict_servicos = {servico["id"]: servico["tipo_servico"] for servico in servicos_filtrados}
                            options_servicos = []
                            for id, nome in dict_servicos.items():
                                options_servicos.append(nome)

                        servico_id = st.selectbox("Escolha o Serviço Para Alterar", options=options_servicos)

                        # Setando ID do usuário selecionado
                        for id, nome in dict_servicos.items():
                            if nome == servico_id:
                                servico_id = id

                        if servico_id:
                            uploaded_files = st.file_uploader("Envie as Fotos", accept_multiple_files=True)
                    
                            if uploaded_files:
                                st.write(f"Foram carregadas {len(uploaded_files)} imagens.")

                                fotos_urls = []

                                for uploaded_file in uploaded_files:
                                    file_path = save_uploaded_file(uploaded_file)
                                    image = Image.open(file_path)
                                    st.image(image, caption=uploaded_file.name, use_column_width=True)
                                    fotos_urls.append(file_path)

                                observacoes = st.text_area("Observacoes")

                                if cinema_id and sala_id and servico_id and uploaded_files and observacoes:

                                    if st.button("Registrar"):
                                        token = st.session_state.get("token")
                                        headers = {"Authorization": f"Bearer {token}"}
                                        payload = {
                                            "status": "Pendente",
                                            "observacoes": observacoes,
                                            "fotos_urls": fotos_urls
                                        }
                                        response = requests.put(f"{API_BASE_URL}/servicos/{servico_id}", json=payload, headers=headers)

                                        if response.status_code == 200:
                                            st.success("Serviço Atualizado com sucesso!")

                                        else:
                                            st.error("Erro ao Atualizar o Serviço.")

        elif tipo_usuario == "Gerente":
                
            # Recuperando Todas as Salas Para Adicionar ao Dropdown
            response = requests.get(f"{API_BASE_URL}/salas/", headers=headers)
            
            if response.status_code == 200:
                salas = response.json()
                dict_salas = {sala['id']: sala['nome'] for sala in salas}
                options_salas = []
                for id, nome in dict_salas.items():
                    options_salas.append(nome)

            sala_id = st.selectbox("Escolha a Sala Para Alteração", options=options_salas)

            # Setando ID do usuário selecionado
            for id, nome in dict_salas.items():
                if nome == sala_id:
                    sala_id = id

            if sala_id:
                response = requests.get(f"{API_BASE_URL}/servicos/", headers=headers)

                if response.status_code == 200:
                    servicos = response.json()

                    # Aplicar o filtro localmente no Streamlit: Apenas serviços pendentes da sala escolhida
                    servicos_filtrados = [servico for servico in servicos if servico["sala_id"] == sala_id and servico["status"] == "Pendente"]
                   
                    # Criar dicionário ID, Tipo Serviço → Tipo de Serviço apenas dos serviços pendentes da sala
                    dict_servicos = {servico["id"]: servico["tipo_servico"] for servico in servicos_filtrados}
                    options_servicos = []
                    for id, nome in dict_servicos.items():
                        options_servicos.append(nome)

                servico_id = st.selectbox("Escolha o Serviço", options=options_servicos)

                # Setando ID do usuário selecionado
                for id, nome in dict_servicos.items():
                    if nome == servico_id:
                        servico_id = id

                if servico_id:
                    # Buscar Serviço Selecionado
                    servico_selecionado = next((s for s in servicos_filtrados if s["id"] == servico_id), None)

                    if servico_selecionado:
                        st.write(f"Serviço Selecionado: {servico_selecionado["tipo_servico"]}")

                        # Exibir Observações
                        st.subheader("📌 Observações:")
                        if servico_selecionado["observacoes"]:
                            st.write(servico_selecionado["observacoes"])
                        else:
                            st.write("Sem observações registradas.")

                        # Buscando fotos do serviço selecionado
                        response = requests.get(f"{API_BASE_URL}/imagens/", headers=headers)
                        if response.status_code == 200:
                            fotos = response.json()
                            dict_fotos = {foto["id"]: foto["url_foto"] for foto in fotos if foto["servico_id"] == servico_id}
                            options_fotos = []
                            for id, url_foto in dict_fotos.items():
                                options_fotos.append(url_foto)

                            # Exibir Fotos Associadas ao Serviço
                            st.subheader("📷 Fotos do Serviço:")
                            if servico_selecionado:
                                for foto_url in options_fotos:
                                    image = Image.open(f"../{foto_url}")
                                    st.image(image, caption="Foto do Serviço", use_container_width=True)
                        else:
                            st.write("Nenhuma foto disponível para este serviço.")

                        # Permitir atualização do status e observações
                        g_observacoes = st.text_area("Escreva as Observações", placeholder="Aprovado Pelo Gerente")

                        if g_observacoes:
                            aprovar = st.button("Aprovar", type="primary")
                            recusar = st.button("Recusar", type="secondary")

                            if aprovar:
                                token = st.session_state.get("token")
                                headers = {"Authorization": f"Bearer {token}"}
                                payload = {
                                    "observacoes": g_observacoes,
                                    "status": "Aprovado",
                                }
                                response = requests.put(f"{API_BASE_URL}/servicos/{servico_id}", json=payload, headers=headers)

                                if response.status_code == 200:
                                    st.success("Serviço Atualizado com sucesso!")

                                else:
                                    st.error("Erro ao Atualizar o Serviço.")

                            if recusar:
                                token = st.session_state.get("token")
                                headers = {"Authorization": f"Bearer {token}"}
                                payload = {                                   
                                    "observacoes": g_observacoes,
                                    "status": "Recusado",
                                }
                                response = requests.put(f"{API_BASE_URL}/servicos/{servico_id}", json=payload, headers=headers)

                                if response.status_code == 200:
                                    st.success("Serviço Atualizado com sucesso!")

                                else:
                                    st.error("Erro ao Atualizar o Serviço.")
        
        if tipo_usuario == "Admin":

            # Recuperando todas as empresas para adicionar do dropdown
            response = requests.get(f"{API_BASE_URL}/empresas/", headers=headers)
            if response.status_code == 200:
                empresas = response.json()
                dict_empresas = {empresa['id']: empresa['nome'] for empresa in empresas}
                options_empresas = []
                for id, nome in dict_empresas.items():
                    options_empresas.append(nome)

            empresa_id = st.selectbox("Escolha a Empresa Para Alteração", options=options_empresas)

            # Setando ID do usuário selecionado
            for id, nome in dict_empresas.items():
                if nome == empresa_id:
                    empresa_id = id

            if empresa_id:

                # Recuperando todos os cinemas para adicionar do dropdown
                response = requests.get(f"{API_BASE_URL}/cinemas/", headers=headers)

                if response.status_code == 200:
                    cinemas = response.json()
                    cinemas_filtrados = [cinema for cinema in cinemas if cinema["empresa_id"] == empresa_id]
                    dict_cinemas = {cinema['id']: cinema['nome'] for cinema in cinemas_filtrados}
                    options_cinemas = []
                    for id, nome in dict_cinemas.items():
                        options_cinemas.append(nome)

                cinema_id = st.selectbox("Escolha o Cinema", options=options_cinemas)

                # Setando ID do usuário selecionado
                for id, nome in dict_cinemas.items():
                    if nome == cinema_id:
                        cinema_id = id

                if cinema_id:

                    # Recuperando todas as salas para adicionar do dropdown
                    response = requests.get(f"{API_BASE_URL}/salas/", headers=headers)
                    if response.status_code == 200:
                        salas = response.json()
                        salas_filtradas = [sala for sala in salas if sala["cinema_id"] == cinema_id]
                        dict_salas = {sala['id']: sala['nome'] for sala in salas_filtradas}
                        options_salas = []
                        for id, nome in dict_salas.items():
                            options_salas.append(nome)

                    sala_id = st.selectbox("Escolha a Empresa Para Alteração", options=options_salas)

                    # Setando ID do usuário selecionado
                    for id, nome in dict_salas.items():
                        if nome == sala_id:
                            sala_id = id

                    if sala_id:
                        response = requests.get(f"{API_BASE_URL}/servicos/", headers=headers)

                        if response.status_code == 200:
                            servicos = response.json()

                            # Aplicar o filtro localmente no Streamlit: Apenas serviços pendentes da sala escolhida
                            servicos_filtrados = [servico for servico in servicos if servico["sala_id"] == sala_id and servico["status"] == "Aprovado"]
                        
                            # Criar dicionário ID, Tipo Serviço → Tipo de Serviço apenas dos serviços pendentes da sala
                            dict_servicos = {servico["id"]: servico["tipo_servico"] for servico in servicos_filtrados}
                            options_servicos = []
                            for id, nome in dict_servicos.items():
                                options_servicos.append(nome)

                        servico_id = st.selectbox("Escolha o Serviço", options=options_servicos)

                        # Setando ID do usuário selecionado
                        for id, nome in dict_servicos.items():
                            if nome == servico_id:
                                servico_id = id

                        if servico_id:

                            servico_selecionado = next((s for s in servicos_filtrados if s["id"] == servico_id), None)

                            # Exibir Observações
                            if servico_selecionado:
                                st.subheader("📌 Observações:")
                                st.write(servico_selecionado["observacoes"])
                            else:
                                st.write("Serviço concluído sem obervações.")

                            # Buscando fotos do serviço selecionado
                            response = requests.get(f"{API_BASE_URL}/imagens/", headers=headers)
                            if response.status_code == 200:
                                fotos = response.json()
                                dict_fotos = {foto["id"]: foto["url_foto"] for foto in fotos if foto["servico_id"] == servico_id}
                                options_fotos = []
                                for id, url_foto in dict_fotos.items():
                                    options_fotos.append(url_foto)

                                # Exibir Fotos Associadas ao Serviço
                                st.subheader("📷 Fotos do Serviço:")
                                if servico_selecionado:
                                    for foto_url in options_fotos:
                                        image = Image.open(f"../{foto_url}")
                                        st.image(image, caption="Foto do Serviço", use_container_width=True)

                            # Adicionar Observações
                            adm_observacoes = st.text_area("Escreva as Observações", placeholder="Serviço Concluído")

                            if adm_observacoes:
                                concluir = st.button("Aprovar", type="primary")
                                analise = st.button("Análise", type="secondary")
                                recusar = st.button("Recusar", type="tertiary")

                                if concluir:
                                    token = st.session_state.get("token")
                                    headers = {"Authorization": f"Bearer {token}"}
                                    payload = {
                                        "status": "Concluido",
                                        "observacoes": adm_observacoes
                                    }
                                    response = requests.put(f"{API_BASE_URL}/servicos/{servico_id}", json=payload, headers=headers)

                                    if response.status_code == 200:
                                        st.success("Serviço Atualizado com sucesso!")

                                    else:
                                        st.error("Erro ao Atualizar o Serviço.")

                                if recusar:
                                    token = st.session_state.get("token")
                                    headers = {"Authorization": f"Bearer {token}"}
                                    payload = {                                   
                                        "observacoes": adm_observacoes,
                                        "status": "Recusado",
                                    }
                                    response = requests.put(f"{API_BASE_URL}/servicos/{servico_id}", json=payload, headers=headers)

                                    if response.status_code == 200:
                                        st.success("Serviço Atualizado com sucesso!")

                                    else:
                                        st.error("Erro ao Atualizar o Serviço.")
                                    
                                if analise:
                                    token = st.session_state.get("token")
                                    headers = {"Authorization": f"Bearer {token}"}
                                    payload = {                                   
                                        "observacoes": adm_observacoes,
                                        "status": "Em Análise",
                                    }
                                    response = requests.put(f"{API_BASE_URL}/servicos/{servico_id}", json=payload, headers=headers)

                                    if response.status_code == 200:
                                        st.success("Serviço Atualizado com sucesso!")

                                    else:
                                        st.error("Erro ao Atualizar o Serviço.")

    else:
        st.error("Usuário não autenticado.")

# ============ Interfaces de cada Usuário ============

# Admin
def menu_admin():
    st.title("Admin")
    st.subheader("Aqui você pode gerenciar todo o seu negócio")

    if "pagina" not in st.session_state:
        st.session_state.pagina = "Dashboard"

    with st.sidebar:
        st.title("Menu")
        pagina = st.radio("Escolha uma página:", ["Dashboard", "Empresas", "Cinemas", "Salas", "Serviços", "Usuários"])

    st.session_state.pagina = pagina

    if st.session_state.pagina == "Dashboard":
        st.title("Em desenvolvimento...")

    if st.session_state.pagina == "Empresas":
        st.title("Empresas")
        acao = st.radio("Escolha a ação que deseja realizar:", ["Criar Empresa", "Atualizar Empresa", "Listar Empresas"])

        if acao == "Criar Empresa":
            create_empresa()

        if acao == "Atualizar Empresa":
            update_empresa()

        if acao == "Listar Empresas":
            show_empresas()

    if st.session_state.pagina == "Cinemas":
        st.title("Cinemas")
        acao = st.radio("Escolha a ação que deseja realizar:", ["Criar Cinema", "Atualizar Cinema", "Listar Cinemas"])

        if acao == "Criar Cinema":
            create_cinema()

        if acao == "Atualizar Cinema":
            update_cinema()

        if acao == "Listar Cinemas":
            show_cinemas()

    if st.session_state.pagina == "Salas":
        st.title("Salas")
        acao = st.radio("Escolha a ação que deseja realizar:", ["Criar Sala", "Atualizar Sala", "Listar Salas"])

        if acao == "Criar Sala":
            create_sala()

        if acao == "Atualizar Sala":
            update_sala()

        if acao == "Listar Salas":
            show_salas()

    if st.session_state.pagina == "Serviços":
        st.title("Serviços")
        acao = st.radio("Escolha a ação que deseja realizar:", ["Criar Serviço", "Atualizar Serviço", "Listar Serviços"])

        if acao == "Criar Serviço":
            create_servico()

        if acao == "Atualizar Serviço":
            update_servico()

        if acao == "Listar Serviços":
            show_servicos()

    if st.session_state.pagina == "Usuários":
        st.title("Usuários")
        acao = st.radio("Escolha a ação que deseja realizar:", ["Criar Usuário", "Atualizar Usuário", "Listar Usuários"])

        if acao == "Criar Usuário":
            create_usuario()

        if acao == "Atualizar Usuário":
            update_usuario()

        if acao == "Listar Usuários":
            show_usuarios()


def menu_encarregado():
    st.title("Encarregado")
    st.subheader("Aqui você pode gerenciar seus serviços")
    st.title("Menu")
    acao = st.radio("Escolha uma página:", ["Registrar Serviço", "Atualizar Serviço", "Serviços Recusados"])

    if acao == "Registrar Serviço":
        create_servico()

    if acao == "Atualizar Serviço":
        update_servico()

    if acao == "Serviços Recusados":
        show_servicos()

def menu_gerente():
    st.title("Gerente")
    st.subheader("Aqui você pode gerenciar seu Cinema")
    st.title("Menu")
    acao = st.radio("Escolha uma página:", ["Atualizar Serviço", "Serviços Pendentes"])

    if acao == "Atualizar Serviço":
        update_servico()

    if acao == "Serviços Pendentes":
        show_servicos()

def menu_representante():
    st.title("Representante")
    st.subheader("Aqui você pode ver os serviços concluídos do seu Cinema")
    
    show_servicos()