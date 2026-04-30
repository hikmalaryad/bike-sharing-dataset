import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import scipy.stats as stats

sns.set(style="whitegrid")

st.set_page_config(
   page_title="Dashboard Analisis Penyewaan Sepeda (2011–2012)",
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

    # tanggal aman
    df["dteday"] = pd.to_datetime(df["dteday"], errors="coerce")

    # drop tanggal rusak
    df = df.dropna(subset=["dteday"])

    # fitur waktu
    df["year"] = df["dteday"].dt.year
    df["month"] = df["dteday"].dt.month

    # ================= FIX SEASON =================
    if df["season"].dtype != "object":
        df["season"] = df["season"].map({
            1: "Spring",
            2: "Summer",
            3: "Fall",
            4: "Winter"
        })

    # ================= FIX WORKINGDAY =================
    if df["workingday"].dtype != "object":
        df["workingday_label"] = df["workingday"].map({
            0: "Holiday",
            1: "Working Day"
        })
    else:
        df["workingday_label"] = df["workingday"]

    # ================= DROP NULL =================
    df = df.dropna(subset=["season", "workingday_label"])

    # ================= TEMP CATEGORY =================
    df["temp_category"] = pd.cut(
        df["temp"],
        bins=[0, 0.33, 0.66, 1.0],
        labels=["Dingin", "Sedang", "Panas"]
    )

    return df

df = load_data()

# ================= FIX FILTER WAJIB =================

# buang data yang gagal mapping
df = df.dropna(subset=["season", "workingday_label"])

# ================= CLEAN DATA =================

# convert tanggal aman
df["dteday"] = pd.to_datetime(df["dteday"], errors="coerce")

# buang tanggal rusak
df = df.dropna(subset=["dteday"])

# ================= FILTER =================
st.sidebar.markdown("## 📊 Filter Data")

# Tahun (WAJIB ADA)
selected_year = st.sidebar.multiselect(
    "Pilih Tahun",
    options=sorted(df["year"].dropna().unique()),
    default=sorted(df["year"].dropna().unique())
)

# Musim
selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    options=[x for x in sorted(df["season"].unique()) if pd.notna(x)],
    default=[x for x in sorted(df["season"].unique()) if pd.notna(x)]
)

# Hari
selected_workingday = st.sidebar.multiselect(
    "Pilih Tipe Hari",
    options=[x for x in sorted(df["workingday_label"].unique()) if pd.notna(x)],
    default=[x for x in sorted(df["workingday_label"].unique()) if pd.notna(x)]
)

# ================= DATE =================
if df.empty:
    st.error("Data kosong setelah cleaning")
    st.stop()

min_date = df["dteday"].min()
max_date = df["dteday"].max()

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=(min_date.date(), max_date.date())
)

# ================= APPLY FILTER =================
df_filtered = df[
    (df["year"].isin(selected_year)) &
    (df["season"].isin(selected_season)) &
    (df["workingday_label"].isin(selected_workingday))
]

# Filter tanggal
if len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    df_filtered = df_filtered[
        (df_filtered["dteday"] >= start) &
        (df_filtered["dteday"] <= end)
    ]

# ================= INFO SIDEBAR =================
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

# ================= VALIDASI DATA =================
if df_filtered.empty:
    st.warning("Filter terlalu sempit, menampilkan semua data.")
    df_filtered = df.copy()

# ================= INFO JUMLAH DATA =================
st.caption(f"Jumlah data ditampilkan: {len(df_filtered)} baris")

# ================= HEADER =================
st.title("🚲 Dashboard Bike Sharing")
st.markdown("Analisis faktor yang memengaruhi penyewaan sepeda (2011–2012).")

st.success("Insight utama: suhu merupakan faktor paling dominan dalam meningkatkan penyewaan sepeda.")

# ================= METRICS =================
col1, col2, col3, col4 = st.columns(4)

mean_val = df_filtered["cnt"].mean()
median_val = df_filtered["cnt"].median()
max_val = df_filtered["cnt"].max()
count_val = len(df_filtered)

col1.markdown(
    f'<div class="card"><h5>Rata-rata</h5><h2>{int(mean_val) if pd.notna(mean_val) else 0:,}</h2></div>',
    unsafe_allow_html=True
)

col2.markdown(
    f'<div class="card"><h5>Median</h5><h2>{int(median_val) if pd.notna(median_val) else 0:,}</h2></div>',
    unsafe_allow_html=True
)

col3.markdown(
    f'<div class="card"><h5>Maksimum</h5><h2>{int(max_val) if pd.notna(max_val) else 0:,}</h2></div>',
    unsafe_allow_html=True
)

col4.markdown(
    f'<div class="card"><h5>Jumlah Data</h5><h2>{count_val}</h2></div>',
    unsafe_allow_html=True
)

st.markdown("""
Secara umum, penyewaan sepeda berada pada level stabil dengan rata-rata sekitar **4.500 unit/hari**.  
Namun, terdapat lonjakan pada kondisi tertentu yang menunjukkan bahwa permintaan dipengaruhi oleh **cuaca dan musim**.
""")

st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)

# =====================================================
# 1. SUHU + KELEMBABAN
# =====================================================
st.markdown("## 🎯 Pertanyaan 1: Pengaruh Suhu & Kelembaban")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    sns.regplot(x="temp", y="cnt", data=df_filtered, ax=ax)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    sns.regplot(x="hum", y="cnt", data=df_filtered, ax=ax)
    st.pyplot(fig)

st.markdown("""
<div class="insight-box">
<b>Insight:</b><br><br>

Suhu (temp) menunjukkan korelasi positif moderat terhadap jumlah penyewaan (r≈0.63), 
menjadikannya faktor utama (key driver) peningkatan demand. Sebaliknya, kelembaban (hum) 
memiliki korelasi negatif sangat lemah (r≈-0.10), sehingga pengaruhnya tidak signifikan. 
Artinya, peningkatan suhu secara konsisten mendorong penyewaan, sementara kelembaban 
bukan faktor penentu utama.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)

# =====================================================
# 2. TREND
# =====================================================
st.markdown("## 🎯 Pertanyaan 2: Tren Penyewaan Sepeda")

monthly = df_filtered.set_index("dteday").resample("ME")["cnt"].mean()

if monthly.empty:
    st.info("Data tidak cukup untuk menampilkan tren")
else:
    fig, ax = plt.subplots(figsize=(8,4))
    monthly.plot(ax=ax)
    st.pyplot(fig)

st.markdown("""
<div class="insight-box">
<b>Insight:</b><br><br>

Tren penyewaan menunjukkan pola musiman yang konsisten, dengan peak terjadi pada 
pertengahan tahun (≈Jun–Sep) dan penurunan di awal serta akhir tahun. Selain itu, 
terlihat adanya peningkatan level penyewaan pada tahun 2012 dibanding 2011, 
mengindikasikan growth demand secara keseluruhan.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)

# =====================================================
# 3. WORKINGDAY + SEASON
# =====================================================
st.markdown("## 🎯 Pertanyaan 3: Perbandingan Hari & Musim")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    sns.barplot(x="workingday_label", y="cnt", data=df_filtered, ax=ax)
    ax.set_xlabel("Jenis Hari")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.set_title("Perbandingan Penyewaan: Hari Kerja vs Libur")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    sns.barplot(x="season", y="cnt", data=df_filtered, ax=ax)
    st.pyplot(fig)

st.markdown("""
<div class="insight-box">
<b>Insight:</b><br><br>

Perbedaan penyewaan antara hari kerja dan hari libur relatif kecil, sehingga 
tipe hari bukan faktor utama dalam menentukan demand. Sebaliknya, musim memiliki 
pengaruh yang lebih signifikan, dengan peak terjadi pada Fall dan Summer serta 
terendah pada Spring, menunjukkan adanya efek seasonality yang kuat.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)

# =====================================================
# ANALISIS LANJUTAN
# =====================================================
st.subheader("Analisis Lanjutan")

tab1, tab2, tab3 = st.tabs(["Tren Tahunan", "Kategori Suhu", "Uji Statistik"])

# ======================
# TAB 1: TREND TAHUNAN
# ======================
with tab1:
    monthly_year = df_filtered.groupby(["year", "month"])["cnt"].mean().reset_index()

    fig, ax = plt.subplots()
    for year, group in monthly_year.groupby("year"):
        ax.plot(group["month"], group["cnt"], marker="o", label=str(year))
    ax.legend()
    ax.set_title("Perbandingan Tren Bulanan per Tahun")
    st.pyplot(fig)

    st.markdown("""
<div class="insight-box">
<b>Insight:</b><br><br>

Tahun 2012 menunjukkan rata-rata penyewaan yang lebih tinggi dibandingkan 2011, 
mengindikasikan adanya <b>growth demand</b> dari waktu ke waktu. Pola musiman tetap 
konsisten di kedua tahun, dengan peak terjadi pada pertengahan tahun, yang 
menunjukkan adanya <b>seasonality yang stabil</b>.
</div>
""", unsafe_allow_html=True)

# ======================
# TAB 2: KATEGORI SUHU
# ======================
with tab2:
    fig, ax = plt.subplots()
    sns.barplot(x="temp_category", y="cnt", data=df_filtered, ax=ax)
    ax.set_title("Rata-rata Penyewaan berdasarkan Kategori Suhu")
    st.pyplot(fig)

    st.markdown("""
<div class="insight-box">
<b>Insight:</b><br><br>

Rata-rata penyewaan meningkat seiring kenaikan kategori suhu, dengan kategori 
<b>Panas</b> sebagai yang tertinggi dan <b>Dingin</b> terendah. Hal ini mengonfirmasi 
bahwa suhu merupakan <b>key driver</b> dalam meningkatkan demand penyewaan sepeda.
</div>
""", unsafe_allow_html=True)

# ======================
# TAB 3: UJI STATISTIK
# ======================
with tab3:
    working = df_filtered[df_filtered["workingday_label"] == "Working Day"]["cnt"]
    holiday = df_filtered[df_filtered["workingday_label"] == "Holiday"]["cnt"]

    t_stat, p_value = stats.ttest_ind(working, holiday, equal_var=False)

    st.metric("P-value", f"{p_value:.4f}")

    # FIX LOGIC (NO ERROR)
    if p_value < 0.05:
        hasil_uji = "<b>Terdapat perbedaan signifikan</b> antara hari kerja dan hari libur (p &lt; 0.05)."
    else:
        hasil_uji = "<b>Tidak terdapat perbedaan signifikan</b> antara hari kerja dan hari libur (p ≥ 0.05)."

    st.markdown(f"""
    <div class="insight-box">
    <b>Insight:</b><br><br>

    {hasil_uji}<br><br>

    Hal ini menunjukkan bahwa tipe hari bukan faktor utama dalam menentukan tingkat penyewaan. 
    Permintaan cenderung stabil sepanjang minggu dibandingkan faktor lain seperti cuaca atau musim.
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin:10px 0'>", unsafe_allow_html=True)

# =====================================================
# KESIMPULAN
# =====================================================
st.subheader("Kesimpulan")

st.markdown("""
<div class="insight-box">
<b>Kesimpulan:</b><br><br>

Suhu merupakan faktor utama yang memengaruhi jumlah penyewaan sepeda, dengan hubungan positif yang cukup kuat, 
sementara kelembaban hanya memiliki pengaruh negatif yang lemah.<br><br>

Tren penyewaan menunjukkan pola musiman yang konsisten, di mana permintaan meningkat pada pertengahan tahun 
(Summer–Fall) dan menurun di awal serta akhir tahun, serta terjadi peningkatan penggunaan pada tahun 2012 dibandingkan 2011.<br><br>

Perbedaan penyewaan antara hari kerja dan hari libur tidak signifikan, sehingga variasi permintaan lebih dipengaruhi 
oleh faktor musim dan kondisi cuaca dibandingkan tipe hari.
</div>
""", unsafe_allow_html=True)


# =====================================================
# REKOMENDASI
# =====================================================
st.subheader("Rekomendasi")

st.markdown("""
<div class="insight-box">
<b>Rekomendasi:</b><br><br>

1. Optimalkan ketersediaan sepeda pada periode <b>high demand</b> (Summer–Fall dan suhu tinggi)  
2. Tingkatkan permintaan melalui <b>promosi atau insentif</b> pada musim rendah (Spring & Winter)  
3. Gunakan <b>suhu sebagai indikator utama</b> dalam perencanaan operasional dan alokasi armada  
4. Pertahankan distribusi sepeda yang <b>stabil sepanjang minggu</b> karena tipe hari tidak berpengaruh signifikan  
</div>
""", unsafe_allow_html=True)