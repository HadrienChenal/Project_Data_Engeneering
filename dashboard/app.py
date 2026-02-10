import streamlit as st
import pandas as pd
from db import get_games

st.set_page_config(
    page_title="Steam Dashboard",
    layout="wide"
)

st.title("🎮 Steam – Top Sellers")

data = get_games()

if not data:
    st.error("Aucune donnée trouvée dans MongoDB")
    st.stop()

df = pd.DataFrame(data)

# ---- Sidebar ----
st.sidebar.header("Filtres")
selected_tags = st.sidebar.multiselect(
    "Tags",
    sorted({tag for tags in df["tags"].dropna() for tag in tags})
)

if selected_tags:
    df = df[df["tags"].apply(lambda x: any(t in x for t in selected_tags) if x else False)]

# ---- Tableau ----
st.subheader("📋 Jeux")
st.dataframe(df, use_container_width=True)

# ---- Graphique ----
st.subheader("📊 Top Tags")
tags = df.explode("tags")["tags"].value_counts().head(10)
st.bar_chart(tags)
