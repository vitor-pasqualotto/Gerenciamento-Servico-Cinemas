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
                callback_empresas()
            if "cinemas" not in st.session_state:
                st.session_state.cinemas = {}
            if "salas" not in st.session_state:
                st.session_state.salas = {}
            if "usuarios" not in st.session_state:
                st.session_state.usuarios = {}
            if "usuario_especifico" not in st.session_state:
                st.session_state.usuario_especifico = {}
            if "servicos" not in st.session_state:
                st.session_state.servicos = {}

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
