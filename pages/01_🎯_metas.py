
import streamlit as st
import streamlit_authenticator as stauth

import pandas as pd
import numpy as np

from configuracion import config
from configuracion import read_json_from_supabase
from custom_widgets import subtitulos, meta, grafico_barras, grafico_velocimetro

from db_values import metas_sucursales, ventas_sucursales

st.set_page_config(
    page_title="Metas por Sucursales",
    page_icon="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjgiIGhlaWdodD0iMTI4IiB2aWV3Qm94PSIwIDAgMTAyIDEwMiI+PGRlZnM+PHBhdGggaWQ9Ikljb25pZnlJZDE5MTQwNDZhNzg0ZGJmYjdkMCIgZmlsbD0iI0YwQzQxOSIgZD0iTTg5IDc0SDc2bDEzIDEzaDEzeiIvPjwvZGVmcz48Y2lyY2xlIGN4PSI1MCIgY3k9IjUyIiByPSI1MCIgb3BhY2l0eT0iLjE1Ii8+PGNpcmNsZSBjeD0iNTIiIGN5PSI1MCIgcj0iNTAiIGZpbGw9IiMzQjk3RDMiLz48cGF0aCBmaWxsPSIjZmZmIiBkPSJNNTIgMTBjMjIuMDkxIDAgNDAgMTcuOTA5IDQwIDQwUzc0LjA5MSA5MCA1MiA5MFMxMiA3Mi4wOTEgMTIgNTBzMTcuOTA5LTQwIDQwLTQwIi8+PHBhdGggZmlsbD0iIzZCQzhGMiIgZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNNTIgMjBjMTYuNTY5IDAgMzAgMTMuNDMxIDMwIDMwYzAgMTYuNTY4LTEzLjQzMSAzMC0zMCAzMGMtMTYuNTY5IDAtMzAtMTMuNDMyLTMwLTMwYzAtMTYuNTY5IDEzLjQzMS0zMCAzMC0zMCIgY2xpcC1ydWxlPSJldmVub2RkIi8+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTUyIDMwYzExLjA0NiAwIDIwIDguOTU1IDIwIDIwcy04Ljk1NCAyMC0yMCAyMHMtMjAtOC45NTUtMjAtMjBzOC45NTQtMjAgMjAtMjAiLz48cGF0aCBmaWxsPSIjRTY0QzNDIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik01MiA0MGM1LjUyMyAwIDEwIDQuNDc3IDEwIDEwYzAgNS41MjItNC40NzcgMTAtMTAgMTBzLTEwLTQuNDc4LTEwLTEwYzAtNS41MjMgNC40NzctMTAgMTAtMTAiIGNsaXAtcnVsZT0iZXZlbm9kZCIvPjx1c2UgaHJlZj0iI0ljb25pZnlJZDE5MTQwNDZhNzg0ZGJmYjdkMCIgZmlsbC1ydWxlPSJldmVub2RkIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiLz48cGF0aCBmaWxsPSIjRjI5QzFGIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik04OSAxMDBWODdMNzYgNzR2MTN6IiBjbGlwLXJ1bGU9ImV2ZW5vZGQiLz48dXNlIGhyZWY9IiNJY29uaWZ5SWQxOTE0MDQ2YTc4NGRiZmI3ZDAiIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIi8+PHBhdGggZD0iTTUwLjQzOSA0OC40MzlMMTUuMTIxIDgzLjc1N2E1MC41MTMgNTAuNTEzIDAgMCAwIDIuMDk3IDIuMTQ1TDUyLjU2IDUwLjU2YTEuNSAxLjUgMCAxIDAtMi4xMjEtMi4xMjEiIG9wYWNpdHk9Ii4xNSIvPjxwYXRoIGZpbGw9IiNFNTdFMjUiIGQ9Ik05MC4zNjMgODkuODk2Yy0uMzg0IDAtLjc2OS0uMTQ2LTEuMDYyLS40MzlMNTAuOTM5IDUxLjA2MWExLjUwMSAxLjUwMSAwIDAgMSAyLjEyMy0yLjEyMWwzOC4zNjMgMzguMzk1YTEuNTAxIDEuNTAxIDAgMCAxLTEuMDYyIDIuNTYxIi8+PC9zdmc+",
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


#* PROCESAMIENTO DE DATOS
if authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username ands password')
elif authentication_status:
    #? Datos de la DB
    metas_dic = metas_sucursales()
    ventas_df_dic, ventas_sum_dic = ventas_sucursales()


    #? Renderizacion de elementos de Bienvenida
    col1, col2 = st.columns([4,1])
    with col1:
        st.success('Bienvenido {}'.format(name))
    with col2:
        authenticator.logout('Logout', 'main')

    subtitulos("Metas por sucursales", "white", "center", 40)

    #? Renderizacion de widgets

    #* ###################
    #* AGRICOLA ORIENTAL #
    #* ###################
    subtitulos("Agrícola Oriental", "grey")
    col1_1, col1_2  = st.columns([2,1])
    with col1_1:
        # Marcador de métas
        meta(metas_dic['Agri'], int(ventas_sum_dic['Agri']-metas_dic['Agri']))
        # Ventas por día
        grafico_barras(ventas_df_dic['Agri'])
    with col1_2:
        # Meta a alcanzar
        grafico_velocimetro(ventas_sum_dic['Agri'], metas_dic['Agri'])
    
    #* ################
    #* NEZAHUALCOYOTL #
    #* ################
    subtitulos("Nezahualcóyotl", "grey")
    col1_3, col1_4  = st.columns([2,1])
    with col1_3:
        # Marcador de métas
        meta(metas_dic['Neza'], int(ventas_sum_dic['Neza']-metas_dic['Neza']))
        # Ventas por día
        grafico_barras(ventas_df_dic['Neza'])
    with col1_4:
        # Meta a alcanzar
        grafico_velocimetro(ventas_sum_dic['Neza'], metas_dic['Neza'])

    #* ############
    #* ZAPOTITLAN #
    #* ############
    subtitulos("Zapotitlán", "grey")
    col1_5, col1_6  = st.columns([2,1])
    with col1_5:
        # Marcador de métas
        meta(metas_dic['Zapo'], int(ventas_sum_dic['Zapo']-metas_dic['Zapo']))
        # Ventas por día
        grafico_barras(ventas_df_dic['Zapo'])
    with col1_6:
        # Meta a alcanzar
        grafico_velocimetro(ventas_sum_dic['Zapo'], metas_dic['Zapo'])

    #* ##########
    #* OAXTEPEC #
    #* ##########
    subtitulos("Oaxtepec", "grey")
    col1_7, col1_8  = st.columns([2,1])
    with col1_7:
        # Marcador de métas
        meta(metas_dic['Oaxte'], int(ventas_sum_dic['Oaxte']-metas_dic['Oaxte']))
        # Ventas por día
        grafico_barras(ventas_df_dic['Oaxte'])
    with col1_8:
        # Meta a alcanzar
        grafico_velocimetro(ventas_sum_dic['Oaxte'], metas_dic['Oaxte'])

    #* ###########
    #* PANTITLAN #
    #* ###########
    subtitulos("Pantitlán", "grey")
    col1_9, col1_10  = st.columns([2,1])
    with col1_9:
        # Marcador de métas
        meta(metas_dic['Panti'], int(ventas_sum_dic['Panti']-metas_dic['Panti']))
        # Ventas por día
        grafico_barras(ventas_df_dic['Panti'])
    with col1_10:
        # Meta a alcanzar
        grafico_velocimetro(ventas_sum_dic['Panti'], metas_dic['Panti'])