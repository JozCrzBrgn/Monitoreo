
import streamlit as st
import streamlit_authenticator as stauth

from configuracion import config
from configuracion import read_json_from_supabase

from db_values import diccionario_categorias
from custom_widgets import subtitulos

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

    st.title("Pedidos por sucursal")

    productos_por_categoria = diccionario_categorias()
    total_sum = i = j = 0
    mi_values = []
    for category, value in productos_por_categoria.items():
        j+=1
        subtitulos(f"Categoria: {category}", "grey")
        for producto in value:
            i+=1
            mi_values.append(st.number_input(f"{producto}"))
        # Calcular la suma de los valores
        mi_value = sum(mi_values)
        total_sum += mi_value

    st.write("The total sum is:", total_sum)