from functions import *
import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"

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
