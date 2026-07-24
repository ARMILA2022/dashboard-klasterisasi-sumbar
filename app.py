
import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Klasterisasi Sumatera Barat",
    page_icon="🗺️",
    layout="wide"
)

st.title(
    "Dashboard Klasterisasi Sosial Ekonomi"
)

st.subheader(
    "Kabupaten/Kota di Provinsi Sumatera Barat"
)

st.write(
    "Dashboard ini menyajikan hasil klasterisasi "
    "kabupaten/kota di Provinsi Sumatera Barat "
    "berdasarkan indikator sosial ekonomi periode 2021–2025 "
    "menggunakan algoritma K-Means."
)

# Membaca data
df_cluster = pd.read_csv(
    "hasil_cluster.csv"
)

gdf = gpd.read_file(
    "hasil_cluster_peta.geojson"
)

# Informasi data
jumlah_wilayah = len(df_cluster)

jumlah_cluster = df_cluster[
    "Cluster"
].nunique()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Jumlah Kabupaten/Kota",
        jumlah_wilayah
    )

with col2:
    st.metric(
        "Jumlah Cluster",
        jumlah_cluster
    )

with col3:
    st.metric(
        "Periode Data",
        "2021–2025"
    )

st.divider()

# Peta
st.header(
    "🗺️ Peta Klasterisasi Sumatera Barat"
)

gdf["Cluster"] = gdf[
    "Cluster"
].astype(str)

fig_map = px.choropleth_mapbox(

    gdf,

    geojson=gdf.__geo_interface__,

    locations=gdf.index,

    color="Cluster",

    hover_name="kab_kota",

    mapbox_style="open-street-map",

    center={
        "lat": -0.95,
        "lon": 100.35
    },

    zoom=6.5,

    opacity=0.6
)

fig_map.update_layout(
    height=650,
    margin={
        "r": 0,
        "t": 0,
        "l": 0,
        "b": 0
    }
)

st.plotly_chart(
    fig_map,
    use_container_width=True
)

# Jumlah anggota cluster
st.header(
    "📊 Jumlah Kabupaten/Kota Setiap Cluster"
)

jumlah_cluster_df = (

    df_cluster[
        "Cluster"
    ]

    .value_counts()

    .sort_index()

    .reset_index()

)

jumlah_cluster_df.columns = [
    "Cluster",
    "Jumlah Kabupaten/Kota"
]

fig_bar = px.bar(

    jumlah_cluster_df,

    x="Cluster",

    y="Jumlah Kabupaten/Kota",

    text="Jumlah Kabupaten/Kota",

    title="Distribusi Kabupaten/Kota Berdasarkan Cluster"

)

st.plotly_chart(
    fig_bar,
    use_container_width=True
)

# Filter cluster
st.header(
    "🔎 Daftar Kabupaten/Kota Berdasarkan Cluster"
)

pilihan_cluster = st.selectbox(

    "Pilih Cluster",

    sorted(
        df_cluster[
            "Cluster"
        ].unique()
    )

)

df_filter = df_cluster[

    df_cluster[
        "Cluster"
    ].astype(str)

    == pilihan_cluster

]

st.dataframe(
    df_filter,
    use_container_width=True
)

# Download data
st.header(
    "📥 Unduh Data Hasil Klasterisasi"
)

csv_download = df_cluster.to_csv(
    index=False
)

st.download_button(

    label="Download Hasil Cluster",

    data=csv_download,

    file_name="hasil_cluster.csv",

    mime="text/csv"

)
