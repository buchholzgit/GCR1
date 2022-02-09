import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib as plt

pd.set_option('display.max_columns', None)
pd.set_option("expand_frame_repr", True)


st.set_page_config(page_title = "Marktanalyse",
                   page_icon=":bar_chart:",
                   layout="wide")

st.title("Meine Marktanalyse")
st.write("Hier werden zukünftig automatisch generierte Marktanalysen für die Sozialwirtschaft abrufbar sein.")

DATA_URL = "https://storage.googleapis.com/bevdbbucket/Bevolkerungsdaten.csv"

@st.cache(persist=True)
def load_data(filepath):
    data = pd.read_csv(filepath, sep=";")
    return data

df = load_data(filepath=DATA_URL)

GemeindeDropDown = st.sidebar.selectbox("Bitte wählen Sie eine Gemeinde aus.", df.Gemeinde.unique())
JahrSelect = st.selectbox("Bitte wählen Sie das Jahr aus.", df.Jahr.unique())
GeschlechtsDropDown = st.selectbox("Bitte wählen Sie das Geschlecht aus.", df.Geschlecht.unique())
AltersDropDown = st.slider(label="Bitte wählen Sie die Altersgruppe aus.", min_value=0, max_value=90, value=(60, 80))

st.write("Altersauswahl: {}".format(AltersDropDown))

@st.cache(ttl=24*60*60, suppress_st_warning=True)
def AgeBarChart():
    data = df[(df["Gemeinde"] == GemeindeDropDown) & (df.Jahr == JahrSelect) & (df.Altersjahr <= AltersDropDown[1]) & (df.Altersjahr >= AltersDropDown[0])
              & (df.Geschlecht == GeschlechtsDropDown)]
    fig = px.bar(data, x="Altersjahr", y="Daten")
    fig.update_layout(
        autosize=False,
        width=1500,
        height=900)
    st.write(fig)

@st.cache(ttl=24*60*60, suppress_st_warning=True)
def ShowDataFrame():
    data = df[(df.Gemeinde == GemeindeDropDown) & (df.Jahr == JahrSelect) & (df.Altersjahr <= AltersDropDown[1]) & (df.Altersjahr >= AltersDropDown[0])
              & (df.Geschlecht == GeschlechtsDropDown)]
    st.dataframe(data)




#ShowDataFrame()
AgeBarChart()

#print(SubDF)
#st.bar_chart(SubDF)["Daten"]







