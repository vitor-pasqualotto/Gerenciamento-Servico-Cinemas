from PIL import Image
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

def callback_empresas():
    """Recupera todas as empresas e retorna um dicionário {id: nome}."""
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = requests.get(f"{API_BASE_URL}/empresas/", headers=headers)

        if response.status_code == 200:
            empresas = response.json()
            st.session_state.empresas = {empresa['id']: empresa['nome'] for empresa in empresas}

def callback_cinemas():
    """Recupera todos os cinemas de uma empresa específica."""
    token = st.session_state.get("token")
    if token:
        empresa_id = st.session_state.empresa_id
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = requests.get(f"{API_BASE_URL}/cinemas/", headers=headers)
        if response.status_code == 200:
            cinemas = response.json()
            st.write("Resposta da API cinemas:", cinemas)  # Debug
            st.session_state.cinemas = {cinema['id']: cinema['nome'] for cinema in cinemas if cinema['empresa_id'] == empresa_id} 

def callback_salas():
    """Recupera todas as salas de um cinema específico."""
    token = st.session_state.get("token")
    if token:
        cinema_id = st.session_state.cinema_id
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = requests.get(f"{API_BASE_URL}/salas/", headers=headers)
        if response.status_code == 200:
            salas = response.json()
            st.session_state.salas = {sala['id']: sala['nome'] for sala in salas if sala['cinema_id'] == cinema_id}

def callback_usuarios():
    """Recupera todos os usuarios de um tipo específico."""
    token = st.session_state.get("token")
    if token:
        tipo_usuario = st.session_state.tipo_usuario
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = requests.get(f"{API_BASE_URL}/usuarios/", headers=headers)
        if response.status_code == 200:
            usuarios = response.json()
            st.session_state.usuarios = {usuario['id']: usuario['nome'] for usuario in usuarios if usuario['tipo_usuario'] == tipo_usuario}

def callback_usuario_especifico():
    """Recupera um usuario específico."""
    token = st.session_state.get("token")
    if token:
        usuario_id = st.session_state.usuario_id
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = requests.get(f"{API_BASE_URL}/usuarios/", headers=headers)
        if response.status_code == 200:
            usuarios = response.json()
            st.session_state.usuario_especifico = [usuario for usuario in usuarios if usuario["id"] == usuario_id]

def callback_servicos():
    """Atualiza a lista de serviços com base no tipo de usuário logado."""
    token = st.session_state.get("token")
    current_user = get_current_user()

    if token and current_user:
        headers = {"Authorization": f"Bearer {token}"}
        response_servicos = requests.get(f"{API_BASE_URL}/servicos/", headers=headers)
        response_salas = requests.get(f"{API_BASE_URL}/salas", headers=headers)

        if response_servicos.status_code == 200 and response_salas.status_code == 200:
            todos_servicos = response_servicos.json()
            todas_salas = response_salas.json()

            # Filtrando serviços de acordo com o tipo de usuário
            if current_user["tipo_usuario"] == "Encarregado":
                servicos_filtrados = [
                    servico for servico in todos_servicos
                    if servico["status"] == "Recusado" and servico["encarregado_id"] == current_user["id"]
                ]
            elif current_user["tipo_usuario"] == "Gerente":
                servicos_filtrados = []

                for servico in todos_servicos:
                    if servico["status"] == "Pendente":
                        for sala in todas_salas:
                            if sala["id"] == servico["sala_id"]:
                                if sala["cinema_id"] == current_user["cinema_id"]:
                                    servicos_filtrados.append(servico)

            elif current_user["tipo_usuario"] == "Admin":
                servicos_filtrados = [
                    servico for servico in todos_servicos
                    if servico["status"] == "Aprovado"
                ]
            else:
                servicos_filtrados = []

            st.session_state.servicos = servicos_filtrados

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

def create_empresa():
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
        st.header("Registrar Novo Cinema")
        empresas = {0: "Selecionar"}
        empresas.update(st.session_state.empresas)
        empresa = st.selectbox("Selecione a Empresa", options=list(empresas.keys()), key="empresa_id", format_func=lambda x: empresas[x], on_change=callback_cinemas, index=0)

        if empresa:

            nome_cinema = st.text_input("Nome do Cinema")
            endereco = st.text_input("Endereço do Cinema")

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
        st.header("Registrar Nova Sala")
        empresas = {0: "Selecionar"}
        empresas.update(st.session_state.empresas)
        empresa = st.selectbox("Selecione a Empresa", options=list(empresas.keys()), key="empresa_id", format_func=lambda x: empresas[x], on_change=callback_cinemas, index=0)
        
        if empresa:
            cinemas = {0: "Selecionar"}
            cinemas.update(st.session_state.cinemas)
            cinema = st.selectbox("Cinema", options=list(cinemas.keys()), key="cinema_id", format_func=lambda x: cinemas[x], on_change=callback_salas, index=0)
            if cinema:
                st.write("Salas Existentes")
                for n in range(len(st.session_state.salas)):
                    st.write(st.session_state.salas[n+1])

                nome_sala = st.text_input("Nome da Sala")

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

def save_uploaded_file(uploaded_file, folder="../static/uploads/"):
    if not os.path.exists(folder):  
        os.makedirs(folder)

    file_path = os.path.join(folder, uploaded_file.name)

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path

# ===================================================================

def create_servico():
    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"}

    st.header("Registrar Novo Serviço")
    empresas = {0: "Selecionar"}
    empresas.update(st.session_state.empresas)
    empresa = st.selectbox("Selecione a Empresa", options=list(empresas.keys()), key="empresa_id", format_func=lambda x: empresas[x], on_change=callback_cinemas, index=0)
    
    if empresa:
        cinemas = {0: "Selecionar"}
        cinemas.update(st.session_state.cinemas)
        cinema = st.selectbox("Cinema", options=list(cinemas.keys()), key="cinema_id", format_func=lambda x: cinemas[x], on_change=callback_salas, index=0)
        if cinema:
            salas = {0: "Selecionar"}
            salas.update(st.session_state.salas)
            sala = st.selectbox("Salas", options=list(salas.keys()), key="sala_id", format_func=lambda x: salas[x], index=0)

            if sala:

                encarregado_id = requests.get(f"{API_BASE_URL}/usuarios/me", headers=headers).json()["id"]
                tipo_servico = st.selectbox("Tipo de Serviço", options=["Limpeza de Carpete", "Limpeza de Tela", "Limpeza de Cortinas"])
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

                    if observacoes:

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
    st.header("Editar Usuário")
    
    # Recuperando todos os tipos de usuários para adicionar ao dropdown
    options_tipo = ["Selecionar", "Gerente", "Representante", "Encarregado"]
    tipo_usuario = st.selectbox("Selecione o Tipo de Usuário", options=options_tipo, key="tipo_usuario", on_change=callback_usuarios)

    if tipo_usuario and tipo_usuario != "Selecionar":
        usuarios = {0: "Selecionar"}
        usuarios.update(st.session_state.usuarios)
        usuario = st.selectbox("Selecione o Usuário", options=list(usuarios.keys()), key="usuario_id", format_func=lambda x: usuarios[x], on_change=callback_usuario_especifico, index=0)

        if usuario and usuario != 0:
            st.write(f"Nome: {st.session_state.usuario_especifico[0]["nome"]}")
            st.write(f"Email: {st.session_state.usuario_especifico[0]["email"]}")
            
            nome_update = st.text_input("Digite o Nome Para Alteração")
            email_update = st.text_input("Digite o Email Para Alteração")
            senha_update = st.text_input("Digite a Senha Para Alteração", type="password")

            empresa = st.session_state.usuario_especifico[0]["empresa_id"]
            cinema = st.session_state.usuario_especifico[0]["cinema_id"]

            if st.button("Atualizar"):
                token = st.session_state.get("token")
                headers = {"Authorization": f"Bearer {token}"}
                payload = {
                    "nome": nome_update,
                    "email": email_update,
                    "senha": senha_update,
                    "tipo_usuario": tipo_usuario,
                    "empresa_id": empresa,
                    "cinema_id": cinema
                }

                response = requests.put(f"{API_BASE_URL}/usuarios/{usuario}", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Usuário Atualizado com sucesso!")

                else:
                    st.error("Erro ao Atualizar o usuário.")


def update_empresa():
    token = st.session_state.get("token")
    if token:
        headers = {"Authorization": f"Bearer {token}"}

        st.header("Registrar Novo Serviço")
        empresas = {0: "Selecionar"}
        empresas.update(st.session_state.empresas)
        empresa = st.selectbox("Selecione a Empresa", options=list(empresas.keys()), key="empresa_id", format_func=lambda x: empresas[x], index=0)
    
        if empresa:
            nome = st.text_input("Digite o Nome da Empresa")
            cnpj = st.text_input("CNPJ da Empresa", placeholder="XX.XXX.XXX/0001-XX")
            contato = st.text_input("Email da Empresa", placeholder="exemplo@dominio.com")

        if empresa and nome and cnpj and contato:

            if st.button("Registrar"):
                token = st.session_state.get("token")
                headers = {"Authorization": f"Bearer {token}"}
                payload = {
                    "nome": nome,
                    "cnpj": cnpj,
                    "contato": contato
                }
                response = requests.put(f"{API_BASE_URL}/empresas/{empresa}", json=payload, headers=headers)

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

        st.header("Atuaizar Cinema")
        empresas = {0: "Selecionar"}
        empresas.update(st.session_state.empresas)
        empresa = st.selectbox("Selecione a Empresa", options=list(empresas.keys()), key="empresa_id", format_func=lambda x: empresas[x], on_change=callback_cinemas, index=0)
        
        if empresa:
            cinemas = {0: "Selecionar"}
            cinemas.update(st.session_state.cinemas)
            cinema = st.selectbox("Cinema", options=list(cinemas.keys()), key="cinema_id", format_func=lambda x: cinemas[x], on_change=callback_salas, index=0)

            if empresa and cinema:
                nome = st.text_input("Digite o Nome Para Alteração")
                endereco = st.text_input("Digite o Endereço Para Alteração")

                if st.button("Registrar"):
                    token = st.session_state.get("token")
                    headers = {"Authorization": f"Bearer {token}"}
                    payload = {
                        "nome": nome,
                        "endereco": endereco,
                        "empresa_id": empresa
                    }
                    response = requests.put(f"{API_BASE_URL}/cinemas/{cinema}", json=payload, headers=headers)

                    if response.status_code == 200:
                        st.success("Empresa Atualizada com sucesso!")

                    else:
                        st.error("Erro ao Atualizar a empresa.")
    else:
        st.error("Usuário não autenticado.")

def update_sala():
    token = st.session_state.get("token")
    if token:
        st.header("Editar Sala")
        empresas = {0: "Selecionar"}
        empresas.update(st.session_state.empresas)
        empresa = st.selectbox("Selecione a Empresa", options=list(empresas.keys()), key="empresa_id", format_func=lambda x: empresas[x], on_change=callback_cinemas, index=0)
        
        if empresa:
            cinemas = {0: "Selecionar"}
            cinemas.update(st.session_state.cinemas)
            cinema = st.selectbox("Cinema", options=list(cinemas.keys()), key="cinema_id", format_func=lambda x: cinemas[x], on_change=callback_salas, index=0)

            if cinema:
                salas = {0: "Selecionar"}
                salas.update(st.session_state.salas)
                sala = st.selectbox("Salas", options=list(salas.keys()), key="sala_id", format_func=lambda x: salas[x], index=0)

                if sala:
                    nome = st.text_input("Digite o nome para alteração")

                    if nome:

                        if st.button("Registrar"):
                            token = st.session_state.get("token")
                            headers = {"Authorization": f"Bearer {token}"}
                            payload = {
                                "nome": nome,
                                "ciniema_id": cinema
                            }
                            response = requests.put(f"{API_BASE_URL}/salas/{sala}", json=payload, headers=headers)

                            if response.status_code == 200:
                                st.success("Sala Atualizada com sucesso!")

                            else:
                                st.error("Erro ao Atualizar a Sala.")
    else:
        st.error("Usuário não autenticado.")

def update_servico():
    """Interface para atualização de serviço baseado na permissão do usuário."""
    st.header("Atualizar Serviço")

    # Pegando dados do usuário logado
    current_user = get_current_user()
    tipo_usuario = current_user["tipo_usuario"]
    
    callback_servicos()

    # Exibir serviços em forma de botões clicáveis
    servicos = st.session_state["servicos"]
    if not servicos:
        st.warning("Nenhum serviço disponível para atualização.")
        return

    st.subheader("📋 Selecione um serviço para editar:")
    
    for servico in servicos:
        if st.button(f"📌 {servico['id']} - {servico['tipo_servico']} - {servico['status']}", key=f"btn_{servico['id']}"):
            st.session_state.servico_selecionado = servico

    # Exibir detalhes do serviço selecionado
    if "servico_selecionado" in st.session_state:
        servico = st.session_state.servico_selecionado
        st.subheader(f"📝 Editando Serviço: {servico['tipo_servico']}")
        st.write(f"**Observações:** {servico['observacoes'] or 'Nenhuma observação registrada'}")

        # Buscar imagens associadas ao serviço
        response_fotos = requests.get(f"{API_BASE_URL}/imagens", headers={"Authorization": f"Bearer {st.session_state.get('token')}"})
        fotos = response_fotos.json() if response_fotos.status_code == 200 else []

        # Exibir imagens do serviço
        st.subheader("📷 Fotos do Serviço:")
        for foto in fotos:
            if foto["servico_id"] == servico["id"] and os.path.exists(foto['url_foto']):
                image = Image.open(f"{foto['url_foto']}")
                st.image(image, caption="Imagem do Serviço", use_container_width=True)

        # Upload de novas imagens (Apenas para Encarregados)
        if tipo_usuario == "Encarregado":
            uploaded_files = st.file_uploader("Envie novas imagens (substituirá as antigas)", accept_multiple_files=True)

            if uploaded_files:
                # Removendo imagens antigas
                for foto in fotos:
                    if foto["servico_id"] == servico["id"]:
                        old_path = f"{foto['url_foto']}"
                        if os.path.exists(old_path):
                            os.remove(old_path)

                st.write(f"Foram carregadas {len(uploaded_files)} imagens.")

                fotos_urls = []
                
                # Salvando novas imagens
                for uploaded_file in uploaded_files:
                    file_path = save_uploaded_file(uploaded_file)
                    image = Image.open(file_path)
                    st.image(image, caption=uploaded_file.name, use_container_width=True)
                    fotos_urls.append(file_path)

        # Novas Observações
        observacoes = st.text_area("Escreva as Observações")

        # Seleção de Status (Dependendo do Tipo de Usuário)
        if tipo_usuario == "Gerente":
            status_opcoes = ["Aprovado", "Recusado"]
        elif tipo_usuario == "Admin":
            status_opcoes = ["Concluído", "Em Análise", "Recusado"]
        else:
            status_opcoes = []

        if tipo_usuario != "Encarregado":
            status = st.selectbox("Status do Serviço", options=status_opcoes)

        else:
            status = "Pendente"

        # Botão de Atualização
        if st.button("Atualizar Serviço"):
            payload = {"observacoes": observacoes}

            # Atualizando o status se aplicável
            if status:
                #payload["status"] = status
                payload.update({"status": status})

            # Atualizando imagens novas apenas se houverem (Encarregado)
            if tipo_usuario == "Encarregado" and fotos_urls:
                #payload["fotos_urls"] = fotos_urls
                payload.update({"fotos_urls": fotos_urls})

            st.write(payload)
            token = st.session_state.get("token")
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.put(f"{API_BASE_URL}/servicos/{servico['id']}", json=payload, headers=headers)

            if response.status_code == 200:
                st.success("Serviço atualizado com sucesso!")
                callback_servicos()  # Recarregar lista de serviços
                st.session_state.pop("servico_selecionado")  # Limpar seleção após atualizar
            else:
                st.error("Erro ao atualizar o serviço.")

# ============ Interfaces de cada Usuário ============

# Admin
def menu_admin():
    st.title("Admin")

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
    st.title("Menu")
    acao = st.radio("Escolha uma página:", ["Atualizar Serviço", "Serviços Pendentes"])

    if acao == "Atualizar Serviço":
        update_servico()

    if acao == "Serviços Pendentes":
        show_servicos()

def menu_representante():
    st.title("Representante")
    
    show_servicos()