import streamlit as st
import pandas as pd
from difflib import SequenceMatcher

st.set_page_config(
    page_title="Santa Hora",
    page_icon="⛪",
    layout="wide",
)

#########

def teste_similaridade(palavra1:str, palavra2:str):
    return SequenceMatcher(None, palavra1, palavra2).ratio()

#########



def resultados_pesquisa_10(pesquisa):
    lista_similaridades = []
    for paroquia_para_testar in df_info_paroquias['Paróquia'].dropna():
        lista_similaridades.append(teste_similaridade(pesquisa.lower(), paroquia_para_testar.lower()))

    # lista_similaridades

    df_similaridades = pd.DataFrame({
        'Similaridade': lista_similaridades
    })

    result = pd.concat([df_info_paroquias, df_similaridades], axis=1)
    return result.sort_values(by=['Similaridade'], ascending=False).head(10)


@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

@st.cache_data
def load_data_latin(url):
    df = pd.read_csv(url, encoding='latin-1')
    return df



df = load_data('https://raw.githubusercontent.com/santahora/santahora/main/horarios_missas_id_2.csv')

df_info_paroquias = load_data_latin('https://raw.githubusercontent.com/santahora/santahora/main/info_paroquias.csv')


###SIDEBAR###
with st.sidebar:
    st.title("⛪ SANTA HORA")
    opcao = st.selectbox(
        'Selecione uma opção',
        ('Pesquisar', 'Dia'),
        index = 1,
    )

    if opcao == 'Pesquisar':
        paroquia_pesquisada = st.text_input(
        label = 'Pesquisar paróquia',
        # value = 'Paróquia',
        placeholder = 'Paróquia',
        label_visibility = 'collapsed',
        )
        dia_selecionado = 'Domingo'
    elif opcao == 'Dia':

        dia_selecionado = st.radio(
        "Selecione o Dia:",
        ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"],
        index=6,
        horizontal = True,
    )

    # decanato_selecionado = st.radio(
    #     "Selecione o Decanato:",
    #     ["Todos", "Centro", "Leste"],
    #     #, "Oeste", "Norte", "Sul", "Tamarana", "Cambé", "Rolândia", "Sertanópolis", "Ibiporã", "Porecatu"
    #     index=0,
    # )
    decanato_selecionado = 'Todos'

#############


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


###MAIN PAGE###


def mostrar_endereco(paroquia):
    for endereco, cidade in zip(df_info_paroquias[df_info_paroquias["Paróquia"] == paroquia]['Endereço'],
                                df_info_paroquias[df_info_paroquias["Paróquia"] == paroquia]['Cidade']):
        st.write('📍 ' + endereco + ' - ' + cidade)

def mostrar_telefone(paroquia):
    for i in df_info_paroquias[df_info_paroquias["Paróquia"] == paroquia]['Telefone']:
        st.write('📞 ' + i)

def mostrar_links(paroquia):
    ###LINKS
    colEmail, colSite, colFB, colInsta = st.columns([1, 1, 1, 15])
    # email icon
    with colEmail:
        for i in df_info_paroquias[df_info_paroquias["Paróquia"] == paroquia]['Email']:
            html = f"<a style='text-decoration:none' href = '{i}' rel = 'noopener noreferrer' target = '_blank' ><font style='font-size: 1.25em;'>📧</font></a>"
            st.markdown(html, unsafe_allow_html=True)
    # site icon
    with colSite:
        try:
            for i in df_info_paroquias[df_info_paroquias["Paróquia"] == paroquia]['Site']:
                if len(i) > 1:
                    html = f"<a style='text-decoration:none' href = '{i}' rel = 'noopener noreferrer' target = '_blank' ><font style='font-size: 1.25em;'>🌐</font></a>"
                    st.markdown(html, unsafe_allow_html=True)
                else:
                    st.empty()
        except:
            pass

    # fb icon
    with colFB:
        try:
            for i in df_info_paroquias[df_info_paroquias["Paróquia"] == paroquia]['Facebook']:
                html = f"<a style='text-decoration:none' href='{i}'><img src='https://github.com/santahora/santahora/blob/main/fbicon18x18.jpg?raw=true'></a>"
                st.markdown(html, unsafe_allow_html=True)
        except:
            pass
    # insta icon
    with colInsta:
        try:
            for i in df_info_paroquias[df_info_paroquias["Paróquia"] == paroquia]['Instagram']:
                html = f"<a style='text-decoration:none' href='{i}'><img src='https://github.com/santahora/santahora/blob/main/instaicon18x18.png?raw=true'></a>"
                st.markdown(html, unsafe_allow_html=True)
        except:
            pass

def mostrar_todas_missas_paroquia(paroquia):
    lista_dias_com_missa_na_paroquia = df[df['Paróquia'] == paroquia]['Dia'].unique()

    df_par = df[df['Paróquia'] == paroquia]

    horarios_do_dia_df = pd.DataFrame()
    for dia in lista_dias_com_missa_na_paroquia:
        horarios_do_dia_dic = {}
        lista_horarios = []

        for horario in df_par[df_par['Dia'] == dia]['Horário']:
            lista_horarios.append(horario)

        horarios_do_dia_dic[dia] = lista_horarios
        horarios_do_dia_dic_df = pd.DataFrame(horarios_do_dia_dic)
        horarios_do_dia_df = pd.concat([horarios_do_dia_df, horarios_do_dia_dic_df], axis=1)

    horarios_do_dia_df.fillna(value='', inplace=True)
    st.write('Outras missas')
    st.dataframe(horarios_do_dia_df, hide_index=True)

def mostrar_horarios(dia_selecionado, df_cut):
    st.header(dia_selecionado, anchor=None, help=None, divider='red')

    lista_tabs = []

    lista_tabs = st.tabs(list(df_cut['Horário'].unique()))

    for tab, horario in zip(lista_tabs, df_cut['Horário'].unique()):
        with tab:
            for paroquia in df_cut[df_cut['Horário'] == horario]['Paróquia'].sort_values():
                with st.expander(paroquia, expanded=False):
                    mostrar_endereco(paroquia)
                    mostrar_telefone(paroquia)
                    mostrar_links(paroquia)
                    mostrar_todas_missas_paroquia(paroquia)

def mostrar_pesquisa(paroquia_pesquisada):
    st.header('Resultado para: ' + paroquia_pesquisada, anchor=None, help=None, divider='red')
    lista_pesquisa = resultados_pesquisa_10(paroquia_pesquisada)
    for paroquia in lista_pesquisa['Paróquia']:
        with st.expander(paroquia, expanded=False):
            mostrar_endereco(paroquia)
            mostrar_telefone(paroquia)
            mostrar_links(paroquia)
            mostrar_todas_missas_paroquia(paroquia)


if opcao == 'Pesquisar':
    # if paroquia_pesquisada != '':
    mostrar_pesquisa(paroquia_pesquisada)

elif opcao == 'Dia':
    # else:
    mostrar_horarios(dia_selecionado, df_cut)





#############


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
