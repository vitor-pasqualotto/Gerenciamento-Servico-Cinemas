from PIL import Image
import streamlit as st
import requests
import os

#API_BASE_URL = "http://localhost:8000"
API_BASE_URL = "https://gerenciamento-servico-cinemas-production.up.railway.app/" 

# ============ LOGIN ============

def login(): 
    """ Função para realizar Login """
    # Título
    st.header("Login")

    # Definindo Session State para dados do login
    if "email" not in st.session_state:
        st.session_state.email = ""

    if "senha" not in st.session_state:
        st.session_state.senha = ""

    # Inputs para logar
    email = st.text_input("Email", value=st.session_state.email)
    senha = st.text_input("Senha", type="password", value=st.session_state.senha)

    # Confirmação do login 
    if st.button("Entrar"): 
        data = {"username": email, "password": senha}

        # Recuperação do Token
        response = requests.post(f"{API_BASE_URL}/token", data=data)
        
        # Verifica Status Code e Atualização do Session State
        if response.status_code == 200:
            st.session_state.token = response.json().get("access_token")
            st.session_state.email = email
            st.session_state.senha = senha
            st.success("Login efetuado com sucesso!")

            # Força uma segunda execução
            st.rerun()

        else:
            # lança um erro
            st.sidebar.error("Erro no login. Verifique suas credenciais.")

def get_current_user(): 
    """ Função para pegar informações do usuário logado """

    # Busca token
    token = st.session_state.get("token")

    # Verifica se o token existe
    if not token:
        return None
    
    # Request para recuperar o usuário atual
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/usuarios/me", headers=headers)

    # Verifica o Status Code
    if response.status_code == 200:
        return response.json()
    
    return None 

# ============ CALLBACKS ============

def callback_empresas():
    """Recupera todas as empresas e retorna um dicionário {id: nome}."""
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe
    if not token:
        return None
    
    # Request para recuperar Empresas
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.get(f"{API_BASE_URL}/empresas/", headers=headers)

    # Verifica Status Code e Atualização do Session State
    if response.status_code == 200:
        empresas = response.json()
        st.session_state.empresas = {empresa['id']: empresa['nome'] for empresa in empresas}

    else:
        st.session_state.empresas = {}

def callback_cinemas():
    """Recupera todos os cinemas de uma empresa específica."""
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe
    if not token:
        return None

    # Request para recuperar Cinemas
    empresa_id = st.session_state.empresa_id
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.get(f"{API_BASE_URL}/cinemas/", headers=headers)

    # Verifica Status Code e Atualização do Session State
    if response.status_code == 200:
        cinemas = response.json()
        st.session_state.cinemas = {cinema['id']: cinema['nome'] for cinema in cinemas if cinema['empresa_id'] == empresa_id} 

    else:
        st.session_state.cinemas = {}

def callback_salas():
    """Recupera todas as salas de um cinema específico."""
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe
    if not token:
        return None
    
    # Request para recuperar Salas
    cinema_id = st.session_state.cinema_id
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.get(f"{API_BASE_URL}/salas/", headers=headers)

    # Verifica Status Code e Atualização do Session State
    if response.status_code == 200:
        salas = response.json()
        st.session_state.salas = {sala['id']: sala['nome'] for sala in salas if sala['cinema_id'] == cinema_id}

    else:
        st.session_state.salas = {}

def callback_usuarios():
    """Recupera todos os usuarios de um tipo específico."""
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe
    if not token:
        return None
    
    # Request para recuperar Usuarios
    tipo_usuario = st.session_state.tipo_usuario
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.get(f"{API_BASE_URL}/usuarios/", headers=headers)

    # Verifica Status Code e Atualização do Session State
    if response.status_code == 200:
        usuarios = response.json()
        st.session_state.usuarios = {usuario['id']: usuario['nome'] for usuario in usuarios if usuario['tipo_usuario'] == tipo_usuario}

    else:
        st.session_state.usuarios = {}

def callback_usuario_especifico():
    """Recupera um usuario específico."""
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe
    if not token:
        return None

    # Request para recuperar Usuarios Específico
    usuario_id = st.session_state.usuario_id
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.get(f"{API_BASE_URL}/usuarios/", headers=headers)

    # Verifica Status Code e Atualização do Session State
    if response.status_code == 200:
        usuarios = response.json()
        st.session_state.usuario_especifico = [usuario for usuario in usuarios if usuario["id"] == usuario_id]

    else:
        st.session_state.usuarios = {}

def callback_servicos():
    """Atualiza a lista de serviços com base no tipo de usuário logado."""
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe
    if not token:
        return None
    
    # Busca current user
    current_user = get_current_user()

    # Verifica se o current user existe
    if current_user:

        # Request para recuperar Serviços e Salas
        headers = {"Authorization": f"Bearer {token}"}
        response_servicos = requests.get(f"{API_BASE_URL}/servicos/", headers=headers)
        response_salas = requests.get(f"{API_BASE_URL}/salas", headers=headers)

        # Verifica Status Code 
        if response_servicos.status_code == 200 and response_salas.status_code == 200:
            todos_servicos = response_servicos.json()
            todas_salas = response_salas.json()

            # Filtrando serviços de acordo com o tipo de usuário
            if current_user["tipo_usuario"] == "Encarregado":

                # Busca somente serviços recusados que levam o id do encarregado logado
                servicos_filtrados = [servico for servico in todos_servicos if servico["status"] == "Recusado" and servico["encarregado_id"] == current_user["id"]]

            elif current_user["tipo_usuario"] == "Gerente":

                # Busca somente serviços pendentes do cinema do gerente logado
                servicos_filtrados = []

                for servico in todos_servicos:
                    if servico["status"] == "Pendente":
                        for sala in todas_salas:
                            if sala["id"] == servico["sala_id"]:
                                if sala["cinema_id"] == current_user["cinema_id"]:
                                    servicos_filtrados.append(servico)

            elif current_user["tipo_usuario"] == "Admin":

                # Busca somente serviços aprovados
                servicos_filtrados = [servico for servico in todos_servicos if servico["status"] == "Aprovado"]

            else:
                servicos_filtrados = []

            # Atualizando Session State
            st.session_state.servicos = servicos_filtrados

# ============ READ ============

def show_usuarios(): 
    """ Mostra todos os usuários """
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe e lança mensagem de erro
    if not token:
        st.error("Usuário não autenticado.")

    # Request para recuperar Usuarios Específico
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/usuarios/", headers=headers)

    # Verifica Status Code 
    if response.status_code == 200:
        registros = response.json()
        st.write("- Lista de Usuários")
        st.table(registros)

    else:
        st.error("Erro ao buscar usuários.")

def show_empresas(): 
    """ Mostra todas as empresas """
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe e lança mensagem de erro
    if not token:
        st.error("Usuário não autenticado.")

    # Request para recuperar Usuarios Específico
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/empresas/", headers=headers)

    # Verifica Status Code 
    if response.status_code == 200:
        registros = response.json()
        st.write("- Lista de Empresas")
        st.table(registros)

    else:
        st.error("Erro ao buscar empresas.")

def show_cinemas(): 
    """ Mostra todos os cinemas """
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe e lança mensagem de erro
    if not token:
        st.error("Usuário não autenticado.")

    # Request para recuperar Usuarios Específico
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/cinemas/", headers=headers)

    # Verifica Status Code 
    if response.status_code == 200:
        registros = response.json()
        st.write("- Lista de cinemas")
        st.table(registros)

    else:
        st.error("Erro ao buscar Cinemas.")

def show_salas():
    """ Mostra todas as salas """
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe e lança mensagem de erro
    if not token:
        st.error("Usuário não autenticado.")

    # Request para recuperar Usuarios Específico
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/salas/", headers=headers)

    # Verifica Status Code 
    if response.status_code == 200:
        registros = response.json()
        st.write("- Lista de Salas")
        st.table(registros)

    else:
        st.error("Erro ao buscar salas.")

def show_servicos(): 
    """ Mostra todos os serviços """
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe e lança mensagem de erro
    if not token:
        st.error("Usuário não autenticado.")

    # Request para recuperar Usuarios Específico
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/servicos/", headers=headers)

    # Verifica Status Code 
    if response.status_code == 200:
        registros = response.json()
        st.write("- Lista de Serviços")
        st.table(registros)

    else:
        st.error("Erro ao buscar serviços.")

def show_historico_status(): 
    """ Mostra todo o histórico de serviços """
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe e lança mensagem de erro
    if not token:
        st.error("Usuário não autenticado.")

    # Request para recuperar Usuarios Específico
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}/historico_status/", headers=headers)

    # Verifica Status Code 
    if response.status_code == 200:
        registros = response.json()
        st.write("- Histórico de Status de Serviços")
        st.table(registros)

    else:
        st.error("Erro ao buscar histórico de serviços.")

# ============ CREATE ============

def create_usuario():
    """ Criar novo usuário """
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe e lança mensagem de erro
    if not token:
        st.error("Usuário não autenticado.")

    # Criando headers
    headers = {"Authorization": f"Bearer {token}"}

    # Título
    st.header("Registrar Novo Usuário")

    # Inputs dispóníveis 
    options = ["Gerente", "Representante", "Encarregado"]
    nome_usuario = st.text_input("Nome do Usuário")
    email = st.text_input("Email Usuário")
    senha = st.text_input("Senha Usuário", type='password')
    tipo_usuario = st.selectbox("Tipo de Usuário", options=options)
    
    # Verifica se o tipo de usuário é gerente ou representante
    if tipo_usuario in ["Gerente", "Representante"]:
        empresas = {0: "Selecionar"} # Opções de empresas
        empresas.update(st.session_state.empresas)
        empresa = st.selectbox("Empresa", options=list(empresas.keys()), key="empresa_id", format_func=lambda x: empresas[x], on_change=callback_cinemas, index=0) # Callback para cinemas
        
        # Verifica se o tipo de usuário é gerente
        if tipo_usuario == "Gerente":
            cinemas = {0: "Selecionar"} # Opções de cinemas
            cinemas.update(st.session_state.cinemas)
            cinema = st.selectbox("Cinema", options=list(cinemas.keys()), format_func=lambda x: cinemas[x], index=0)

        else:
            cinema = None

    else:
        empresa, cinema = None, None

    # Verifica se o botão foi enviado
    if st.button("Registrar"):

        # Request para criar Usuario
        payload = {
            "nome": nome_usuario, 
            "email": email, "senha": senha, 
            "tipo_usuario": tipo_usuario, 
            "empresa_id": empresa, 
            "cinema_id": cinema
        }
        response = requests.post(f"{API_BASE_URL}/usuarios/", json=payload, headers=headers)

        # Verifica Status Code
        if response.status_code == 200:
            st.success("Usuário registrado com sucesso!") 

        else:
            st.error("Erro ao registrar o usuário.")

def create_empresa():
    """ Criar nova empresa """
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe e lança mensagem de erro
    if not token:
        st.error("Usuário não autenticado.")

    # Criando headers
    headers = {"Authorization": f"Bearer {token}"}

    # Título
    st.header("Registrar Nova Empresa")

    # Inputs dispóníveis 
    nome_empresa = st.text_input("Nome da Empresa")
    cnpj = st.text_input("CNPJ da Empresa", placeholder="XX.XXX.XXX/0001-XX")
    contato = st.text_input("Email da Empresa", placeholder="exemplo@dominio.com")

    # Verifica se o botão foi enviado
    if st.button("Registrar"):
        
        # Request para criar Empresa
        payload = {
            "nome": nome_empresa,
            "cnpj": cnpj,
            "contato": contato
        }
        response = requests.post(f"{API_BASE_URL}/empresas/", json=payload, headers=headers)

        # Verifica Status Code
        if response.status_code == 200:
            st.success("Empresa registrada com sucesso!")

        else:
            st.error("Erro ao registrar a empresa.")

def create_cinema():
    """ Criar novo cinema """
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe e lança mensagem de erro
    if not token:
        st.error("Usuário não autenticado.")

    # Criando headers
    headers = {"Authorization": f"Bearer {token}"}

    # Título
    st.header("Registrar Novo Cinema")

    # Inputs dispóníveis
    empresas = {0: "Selecionar"} # Opções de empresas
    empresas.update(st.session_state.empresas)
    empresa = st.selectbox("Selecione a Empresa", options=list(empresas.keys()), key="empresa_id", format_func=lambda x: empresas[x], on_change=callback_cinemas, index=0) # Callback para cinemas

    # Verifica se a empresa foi enviada
    if empresa and empresa != "Selecionar":

        nome_cinema = st.text_input("Nome do Cinema")
        endereco = st.text_input("Endereço do Cinema")

        # Verifica se o botão foi enviado
        if st.button("Registrar"):

            # Request para criar Cinema
            payload = {
                "nome": nome_cinema,
                "endereco": endereco,
                "empresa_id": empresa
            }
            response = requests.post(f"{API_BASE_URL}/cinemas/", json=payload, headers=headers)

            # Verifica Status Code
            if response.status_code == 200:
                st.success("Cinema registrado com sucesso!")

            else:
                st.error("Erro ao registrar o cinema.")

def create_sala():
    """ Criar nova sala """
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe e lança mensagem de erro
    if not token:
        st.error("Usuário não autenticado.")

    # Criando headers
    headers = {"Authorization": f"Bearer {token}"}

    # Título
    st.header("Registrar Nova Sala")

    # Inputs dispóníveis
    empresas = {0: "Selecionar"} # Opções de empresas
    empresas.update(st.session_state.empresas)
    empresa = st.selectbox("Selecione a Empresa", options=list(empresas.keys()), key="empresa_id", format_func=lambda x: empresas[x], on_change=callback_cinemas, index=0) # Callback para cinemas
    
    # Verifica se a empresa foi enviada
    if empresa and empresa != "Selecionar":
        cinemas = {0: "Selecionar"} # Opções de cinemas
        cinemas.update(st.session_state.cinemas)
        cinema = st.selectbox("Cinema", options=list(cinemas.keys()), key="cinema_id", format_func=lambda x: cinemas[x], on_change=callback_salas, index=0) # Callback para salas
        
        # Verifica se o cinema foi enviado
        if cinema and cinema != "Selecionar":
            st.write("Salas Existentes")

            # Percorre as salas e mostra o nome de cada uma
            for n in range(len(st.session_state.salas)):
                st.write(st.session_state.salas[n+1])

            nome_sala = st.text_input("Nome da Sala")

            # Verifica se o botão foi enviado
            if st.button("Registrar"):

                # Request para criar Sala
                payload = {
                    "nome": nome_sala,
                    "cinema_id": cinema
                }
                response = requests.post(f"{API_BASE_URL}/salas/", json=payload, headers=headers)

                # Verifica Status Code
                if response.status_code == 200:
                    st.success("Sala registrada com sucesso!")

                else:
                    st.error("Erro ao registrar a sala.")

# ========== Criação def necessáriA para create_servico =============

def save_uploaded_file(uploaded_file, folder="../static/uploads/"):
    """ Recebe a foto e armazena """
    # Verifica se o folder já existe antes de criar
    if not os.path.exists(folder):  
        os.makedirs(folder)

    # Define o path da foto
    file_path = os.path.join(folder, uploaded_file.name)

    # Armazena a foto no folder certo
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    # Retorna o caminho da foto
    return file_path

# ===================================================================

def create_servico():
    """ Criar novo serviço """
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe e lança mensagem de erro
    if not token:
        st.error("Usuário não autenticado.")

    # Criando headers
    headers = {"Authorization": f"Bearer {token}"}

    # Título
    st.header("Registrar Novo Serviço")

    # Inputs dispóníveis
    empresas = {0: "Selecionar"} # Opções de empresas
    empresas.update(st.session_state.empresas)
    empresa = st.selectbox("Selecione a Empresa", options=list(empresas.keys()), key="empresa_id", format_func=lambda x: empresas[x], on_change=callback_cinemas, index=0) # Callback para cinemas
    
    # Verifica se a empresa foi enviada
    if empresa and empresa != "Selecionar":
        cinemas = {0: "Selecionar"} # Opções de cinemas
        cinemas.update(st.session_state.cinemas)
        cinema = st.selectbox("Cinema", options=list(cinemas.keys()), key="cinema_id", format_func=lambda x: cinemas[x], on_change=callback_salas, index=0) # Callback para salas
        
        # Verifica se o cinema foi enviado
        if cinema and cinema != "Selecionar":
            salas = {0: "Selecionar"} # Opções de salas
            salas.update(st.session_state.salas)
            sala = st.selectbox("Salas", options=list(salas.keys()), key="sala_id", format_func=lambda x: salas[x], index=0)

            # Verifica se a sala foi enviada
            if sala and sala != "Selecionar":
                encarregado_id = requests.get(f"{API_BASE_URL}/usuarios/me", headers=headers).json()["id"]
                tipo_servico = st.selectbox("Tipo de Serviço", options=["Limpeza de Carpete", "Limpeza de Tela", "Limpeza de Cortinas"])

                # Input para fotos
                uploaded_files = st.file_uploader("Envie as Fotos", accept_multiple_files=True)

                # Verifica se as fotos foram enviadas
                if uploaded_files:
                    st.write(f"Foram carregadas {len(uploaded_files)} imagens.") # Exibe quantidade de fotos

                    fotos_urls = []

                    # Percorre fotos, salva, exibe e adiciona o path na lista
                    for uploaded_file in uploaded_files:
                        file_path = save_uploaded_file(uploaded_file)
                        image = Image.open(file_path)
                        st.image(image, caption=uploaded_file.name, use_container_width=True)
                        fotos_urls.append(file_path)

                    observacoes = st.text_area("Observações")

                    # Verifica se as observações foram enviadas
                    if observacoes:

                        # Verifica se o botão foi enviado
                        if st.button("Registrar"):

                            # Request para criar Serviço
                            payload = {
                                "encarregado_id": encarregado_id,
                                "sala_id": sala,
                                "tipo_servico": tipo_servico,
                                "observacoes": observacoes,
                                "fotos_urls": fotos_urls
                            }
                            response = requests.post(f"{API_BASE_URL}/servicos/", json=payload, headers=headers)

                            # Verifica Status Code
                            if response.status_code == 200:
                                st.success("Serviço registrado com sucesso!")

                            else:
                                st.error("Erro ao registrar o serviço.")

# ============ UPDATE ============

def update_usuario():
    """ Atualizar usuário """
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe e lança mensagem de erro
    if not token:
        st.error("Usuário não autenticado.")

    # Criando headers
    headers = {"Authorization": f"Bearer {token}"}

    # Título
    st.header("Editar Usuário")
    
    # Recuperando todos os tipos de usuários para adicionar ao dropdown
    options_tipo = ["Selecionar", "Gerente", "Representante", "Encarregado"]

    # Inputs dispóníveis
    tipo_usuario = st.selectbox("Selecione o Tipo de Usuário", options=options_tipo, key="tipo_usuario", on_change=callback_usuarios) # Callback para usuarios

    # Verifica se o tipo_usuario foi enviado
    if tipo_usuario and tipo_usuario != "Selecionar":
        usuarios = {0: "Selecionar"}
        usuarios.update(st.session_state.usuarios)
        usuario = st.selectbox("Selecione o Usuário", options=list(usuarios.keys()), key="usuario_id", format_func=lambda x: usuarios[x], on_change=callback_usuario_especifico, index=0) # Callback para usuario_especifico

        # Verifica se o usuario foi enviado
        if usuario and usuario != 0:
            st.write(f"Nome: {st.session_state.usuario_especifico[0]["nome"]}")
            st.write(f"Email: {st.session_state.usuario_especifico[0]["email"]}")
            
            nome_update = st.text_input("Digite o Nome Para Alteração")
            email_update = st.text_input("Digite o Email Para Alteração")
            senha_update = st.text_input("Digite a Senha Para Alteração", type="password")

            # Recuperando empresa_id e cinema_id do usuário selecionado
            empresa = st.session_state.usuario_especifico[0]["empresa_id"]
            cinema = st.session_state.usuario_especifico[0]["cinema_id"]

            # Verifica se o botão foi enviado
            if st.button("Atualizar"):

                # Request para atualizar Usuário
                payload = {
                    "nome": nome_update,
                    "email": email_update,
                    "senha": senha_update,
                    "tipo_usuario": tipo_usuario,
                    "empresa_id": empresa,
                    "cinema_id": cinema
                }
                response = requests.put(f"{API_BASE_URL}/usuarios/{usuario}", json=payload, headers=headers)

                # Verifica Status Code
                if response.status_code == 200:
                    st.success("Usuário Atualizado com sucesso!")

                else:
                    st.error("Erro ao Atualizar o usuário.")


def update_empresa():
    """ Atualizar empresa """
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe e lança mensagem de erro
    if not token:
        st.error("Usuário não autenticado.")

    # Criando headers
    headers = {"Authorization": f"Bearer {token}"}

    # Título
    st.header("Registrar Novo Serviço")

    # Inputs dispóníveis
    empresas = {0: "Selecionar"} # Opções de empresas
    empresas.update(st.session_state.empresas)
    empresa = st.selectbox("Selecione a Empresa", options=list(empresas.keys()), key="empresa_id", format_func=lambda x: empresas[x], index=0)

    # Verifica se a empresa foi enviada
    if empresa and empresa != "Selecionar":
        nome = st.text_input("Digite o Nome da Empresa")
        cnpj = st.text_input("CNPJ da Empresa", placeholder="XX.XXX.XXX/0001-XX")
        contato = st.text_input("Email da Empresa", placeholder="exemplo@dominio.com")

        # Verifica se o botão foi enviado
        if st.button("Registrar"):

            # Request para atualizar Empresa
            payload = {
                "nome": nome,
                "cnpj": cnpj,
                "contato": contato
            }
            response = requests.put(f"{API_BASE_URL}/empresas/{empresa}", json=payload, headers=headers)

            # Verifica Status Code
            if response.status_code == 200:
                st.success("Empresa Atualizada com sucesso!")

            else:
                st.error("Erro ao Atualizar a empresa.")

def update_cinema():
    """ Atualizar cinema """
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe e lança mensagem de erro
    if not token:
        st.error("Usuário não autenticado.")

    # Criando headers
    headers = {"Authorization": f"Bearer {token}"}

    # Título
    st.header("Atuaizar Cinema")

    # Inputs dispóníveis
    empresas = {0: "Selecionar"} # Opções de empresas
    empresas.update(st.session_state.empresas)
    empresa = st.selectbox("Selecione a Empresa", options=list(empresas.keys()), key="empresa_id", format_func=lambda x: empresas[x], on_change=callback_cinemas, index=0) # Callback para cinemas
    
    # Verifica se a empresa foi enviada
    if empresa and empresa != "Selecionar":
        cinemas = {0: "Selecionar"}
        cinemas.update(st.session_state.cinemas)
        cinema = st.selectbox("Cinema", options=list(cinemas.keys()), key="cinema_id", format_func=lambda x: cinemas[x], on_change=callback_salas, index=0) # Callback para salas

        # Verifica se o cinema foi enviado
        if cinema and cinemas != "Selecionar":
            nome = st.text_input("Digite o Nome Para Alteração")
            endereco = st.text_input("Digite o Endereço Para Alteração")

            # Verifica se o botão foi enviado
            if st.button("Registrar"):

                # Request para atualizar Cinema
                payload = {
                    "nome": nome,
                    "endereco": endereco,
                    "empresa_id": empresa
                }
                response = requests.put(f"{API_BASE_URL}/cinemas/{cinema}", json=payload, headers=headers)

                # Verifica Status Code
                if response.status_code == 200:
                    st.success("Empresa Atualizada com sucesso!")

                else:
                    st.error("Erro ao Atualizar a empresa.")

def update_sala():
    """ Atualizar sala """
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe e lança mensagem de erro
    if not token:
        st.error("Usuário não autenticado.")

    # Criando headers
    headers = {"Authorization": f"Bearer {token}"}

    # Título
    st.header("Editar Sala")

    # Inputs dispóníveis
    empresas = {0: "Selecionar"} # Opções de empresas
    empresas.update(st.session_state.empresas)
    empresa = st.selectbox("Selecione a Empresa", options=list(empresas.keys()), key="empresa_id", format_func=lambda x: empresas[x], on_change=callback_cinemas, index=0)
    
    # Verifica se a empresa foi enviada
    if empresa and empresa != "Selecionar":
        cinemas = {0: "Selecionar"}
        cinemas.update(st.session_state.cinemas)
        cinema = st.selectbox("Cinema", options=list(cinemas.keys()), key="cinema_id", format_func=lambda x: cinemas[x], on_change=callback_salas, index=0)

        # Verifica se o empreso foi enviado
        if cinema and cinema != "Selecionar":
            salas = {0: "Selecionar"}
            salas.update(st.session_state.salas)
            sala = st.selectbox("Salas", options=list(salas.keys()), key="sala_id", format_func=lambda x: salas[x], index=0)

            # Verifica se a sala foi enviada
            if sala and sala != "Selecionar":
                nome = st.text_input("Digite o nome para alteração")

                # Verifica se o botão foi enviado
                if st.button("Registrar"):

                    # Request para atualizar Sala
                    payload = {
                        "nome": nome,
                        "ciniema_id": cinema
                    }
                    response = requests.put(f"{API_BASE_URL}/salas/{sala}", json=payload, headers=headers)

                    # Verifica Status Code
                    if response.status_code == 200:
                        st.success("Sala Atualizada com sucesso!")

                    else:
                        st.error("Erro ao Atualizar a Sala.")

def update_servico():
    """ Atualizar serviço """
    # Busca token
    token = st.session_state.get("token")

    # Verfica se o token existe e lança mensagem de erro
    if not token:
        st.error("Usuário não autenticado.")

    # Criando headers
    headers = {"Authorization": f"Bearer {token}"}

    # Título
    st.header("Atualizar Serviço")

    # Pegando dados do usuário logado
    current_user = get_current_user()
    tipo_usuario = current_user["tipo_usuario"]
    
    # Chama callback_servicos
    callback_servicos()
    st.write(st.session_state.servicos) # *************** DEBUG ***************

    # Exibir serviços em forma de botões clicáveis
    servicos = st.session_state.servicos

    # Verfica se os serviços existem e lança mensagem de erro
    if not servicos:
        st.error("Nenhum serviço disponível para atualização.")

    # Título para selecionar um serviço
    st.subheader("Selecione um serviço para editar:")
    
    # Percorre os serviços e mostra cada um dentro de um botão
    for servico in servicos:
        if st.button(f"📌 {servico['id']} - {servico['tipo_servico']} - {servico['status']}", key=f"btn_{servico['id']}"):
            st.session_state.servico_selecionado = servico

    # Exibir detalhes do serviço selecionado
    if "servico_selecionado" in st.session_state:
        servico = st.session_state.servico_selecionado
        st.subheader(f"Editando Serviço: 📌 {servico['id']} - {servico['tipo_servico']} - {servico['status']}")
        st.write(f"Observações: {servico['observacoes'] or 'Nenhuma observação registrada'}")

        # Buscar imagens associadas ao serviço
        response_fotos = requests.get(f"{API_BASE_URL}/imagens", headers={"Authorization": f"Bearer {st.session_state.get('token')}"})
        fotos = response_fotos.json() if response_fotos.status_code == 200 else []

        # Exibir imagens do serviço percorrendo
        st.subheader("📷 Fotos do Serviço:")
        for foto in fotos:
            if foto["servico_id"] == servico["id"] and os.path.exists(foto['url_foto']):
                image = Image.open(f"{foto['url_foto']}")
                st.image(image, caption="Imagem do Serviço", use_container_width=True)

        # Upload de novas imagens (Apenas para Encarregados)
        if tipo_usuario == "Encarregado":
            uploaded_files = st.file_uploader("Envie novas imagens (substituirá as antigas)", accept_multiple_files=True)

            # Verifica se as fotos foram enviadas
            if uploaded_files:

                # Removendo imagens antigas
                for foto in fotos:
                    if foto["servico_id"] == servico["id"]:
                        old_path = f"{foto['url_foto']}"
                        if os.path.exists(old_path):
                            os.remove(old_path)

                # Exibe a quantidade de fotos
                st.write(f"Foram carregadas {len(uploaded_files)} imagens.")

                fotos_urls = []
                
                # Percorre fotos, salva, exibe e adiciona o path na lista
                for uploaded_file in uploaded_files:
                    file_path = save_uploaded_file(uploaded_file)
                    image = Image.open(file_path)
                    st.image(image, caption=uploaded_file.name, use_container_width=True)
                    fotos_urls.append(file_path)
        
        observacoes = st.text_area("Escreva as Observações")

        # Seleção de Status (Dependendo do Tipo de Usuário)
        if tipo_usuario == "Gerente":
            status_opcoes = ["Aprovado", "Recusado"]
        elif tipo_usuario == "Admin":
            status_opcoes = ["Concluído", "Em Análise", "Recusado"]
        else:
            status_opcoes = []

        # Se for diferente de encarregado exibe opção para alterar o status 
        if tipo_usuario != "Encarregado":
            status = st.selectbox("Status do Serviço", options=status_opcoes)

        # Se for encarregado define um valor automaticamente
        else:
            status = "Pendente"

        # Verifica se o botão foi enviado
        if st.button("Atualizar Serviço"):
            payload = {"observacoes": observacoes}

            # Atualizando o status se aplicável
            if status:
                payload.update({"status": status})

            # Atualizando imagens novas apenas se houverem (Encarregado)
            if tipo_usuario == "Encarregado" and fotos_urls:
                payload.update({"fotos_urls": fotos_urls})

            # Request para atualizar Serviço
            response = requests.put(f"{API_BASE_URL}/servicos/{servico['id']}", json=payload, headers=headers)

            # Verifica Status Code
            if response.status_code == 200:
                st.success("Serviço atualizado com sucesso!")
                callback_servicos()  # Recarregar lista de serviços
                st.session_state.pop("servico_selecionado")  # Limpar seleção após atualizar

            else:
                st.error("Erro ao atualizar o serviço.")

# ============ Interfaces de cada Usuário ============

# Admin
def menu_admin():
    """ Menu admin """
    # Título 
    st.title("Admin")

    # Verifica se página já existe no Session State
    if "pagina" not in st.session_state:
        st.session_state.pagina = "Dashboard"

    # Menu para o admin navegar 
    with st.sidebar:
        st.title("Menu")
        pagina = st.radio("Escolha uma página:", ["Dashboard", "Empresas", "Cinemas", "Salas", "Serviços", "Usuários"])

    # Define página no Session State
    st.session_state.pagina = pagina

    if st.session_state.pagina == "Dashboard":
        st.title("Em desenvolvimento...")

    # Se escolher Empresas
    if st.session_state.pagina == "Empresas":
        st.title("Empresas")
        acao = st.radio("Escolha a ação que deseja realizar:", ["Criar Empresa", "Atualizar Empresa", "Listar Empresas"])

        if acao == "Criar Empresa":
            create_empresa()

        if acao == "Atualizar Empresa":
            update_empresa()

        if acao == "Listar Empresas":
            show_empresas()

    # Se escolher Cinemas
    if st.session_state.pagina == "Cinemas":
        st.title("Cinemas")
        acao = st.radio("Escolha a ação que deseja realizar:", ["Criar Cinema", "Atualizar Cinema", "Listar Cinemas"])

        if acao == "Criar Cinema":
            create_cinema()

        if acao == "Atualizar Cinema":
            update_cinema()

        if acao == "Listar Cinemas":
            show_cinemas()

    # Se escolher Salas
    if st.session_state.pagina == "Salas":
        st.title("Salas")
        acao = st.radio("Escolha a ação que deseja realizar:", ["Criar Sala", "Atualizar Sala", "Listar Salas"])

        if acao == "Criar Sala":
            create_sala()

        if acao == "Atualizar Sala":
            update_sala()

        if acao == "Listar Salas":
            show_salas()

    # Se escolher Serviços
    if st.session_state.pagina == "Serviços":
        st.title("Serviços")
        acao = st.radio("Escolha a ação que deseja realizar:", ["Criar Serviço", "Atualizar Serviço", "Listar Serviços"])

        if acao == "Criar Serviço":
            create_servico()

        if acao == "Atualizar Serviço":
            update_servico()

        if acao == "Listar Serviços":
            show_servicos()

    # Se escolher Usuários 
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
    """ Menu encarregado """
    # Título
    st.title("Encarregado")

    acao = st.radio("Escolha uma página:", ["Registrar Serviço", "Atualizar Serviço", "Serviços Recusados"])

    if acao == "Registrar Serviço":
        create_servico()

    if acao == "Atualizar Serviço":
        update_servico()

    if acao == "Serviços Recusados":
        show_servicos()

def menu_gerente():
    """ Menu gerente """
    # Título
    st.title("Gerente")

    acao = st.radio("Escolha uma página:", ["Atualizar Serviço", "Serviços Pendentes"])

    if acao == "Atualizar Serviço":
        update_servico()

    if acao == "Serviços Pendentes":
        show_servicos()

def menu_representante():
    """ Menu representante """
    # Título
    st.title("Representante")
    
    show_servicos()