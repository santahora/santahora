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
df_cut = df[df["Dia"] == dia_selecionado].drop(['ID missa', 'Arquidiocese', 'Decanato', 'Cidade', 'Observação'], axis=1).sort_values(by='Horário')
# st.write(df_cut)

# st.write(df_cut['Horário'].unique())

# for horario in df_cut['Horário'].unique():
#     st.write(horario)
#     for paroquia in df_cut[df_cut['Horário'] == horario]['Paróquia']:
#         st.write(paroquia)

lista_tabs = []

lista_tabs = st.tabs(list(df_cut['Horário'].unique()))

# for tab in lista_horarios:
#     with tab:
#         st.write(type(str(tab)))
#         for horario in df_cut['Horário'].unique():
#             st.write(horario)
#             for paroquia in df_cut[df_cut['Horário'] == horario]['Paróquia']:
#                 st.write(paroquia)

for tab, horario in zip(lista_tabs, df_cut['Horário'].unique()):
    with tab:
        st.write(horario)
        for paroquia in df_cut[df_cut['Horário'] == horario]['Paróquia'].sort_values():
            st.write(paroquia)