
import streamlit as st
import streamlit_authenticator as stauth

from configuracion import config
from configuracion import read_json_from_supabase

from db_values import diccionario_categorias
from custom_widgets import subtitulos
from pdf import descargar_pdf

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
    total_sum = 0
    productos_con_valor_mayor_a_cero = []

    for category, productos in productos_por_categoria.items():
        st.subheader(f"Categoría: {category}")
        mi_values = []  # Lista para almacenar los valores ingresados por producto en cada categoría
        for producto in productos:
            valor_producto = st.number_input(f"{producto}", min_value=0, step=1)
            if valor_producto > 0:
                productos_con_valor_mayor_a_cero.append([producto, valor_producto])
            mi_values.append(valor_producto)

        # Calcular la suma de los valores de esta categoría
        mi_value = sum(mi_values)
        total_sum += mi_value

    # Mostrar la suma total
    st.write("La suma total es:", total_sum)

    # Mostrar productos con valor mayor a cero
    if productos_con_valor_mayor_a_cero:
        st.write("Productos con valor mayor a cero:", productos_con_valor_mayor_a_cero)
        nombre_sucursal = st.selectbox(
            "Sucursal",
            ("Agricola Oriental", "Nezahualcóyotl", "Zapotitlan", "Oaxtepec", "Pantitlan"),
        )

        fecha_pedido = st.date_input("Fecha de pedido")
        fecha_pedido_str = fecha_pedido.strftime("%Y-%m-%d")

        fecha_entrega = st.date_input("Fecha de entrega")
        fecha_entrega_str = fecha_entrega.strftime("%Y-%m-%d")

        clave ='XX0001'

        pdf_data = descargar_pdf(nombre_sucursal, clave, fecha_pedido_str, fecha_entrega_str, productos_con_valor_mayor_a_cero)
        st.download_button(
            label="Descargar PDF",
            data=pdf_data,
            file_name=f"Pedido_{clave}_{fecha_pedido}.pdf",
            mime="application/pdf"
        )
    else:
        st.write("No hay productos con valor mayor a cero.")
