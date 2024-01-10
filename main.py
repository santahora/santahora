import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Santa Hora",
    page_icon="⛪",
    layout="wide",
)

df = pd.read_csv('https://raw.githubusercontent.com/santahora/santahora/main/horarios_missas_id_2.csv')

df_info_paroquias = pd.read_csv('https://raw.githubusercontent.com/santahora/santahora/main/info_paroquias.csv', encoding='latin-1')

with st.sidebar:
    st.title("⛪ SANTA HORA")

    dia_selecionado = st.radio(
        "Selecione o Dia:",
        ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"],
        index=6,
    )

    decanato_selecionado = st.radio(
        "Selecione o Decanato:",
        ["Todos", "Centro", "Leste"],
        #, "Oeste", "Norte", "Sul", "Tamarana", "Cambé", "Rolândia", "Sertanópolis", "Ibiporã", "Porecatu"
        index=0,
    )

#FILTRANDO O DATABASE
df_cut = df
df_cut = df_cut[df_cut["Dia"] == dia_selecionado]

if decanato_selecionado != None and decanato_selecionado != "Todos":
    df_cut = df_cut[df_cut["Decanato"] == decanato_selecionado]
else:
    df_cut.drop(['Decanato'], axis=1)

df_cut = df_cut.drop(['ID missa', 'Arquidiocese', 'Cidade', 'Observação'], axis=1)
df_cut = df_cut.sort_values(by='Horário')

#FIM FILTRO DATABASE


st.header(dia_selecionado, anchor=None, help=None, divider='red')

lista_tabs = []

lista_tabs = st.tabs(list(df_cut['Horário'].unique()))

for tab, horario in zip(lista_tabs, df_cut['Horário'].unique()):
    with tab:
        for paroquia in df_cut[df_cut['Horário'] == horario]['Paróquia'].sort_values():
            with st.expander(paroquia, expanded=False):
                for i in df_info_paroquias[df_info_paroquias["Paróquia"] == paroquia]['Endereço']:
                    st.write('📍 ' + i)
                for i in df_info_paroquias[df_info_paroquias["Paróquia"] == paroquia]['Telefone']:
                    st.write('📞 ' + i)

###LINKS
                colEmail, colSite, colFB, colInsta = st.columns([1,1,1,15])
#email icon
                with colEmail:
                    for i in df_info_paroquias[df_info_paroquias["Paróquia"] == paroquia]['Email']:
                        html = f"<a href = '{i}' rel = 'noopener noreferrer' target = '_blank' >📧</a>"
                        st.markdown(html, unsafe_allow_html=True)
#site icon
                with colSite:
                    try:
                        for i in df_info_paroquias[df_info_paroquias["Paróquia"] == paroquia]['Site']:
                            if len(i) > 1:
                                html = f"<a href = '{i}' rel = 'noopener noreferrer' target = '_blank' >🌐</a>"
                                st.markdown(html, unsafe_allow_html=True)
                            else:
                                st.empty()
                    except:
                        pass

#fb icon
                with colFB:
                    try:
                        for i in df_info_paroquias[df_info_paroquias["Paróquia"] == paroquia]['Facebook']:
                            html = f"<a href='{i}'><img src='https://github.com/santahora/santahora/blob/main/fbicon18x18.jpg?raw=true'></a>"
                            st.markdown(html, unsafe_allow_html=True)
                    except:
                        pass
#insta icon
                with colInsta:
                    try:
                        for i in df_info_paroquias[df_info_paroquias["Paróquia"] == paroquia]['Instagram']:
                            html = f"<a href='{i}'><img src='https://github.com/santahora/santahora/blob/main/instaicon18x18.png?raw=true'></a>"
                            st.markdown(html, unsafe_allow_html=True)
                    except:
                        pass

                lista_dias_com_missa_na_paroquia = df[df['Paróquia'] == paroquia]['Dia'].unique()

                df_par = df[df['Paróquia'] == paroquia]

                horarios_do_dia_df = pd.DataFrame()
                for dia in lista_dias_com_missa_na_paroquia:
                    horarios_do_dia_dic = {}
                    lista_horarios = []
                    for horario in df_par[df_par['Dia'] == dia]['Horário']:
                        lista_horarios.append(horario)
                    print(dia)
                    horarios_do_dia_dic[dia] = lista_horarios
                    horarios_do_dia_dic_df = pd.DataFrame(horarios_do_dia_dic)
                    horarios_do_dia_df = pd.concat([horarios_do_dia_df, horarios_do_dia_dic_df], axis=1)
                horarios_do_dia_df.fillna(value='', inplace=True)
                st.write('Outras missas')
                st.dataframe(horarios_do_dia_df, hide_index=True)

css = '''
<style>
    /* Aumentar fonte dos horarios na tab */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.5rem;
    }
    
    
    /* Esconder botao de download da tabela de horarios */
    [data-testid="stElementToolbar"] {
    display: none;
    }
    
</style>
'''

st.markdown(css, unsafe_allow_html=True)