import streamlit as st
import requests
from urllib.parse import urlparse, parse_qs

st.title("🔐 Login com Mercado Livre")

# Pegamos o código da URL se existir
query_params = st.experimental_get_query_params()
code = query_params.get("code", [None])[0]

client_id = "SEU_CLIENT_ID"
client_secret = "SEU_CLIENT_SECRET"
redirect_uri = "https://plusdobrasil.streamlit.app"

if code:
    st.success("Código de autorização recebido!")
    # Troca o code pelo access_token
    url_token = "https://api.mercadolibre.com/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri
    }

    response = requests.post(url_token, data=payload)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        st.success(f"Token de acesso: {access_token}")
    else:
        st.error("Erro ao obter o token.")
else:
    # Gera link de autorização
    auth_url = f"https://auth.mercadolivre.com.br/authorization?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
    st.markdown(f"[Clique aqui para autorizar o app com sua conta Mercado Livre]({auth_url})")
