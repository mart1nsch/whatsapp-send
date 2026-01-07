import streamlit as st
import pandas as pd
import pywhatkit as kit
import time
import random

def config_inicias() -> None:
    st.set_page_config(page_title='WhatsApp Send', page_icon=':mailbox:')
    st.markdown('### Sender automático de mensagens para o WhatsApp')

def trata_dados(df:pd.DataFrame) -> list:
    df = df.dropna(subset=['Unnamed: 22'])
    telefones = df['Unnamed: 22'].iloc[1::]

    for i, j in telefones.items():
        telefones[i] = '+55' + (j.replace('(', '')
                                 .replace(')', '')
                                 .replace(' ', '')
                                 .replace('-', ''))

    return list(telefones)

def mostra_telefones(telefones:list) -> None:
    df_telefones = pd.DataFrame(telefones)
    df_telefones.columns = ['Telefones']
    st.dataframe(df_telefones, hide_index=True)

config_inicias()

telefones = []
file_upload = st.file_uploader(label='Selecione o arquivo com os contatos', type=['xlsx','csv'])

if file_upload:
    if file_upload.type.__contains__('.sheet'):
        df = pd.read_excel(file_upload)
        telefones = trata_dados(df)
    else:
        df = pd.read_csv(file_upload)
        telefones = df['telefones']
        for i, j in telefones.items():
            telefones[i] = '+' + str(j)
        telefones = list(telefones)
    mostra_telefones(telefones)

if telefones:
    mensagem = st.text_area('Coloque a sua mensagem para enviar')
    button_pressed = st.button(label='Confirmar Envio')
    if button_pressed:
        for numero in telefones:
            kit.sendwhatmsg_instantly(
                phone_no=numero,
                message=mensagem,
                wait_time=15,
                tab_close=True
            )
            time.sleep(15 + random.randint(5, 15))
        st.text('Processamento Finalizado!')