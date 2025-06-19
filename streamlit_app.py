import streamlit as st
import requests

client_id = "plus.do.brasil8567"
client_secret = "SEU_CLIENT_SECRET"
redirect_uri = "https://plusdobrasil.streamlit.app"

query_params = st.query_params
code = query_params.get("code", [None])[0]

if code:
    st.success("Código recebido. Trocando por token...")

    # 1. Troca o code pelo access_token
    token_url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri
    }

    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        st.success("Autenticado com sucesso!")

        # 2. Aqui você coloca a consulta de dados do usuário
        headers = {"Authorization": f"Bearer {access_token}"}
        usuario = requests.get("https://api.mercadolibre.com/users/me", headers=headers).json()

        st.subheader("👤 Dados do vendedor:")
        st.write(f"Nome: {usuario.get('first_name')} {usuario.get('last_name')}")
        st.write(f"Nickname: {usuario.get('nickname')}")
        st.write(f"ID: {usuario.get('id')}")
        st.write(f"E‑mail: {usuario.get('email', 'Não disponível')}")
    else:
        st.error("Erro ao obter token.")
else:
    auth_url = f"https://auth.mercadolivre.com.br/authorization?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
    st.markdown(f"[🔐 Clique aqui para autorizar com sua conta do Mercado Livre]({auth_url})")
