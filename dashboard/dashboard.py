import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import scipy.stats as stats

sns.set(style="whitegrid")

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

st.markdown("""
<style>

/* CARD */
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f8f9fc;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    text-align: center;
}

/* INSIGHT BOX */
.insight-box {
    background: linear-gradient(135deg, #e3f2fd, #f8fbff);
    padding: 18px;
    border-left: 6px solid #1e88e5;
    border-radius: 10px;
    margin-top: 8px;
    margin-bottom: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    font-size: 18px;
    line-height: 1.6;
}

.insight-box b:first-child {
    font-size: 18px;
    color: #0d47a1;
}

/* SECTION */
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-top: 10px;
}

/* BOX KESIMPULAN */
.box-kesimpulan {
    background-color: #eef4ff;
    padding: 18px;
    border-radius: 12px;
}

/* BOX REKOMENDASI */
.box-rekomendasi {
    background-color: #e8f5e9;
    padding: 18px;
    border-radius: 12px;
}

/* RAPIIIN GLOBAL */
.block-container {
    padding-top: 2rem;
    padding-bottom: 1rem;
}

</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])
    df["year"] = df["dteday"].dt.year
    df["month"] = df["dteday"].dt.month

    df["temp_category"] = pd.cut(
        df["temp"],
        bins=[0, 0.33, 0.66, 1.0],
        labels=["Dingin", "Sedang", "Panas"]
    )

    return df

df = load_data()

# ================= FILTER =================
st.sidebar.markdown("## 📊 Filter Data")

selected_year = st.sidebar.multiselect(
    "Tahun",
    sorted(df["year"].unique()),
    default=sorted(df["year"].unique())
)

selected_season = st.sidebar.multiselect(
    "Musim",
    ["Spring", "Summer", "Fall", "Winter"],
    default=["Spring", "Summer", "Fall", "Winter"]
)

date_range = st.sidebar.date_input(
    "Rentang waktu",
    [df["dteday"].min(), df["dteday"].max()]
)

df_filtered = df[
    (df["year"].isin(selected_year)) &
    (df["season"].isin(selected_season))
]

if len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    df_filtered = df_filtered[
        (df_filtered["dteday"] >= start) &
        (df_filtered["dteday"] <= end)
    ]

st.sidebar.info("""
Dashboard ini menganalisis penyewaan sepeda

Fokus:
- Tren waktu  
- Suhu 
- Kelembaban & angin  
- Musim  
- Hari kerja vs libur  

Insight utama: suhu paling berpengaruh terhadap permintaan.
""")

# ================= HEADER =================
st.title("🚲 Dashboard Bike Sharing")
st.markdown("Analisis faktor yang memengaruhi penyewaan sepeda (2011–2012).")

st.success("Insight utama: suhu merupakan faktor paling dominan dalam meningkatkan penyewaan sepeda.")

# ================= METRICS =================
col1, col2, col3, col4 = st.columns(4)

col1.markdown(f'<div class="card"><h5>Rata-rata</h5><h2>{int(df_filtered["cnt"].mean()):,}</h2></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="card"><h5>Median</h5><h2>{int(df_filtered["cnt"].median()):,}</h2></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="card"><h5>Maksimum</h5><h2>{df_filtered["cnt"].max():,}</h2></div>', unsafe_allow_html=True)
col4.markdown(f'<div class="card"><h5>Jumlah Data</h5><h2>{len(df_filtered)}</h2></div>', unsafe_allow_html=True)

st.markdown("""
Secara umum, penyewaan sepeda berada pada level stabil dengan rata-rata sekitar **4.500 unit/hari**.  
Namun, terdapat lonjakan pada kondisi tertentu yang menunjukkan bahwa permintaan dipengaruhi oleh **cuaca dan musim**.
""")

st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)

# =====================================================
# 1. SUHU
# =====================================================
st.subheader("1. Hubungan Suhu dengan Jumlah Penyewaan Sepeda")

fig, ax = plt.subplots(figsize=(6,4))
sns.regplot(x="temp", y="cnt", data=df_filtered, ax=ax)
plt.tight_layout()
st.pyplot(fig)

st.markdown("""
<div class="insight-box">
<b>Insight:</b><br><br>

<b>Suhu (temperature)</b> memiliki pengaruh paling dominan terhadap jumlah penyewaan sepeda.  
Semakin tinggi suhu, jumlah penyewaan meningkat secara konsisten, menunjukkan hubungan positif yang kuat.<br><br> 
Meskipun terdapat variasi pada beberapa titik data, pola umum tetap stabil dan jelas, 
sehingga suhu dapat dianggap sebagai faktor utama yang mendorong aktivitas bersepeda.<br><br>
Hal ini menunjukkan bahwa <b>suhu dapat digunakan sebagai indikator utama dalam memprediksi permintaan</b>, 
serta sebagai dasar dalam pengambilan keputusan operasional seperti penambahan unit sepeda saat cuaca hangat.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)

# =====================================================
# 2. KELEMBABAN
# =====================================================
st.subheader("2. Pengaruh Kelembaban terhadap Penyewaan Sepeda")

fig, ax = plt.subplots(figsize=(6,4))
sns.regplot(x="hum", y="cnt", data=df_filtered, ax=ax)
plt.tight_layout()
st.pyplot(fig)

st.markdown("""
<div class="insight-box">
<b>Insight:</b><br><br>

<b>Kelembaban (humidity)</b> menunjukkan hubungan negatif terhadap jumlah penyewaan, 
namun dengan kekuatan yang relatif lemah.<br><br>
Peningkatan kelembaban cenderung diikuti dengan penurunan jumlah penyewaan, 
tetapi pola ini tidak konsisten di seluruh data.<br><br>
Hal ini mengindikasikan bahwa <b>kelembaban bukan faktor utama dalam menentukan permintaan</b>, 
melainkan hanya sebagai faktor pendukung yang memiliki pengaruh terbatas dibandingkan suhu.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)

# =====================================================
# 3. TREND WAKTU
# =====================================================
st.subheader("3. Tren Penyewaan Sepeda Berdasarkan Waktu")

monthly = df_filtered.set_index("dteday").resample("ME")["cnt"].sum()

fig, ax = plt.subplots(figsize=(6,4))
monthly.plot(ax=ax)
plt.tight_layout()
st.pyplot(fig)

st.markdown("""
<div class="insight-box">
<b>Insight:</b><br><br>

Penyewaan sepeda menunjukkan <b>pola musiman (seasonality) yang jelas</b>, 
dengan peningkatan bertahap dari awal tahun hingga mencapai puncak di pertengahan tahun, 
kemudian menurun kembali di akhir tahun.<br><br>
Selain itu, terdapat <b>tren peningkatan jumlah penyewaan dari tahun 2011 ke 2012</b>, 
yang menunjukkan adanya pertumbuhan penggunaan layanan sepeda dari waktu ke waktu.<br><br>
Pola ini mengindikasikan bahwa <b>permintaan dipengaruhi oleh faktor waktu dan musim</b>, 
sehingga penting untuk menyesuaikan strategi operasional berdasarkan periode tertentu.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)

# =====================================================
# 4. WORKINGDAY
# =====================================================
st.subheader("4. Perbandingan Penyewaan Berdasarkan Hari Kerja dan Hari Libur")

fig, ax = plt.subplots(figsize=(6,4))
sns.barplot(x="workingday", y="cnt", data=df_filtered, ax=ax)
plt.tight_layout()
st.pyplot(fig)

st.markdown("""
<div class="insight-box">
<b>Insight:</b><br><br>

Perbedaan jumlah penyewaan antara <b>hari kerja</b> dan <b>hari libur</b> tidak signifikan.  
Rata-rata penyewaan pada kedua kategori berada pada level yang hampir sama.<br><br>
Hal ini menunjukkan bahwa sepeda digunakan baik untuk keperluan rutin seperti bekerja 
maupun untuk aktivitas rekreasi.<br><br>
Dengan demikian, <b>permintaan cenderung stabil sepanjang minggu</b>, 
dan tidak terlalu dipengaruhi oleh jenis hari.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)

# =====================================================
# 5. SEASON
# =====================================================
st.subheader("5. Perbandingan Penyewaan Berdasarkan Musim")

fig, ax = plt.subplots(figsize=(6,4))
sns.barplot(x="season", y="cnt", data=df_filtered, ax=ax)
plt.tight_layout()
st.pyplot(fig)

st.markdown("""
<div class="insight-box">
<b>Insight:</b><br><br>

Musim memiliki pengaruh yang cukup signifikan terhadap jumlah penyewaan sepeda.  
<b>Fall</b> menunjukkan tingkat penyewaan tertinggi, diikuti oleh Summer dan Winter, 
sedangkan <b>Spring</b> memiliki nilai terendah.<br><br>
Hal ini menunjukkan bahwa <b>kondisi lingkungan dan kenyamanan pada musim tertentu</b> 
berperan penting dalam meningkatkan atau menurunkan minat masyarakat untuk bersepeda.<br><br>
Dengan demikian, <b>pola musiman dapat dimanfaatkan untuk mengoptimalkan strategi operasional</b> 
dan perencanaan ketersediaan sepeda.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)

# =====================================================
# ANALISIS LANJUTAN (TETAP)
# =====================================================
st.subheader("6. Analisis Lanjutan")

tab1, tab2, tab3 = st.tabs(["Tren Tahunan", "Kategori Suhu", "Uji Statistik"])

with tab1:
    monthly_year = df_filtered.groupby(["year", "month"])["cnt"].sum().reset_index()

    fig, ax = plt.subplots()
    for year, group in monthly_year.groupby("year"):
        ax.plot(group["month"], group["cnt"], marker="o", label=str(year))
    ax.legend()
    st.pyplot(fig)

    st.info("Tahun 2012 menunjukkan peningkatan penyewaan dibandingkan 2011.")

with tab2:
    fig, ax = plt.subplots()
    sns.barplot(x="temp_category", y="cnt", data=df_filtered, ax=ax)
    st.pyplot(fig)

    st.info("Kategori suhu memperjelas hubungan suhu dengan penyewaan.")

with tab3:
    working = df_filtered[df_filtered["workingday"] == "Working Day"]["cnt"]
    holiday = df_filtered[df_filtered["workingday"] == "Holiday"]["cnt"]

    t_stat, p_value = stats.ttest_ind(working, holiday, equal_var=False)

    st.metric("P-value", f"{p_value:.4f}")

    if p_value < 0.05:
        st.success("Signifikan")
    else:
        st.info("Tidak signifikan")

st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)

# =====================================================
# KESIMPULAN
# =====================================================
st.subheader("7. Kesimpulan")

st.markdown("""
Analisis menunjukkan bahwa suhu merupakan faktor utama yang memengaruhi jumlah penyewaan sepeda, 
dengan hubungan positif yang kuat. Kelembaban memiliki pengaruh negatif namun relatif lemah. 
Selain itu, terdapat pola musiman yang konsisten serta tren peningkatan dari tahun ke tahun. 
Perbedaan antara hari kerja dan hari libur tidak signifikan, sedangkan musim memiliki pengaruh yang cukup jelas terhadap variasi penyewaan.
""")

# =====================================================
# REKOMENDASI
# =====================================================
st.subheader("8. Rekomendasi")

st.markdown("""
1. Tingkatkan ketersediaan sepeda saat suhu tinggi  
2. Fokus pada musim dengan permintaan tinggi  
3. Lakukan promosi pada musim rendah  
4. Gunakan suhu sebagai indikator prediksi  
5. Pertahankan operasional stabil sepanjang minggu  
6. Kembangkan layanan seiring peningkatan tren  
""")