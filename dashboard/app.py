import streamlit as st
import pandas as pd
from db import get_games


# -------------------------
# CONFIG
# -------------------------
st.set_page_config(
    page_title="Steam Top Sellers Dashboard",
    layout="wide"
)

st.title("🎮 Steam Top Sellers Dashboard")


# -------------------------
# LOAD DATA
# -------------------------
data = get_games()

if not data:
    st.error("Aucune donnée trouvée dans MongoDB")
    st.stop()

df = pd.DataFrame(data)


# -------------------------
# DATA CLEANING
# -------------------------
df["discount_percent"] = pd.to_numeric(df["discount_percent"], errors="coerce").fillna(0)
df["review_score"] = pd.to_numeric(df["review_score"], errors="coerce")
df["review_count"] = pd.to_numeric(df["review_count"], errors="coerce")
df["release_date_parsed"] = pd.to_datetime(
    df["release_date"],
    errors="coerce",
    dayfirst=True
)

df["year"] = df["release_date_parsed"].dt.year


# -------------------------
# SIDEBAR FILTERS
# -------------------------
st.sidebar.header("🎯 Filtres")

# Tags
all_tags = sorted({tag for tags in df["tags"].dropna() for tag in tags})
selected_tags = st.sidebar.multiselect("Tags", all_tags)

# Discount
min_discount = st.sidebar.slider("Réduction minimale (%)", 0, 100, 0)

# Review score
min_score = st.sidebar.slider("Score minimum", 0, 100, 0)

# Top N
top_n = st.sidebar.slider("Afficher Top N jeux", 10, 100, 50)


# Apply filters
if selected_tags:
    df = df[df["tags"].apply(lambda x: any(t in x for t in selected_tags) if x else False)]

df = df[df["discount_percent"] >= min_discount]
df = df[df["review_score"].fillna(0) >= min_score]
df = df.sort_values("rank").head(top_n)


# -------------------------
# KPIs
# -------------------------
st.subheader("📊 Indicateurs clés")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🎮 Nombre de jeux", len(df))

col2.metric(
    "🔥 Réduction moyenne",
    f"{df['discount_percent'].mean():.1f}%"
)

col3.metric(
    "⭐ Score moyen",
    f"{df['review_score'].mean():.1f}"
)

col4.metric(
    "🗣 Reviews totales",
    int(df["review_count"].sum())
)


# -------------------------
# TABLE
# -------------------------
st.subheader("📋 Liste des jeux")

display_columns = [
    "rank",
    "name",
    "price",
    "discount_percent",
    "review_score",
    "review_count",
    "release_date"
]

st.dataframe(
    df[display_columns],
    use_container_width=True
)


# -------------------------
# TOP 10 SCORES
# -------------------------
st.subheader("🏆 Top 10 jeux par score")

top_rated = df.sort_values("review_score", ascending=False).head(10)

st.bar_chart(
    top_rated.set_index("name")["review_score"]
)


# -------------------------
# DISCOUNT vs POPULARITY
# -------------------------
st.subheader("💰 Réduction vs Popularité")

scatter_df = df.dropna(subset=["discount_percent", "review_count"])

st.scatter_chart(
    scatter_df,
    x="discount_percent",
    y="review_count"
)


# -------------------------
# TOP TAGS
# -------------------------
st.subheader("🏷 Top 10 Tags")

tags_series = df.explode("tags")["tags"].value_counts().head(10)

st.bar_chart(tags_series)