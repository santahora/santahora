import streamlit as st
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/santahora/santahora/main/horarios_missas_id_2.csv")

with st.sidebar:
    st.title("SANTA HORA")
    # st.write("Dia")

    dia_selecionado = st.radio(
        "Selecione o Dia:",
        ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"],
        index=6,
    )

    st.write("You selected:", dia_selecionado)

    # dom = st.toggle('Domingo')

    # if dom:
    #     st.write(df["Segunda"][0])

# if dom:
st.write(df[df["Dia"] == dia_selecionado].drop(['ID missa', 'Arquidiocese', 'Decanato', 'Cidade', 'Observação'], axis=1).sort_values(by='Horário'))