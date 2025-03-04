from functions import *
import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"

# ============ APLICAÇÃO PRINCIPAL ============

def main():
    
    if "token" not in st.session_state:
        login()

    else:
        user = get_current_user()
        if user:
            # Inicializa session state se necessário
            if "empresas" not in st.session_state:
                st.session_state.empresas = fetch_empresas()
            if "cinemas" not in st.session_state:
                st.session_state.cinemas = {}
            if "salas" not in st.session_state:
                st.session_state.salas = {}
            if "usuario_id" not in st.session_state:
                st.session_state.usuario_id = requests.get(f"{API_BASE_URL}/usuarios/me", headers={"Authorization": f"Bearer {st.session_state.get('token')}"}).json().get("id", None)

            st.write(user.get("nome"))
            tipo_usuario = user.get("tipo_usuario")

            menus = {
                "Admin": menu_admin,
                "Encarregado": menu_encarregado,
                "Gerente": menu_gerente,
                "Representante": menu_representante
            }

            if tipo_usuario in menus:
                menus[tipo_usuario]()  # Chama o menu correto dinamicamente

        else:
            st.error("Não foi possível obter as informações do usuário")
            st.stop()

if __name__ == "__main__":
    main()
