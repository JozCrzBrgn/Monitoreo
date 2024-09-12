
import streamlit as st
import streamlit_authenticator as stauth

import ConectorPython

from configuracion import config
from configuracion import read_json_from_supabase

st.set_page_config(
    page_title="Metas",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

#* USER AUTHENTICATION
credenciales = read_json_from_supabase(config.BUCKET_GENERAL, config.CREDENCIALES_FILE)
authenticator = stauth.Authenticate(
    credenciales,
    st.secrets["COOKIE_NAME"],
    st.secrets["COOKIE_KEY"],
    int(st.secrets["COOKIE_EXPIRY_DAYS"]),
)
name, authentication_status, username = authenticator.login()

if authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username ands password')
elif authentication_status:
    col1, col2 = st.columns([4,1])
    with col1:
        st.success('Bienvenido {}'.format(name))
    with col2:
        authenticator.logout('Logout', 'main')

    st.title("Test imprimir")

    def imprimir():
        nombreImpresora = "WL88S"
        conector = ConectorPython.ConectorV3(serial=config.SERIAL)
        conector.Iniciar()
        conector.EscribirTexto("Hola mundo")
        conector.Feed(1)
        conector.Corte(1)
        respuesta = conector.imprimirEn(nombreImpresora)
        return respuesta
    
    if st.button("Imprimir"):
        resultado = imprimir()
        st.write("Resultado de la impresión:", resultado)