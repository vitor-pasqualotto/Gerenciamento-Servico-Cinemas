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
            st.write(user.get("nome"))
            tipo_usuario = user.get("tipo_usuario")

            if tipo_usuario == "Admin":
                menu_admin()

            if tipo_usuario == "Encarregado":
                menu_encarregado()

            if tipo_usuario == "Gerente":
                menu_gerente()

        else:
            st.erro("Não foi possível obter as informações do usuário")
            st.stop()

if __name__ == "__main__":
    main()
