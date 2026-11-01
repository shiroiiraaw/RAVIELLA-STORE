import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman Web
st.set_page_config(
    page_title="RAVIELLA STORE - Toko Aplikasi Premium",
    page_icon="💖",
    layout="wide"
)

# ---------------------------------------------------------
# STYLING TEMA PINKY CUTIE & ANIMASI INTERAKTIF HOVER (HTML CSS)
# ---------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Poppins:wght@300;400;600&display=swap');

    html, body, [class*="css"], div, span, label, button, input {
        font-family: 'Poppins', sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Fredoka', cursive !important;
        color: #ff1493 !important;
        letter-spacing: 0.5px;
    }

    .stApp {
        background-color: #fff0f5 !important;
        color: #4a4a4a !important;
    }
    [data-testid="stSidebar"] {
        background-color: #ffe4e1 !important;
    }

    /* KARTU PRODUK INTERAKTIF (EFEK HOVER BERGERAK SAAT DISENTUH) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 2px solid #ffb6c1 !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 12px rgba(255, 182, 193, 0.25) !important;
        transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        cursor: pointer;
    }

    /* EFEK HOVER: KARTU NAIK, MEMBESAR, SERTA GLOW PINK SAAT KURSOR MENEMPEL */
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-10px) scale(1.03) !important;
        border-color: #ff1493 !important;
        box-shadow: 0 15px 30px rgba(255, 20, 147, 0.35) !important;
    }

    /* ANIMASI IKON KETIKA KURSOR DIATAS KARTU PRODUK */
    [data-testid="stVerticalBlockBorderWrapper"]:hover h4 {
        color: #ff1493 !important;
        animation: pulseText 0.6s ease infinite alternate;
    }

    @keyframes pulseText {
        0% { transform: scale(1); }
        100% { transform: scale(1.04); }
    }

    /* TOMBOL PINK GLOW SAAT HOVER */
    .stButton>button {
        background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%) !important;
        color: #ffffff !important;
        border-radius: 16px !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 16px !important;
        box-shadow: 0px 4px 10px rgba(255, 105, 180, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0px 8px 20px rgba(255, 20, 147, 0.5) !important;
    }

    /* LOGO HEADER BERGERAK SAAT KURSOR DIPUTAR */
    .interactive-header {
        display: inline-block;
        transition: transform 0.4s ease;
    }
    .interactive-header:hover {
        transform: rotate(15deg) scale(1.2);
    }
    </style>
""", unsafe_allow_html=True)

ADMIN_PIN = "246810"
KUPON_DISCOUNT = {"DISKON10": 0.10, "AURAVIELLA": 0.20, "PROMOOKTOBER": 0.15}
QRIS_IMAGE_URL = "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=00020101021126580014ID.LINKAJA.WWW01189360091430000000005204599953033605802ID5911STORE_PREMIUM6013JAKARTA_PUSAT61051011062070703A0163041234"

# MASTER

@st.cache_data
def load_data():
    produk_list = [
        # BSTATION
        {"id": 32, "kategori": "BSTATION", "nama": "Bstation Premium Sharing", "durasi": "1 Bulan", "harga": 5000, "stok": 15},
        {"id": 33, "kategori": "BSTATION", "nama": "Bstation Premium Private", "durasi": "1 Bulan", "harga": 25000, "stok": 10},
        
        # CANVA
        {"id": 1, "kategori": "CANVA", "nama": "Canva Member PRO", "durasi": "3 Bulan", "harga": 1000, "stok": 50},
        {"id": 2, "kategori": "CANVA", "nama": "Canva Member PRO + Designer", "durasi": "3 Bulan", "harga": 1500, "stok": 30},
        {"id": 3, "kategori": "CANVA", "nama": "Canva Member EDU", "durasi": "1 Tahun", "harga": 3500, "stok": 50},
        {"id": 4, "kategori": "CANVA", "nama": "Canva Head PRO", "durasi": "3 Bulan", "harga": 5000, "stok": 20},

        # CAPCUT
        {"id": 5, "kategori": "CAPCUT", "nama": "CapCut PRO Private", "durasi": "7 Hari", "harga": 4000, "stok": 15},
        {"id": 6, "kategori": "CAPCUT", "nama": "CapCut PRO Private", "durasi": "30 Hari", "harga": 20000, "stok": 10},
        {"id": 7, "kategori": "CAPCUT", "nama": "CapCut PRO Private", "durasi": "42 Hari", "harga": 25000, "stok": 10},
        {"id": 8, "kategori": "CAPCUT", "nama": "CapCut PRO Sharing (Non-iOS)", "durasi": "30 Hari", "harga": 10000, "stok": 20},

        # DISNEY+ HOTSTAR
        {"id": 9, "kategori": "DISNEY", "nama": "Disney+ Sharing Standar", "durasi": "1 Bulan", "harga": 7000, "stok": 15},
        {"id": 10, "kategori": "DISNEY", "nama": "Disney+ Sharing Premium", "durasi": "1 Bulan", "harga": 15000, "stok": 15},
        {"id": 11, "kategori": "DISNEY", "nama": "Disney+ Premium Standar", "durasi": "1 Bulan", "harga": 25000, "stok": 10},
        {"id": 12, "kategori": "DISNEY", "nama": "Disney+ Premium Premium", "durasi": "1 Bulan", "harga": 80000, "stok": 5},

        # GEMINI AI
        {"id": 13, "kategori": "GEMINI", "nama": "Gemini AI PRO Invite", "durasi": "1 Bulan", "harga": 5000, "stok": 20},
        {"id": 14, "kategori": "GEMINI", "nama": "Gemini AI PRO Invite", "durasi": "3 Bulan", "harga": 10000, "stok": 15},

        # CHATGPT
        {"id": 15, "kategori": "GPT", "nama": "ChatGPT Plus Sharing", "durasi": "1 Bulan", "harga": 20000, "stok": 15},

        # HBO GO MAX
        {"id": 16, "kategori": "HBO", "nama": "HBO GO MAX Sharing Ultimate", "durasi": "1 Bulan", "harga": 10000, "stok": 10},
        {"id": 17, "kategori": "HBO", "nama": "HBO GO MAX Private Standar", "durasi": "1 Bulan", "harga": 18000, "stok": 10},

        # IQIYI
        {"id": 18, "kategori": "IQIYI", "nama": "iQIYI VIP Premium Sharing", "durasi": "1 Bulan", "harga": 5000, "stok": 20},
        {"id": 19, "kategori": "IQIYI", "nama": "iQIYI VIP Premium Private", "durasi": "1 Bulan", "harga": 25000, "stok": 10},

        # LOKLOK
        {"id": 20, "kategori": "LOKLOK", "nama": "Loklok VIP Basic Sharing", "durasi": "30 Hari", "harga": 10000, "stok": 20},

        # NETFLIX
        {"id": 21, "kategori": "NETFLIX", "nama": "Netflix Netcrack (Nogar)", "durasi": "1 Bulan", "harga": 5000, "stok": 30},
        {"id": 22, "kategori": "NETFLIX", "nama": "Netflix Premium Sharing 1P1U", "durasi": "1 Bulan", "harga": 30000, "stok": 15},

        # PICSART
        {"id": 23, "kategori": "PICSART", "nama": "Picsart PRO Indplan", "durasi": "7 Hari", "harga": 4000, "stok": 15},

        # SPOTIFY
        {"id": 24, "kategori": "SPOTIFY", "nama": "Spotify Premium Nogar", "durasi": "1 Bulan", "harga": 6000, "stok": 25},
        {"id": 25, "kategori": "SPOTIFY", "nama": "Spotify Premium Fullgar", "durasi": "1 Bulan", "harga": 12000, "stok": 25},

        # VIDIO
        {"id": 26, "kategori": "VIDIO", "nama": "Vidio.com Platinum Private Mobile", "durasi": "1 Bulan", "harga": 22000, "stok": 15},

        # VISION
        {"id": 27, "kategori": "VISION", "nama": "Vision+ Sports Private", "durasi": "1 Bulan", "harga": 25000, "stok": 10},

        # VPN
        {"id": 28, "kategori": "VPN", "nama": "VPN HMA Premium", "durasi": "1 Bulan", "harga": 5000, "stok": 20},

        # WINK
        {"id": 29, "kategori": "WINK", "nama": "Wink VIP+ Private (Non-iOS)", "durasi": "7 Hari", "harga": 5500, "stok": 15},

        # YOUTUBE
        {"id": 30, "kategori": "YOUTUBE", "nama": "YouTube Premium Indplan (Garansi)", "durasi": "1 Bulan", "harga": 13000, "stok": 20},
        {"id": 31, "kategori": "YOUTUBE", "nama": "YouTube Premium Jaspay (Nogar)", "durasi": "3 Bulan", "harga": 15000, "stok": 20},

        # ZOOM
        {"id": 38, "kategori": "ZOOM", "nama": "Zoom Pro 100 Peserta", "durasi": "1 Bulan", "harga": 30000, "stok": 10},
        {"id": 39, "kategori": "ZOOM", "nama": "Zoom Pro 300 Peserta", "durasi": "1 Bulan", "harga": 60000, "stok": 5},
    ]
    
    penjualan_list = [
        {"tanggal": "2026-10-24", "produk": "Canva Member PRO", "harga_akhir": 1000, "diskon": 0, "pembeli": "Aura"},
        {"tanggal": "2026-10-25", "produk": "YouTube Premium Indplan (Garansi)", "harga_akhir": 13000, "diskon": 0, "pembeli": "Budi"},
    ]
    return pd.DataFrame(produk_list), pd.DataFrame(penjualan_list)

df_produk, df_penjualan = load_data()

# ---------------------------------------------------------
# NAVIGASI SIDEBAR
# ---------------------------------------------------------
st.sidebar.markdown("# 💖 RAVIELLA STORE")
st.sidebar.caption("✨ Cute & Reliable Premium Store ✨")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎀 MENU UTAMA")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["📱 KATALOG PRODUK", "🛒 CHECKOUT & BAYAR", "🔒 DASHBOARD ADMIN"]
)

# ==========================================
# HALAMAN 1: KATALOG PRODUK (INTERAKTIF HOVER)
# ==========================================
if menu == "📱 KATALOG PRODUK":
    col_text, col_anim = st.columns([3, 1])
    with col_text:
        st.title("💖 RAVIELLA STORE")
        st.caption("✨ Arahkan kursor / sentuh kartu produk untuk melihat efek interaktifnya! ✨")
    with col_anim:
        st.markdown('<h1 class="interactive-header" style="font-size: 50px;">🛍️💖</h1>', unsafe_allow_html=True)

    st.divider()

    daftar_kategori = ["Semua Kategori"] + sorted(list(df_produk['kategori'].unique()))
    kategori_pilihan = st.selectbox("🔍 Pilih Kategori Aplikasi:", daftar_kategori)

    if kategori_pilihan != "Semua Kategori":
        df_tampil = df_produk[df_produk['kategori'] == kategori_pilihan]
    else:
        df_tampil = df_produk

    cols = st.columns(3)
    for index, row in df_tampil.reset_index().iterrows():
        col_idx = index % 3
        with cols[col_idx]:
            with st.container(border=True):
                st.markdown(f"#### ⚡ {row['nama']}")
                st.caption(f"🏷️ Kategori: **{row['kategori']}** | ⏱️ **{row['durasi']}**")
                st.markdown(f"### **Rp {row['harga']:,}**")
                if row['stok'] > 0:
                    st.success(f" Ready Stok ({row['stok']})")
                else:
                    st.error(" Stok Habis")

# ==========================================
# HALAMAN 2: CHECKOUT & BAYAR
# ==========================================
elif menu == "🛒 CHECKOUT & BAYAR":
    st.title("🛒 Form Order & Pembayaran QRIS")
    st.caption("Isi data kamu dan scan QRIS untuk menyelesaikan pesanan ✨")
    st.divider()

    with st.container(border=True):
        col_input1, col_input2 = st.columns(2)
        with col_input1:
            nama_pembeli = st.text_input("Nama / No. WhatsApp Pembeli")
            email_pembeli = st.text_input("Email (Untuk Pengiriman Akun/Invite)")
        with col_input2:
            pilihan_app = st.selectbox(
                "Pilih Akun yang Ingin Dibeli", 
                options=[f"{r['id']} - [{r['kategori']}] {r['nama']} ({r['durasi']}) - Rp {r['harga']:,}" for _, r in df_produk.iterrows()]
            )
            kode_diskon = st.text_input("Masukkan Kode Diskon (Jika Ada)", placeholder="Contoh: AURAVIELLA").upper().strip()

        selected_id = int(pilihan_app.split(" - ")[0])
        produk_terpilih = df_produk[df_produk['id'] == selected_id].iloc[0]
        harga_asli = produk_terpilih['harga']
        
        potongan = 0
        if kode_diskon:
            if kode_diskon in KUPON_DISCOUNT:
                persen = KUPON_DISCOUNT[kode_diskon]
                potongan = harga_asli * persen
                st.success(f"🎉 Kode Kupon Berhasil! Diskon {int(persen*100)}% (-Rp {potongan:,.0f})")
            else:
                st.error("❌ Kode diskon tidak valid.")

        total_bayar = max(0, harga_asli - potongan)
        
        st.divider()
        st.markdown(f"## **Total Pembayaran: Rp {total_bayar:,.0f}**")
        
        if st.button("💳 Tampilkan QRIS & Bayar", type="primary", use_container_width=True):
            if not nama_pembeli or not email_pembeli:
                st.warning("⚠️ Harap isi Nama dan Email terlebih dahulu!")
            else:
                @st.dialog("Scan QRIS Pembayaran RAVIELLA STORE")
                def show_qris_dialog():
                    st.write(f"Halo **{nama_pembeli}**, silakan scan QRIS di bawah ini:")
                    st.image(QRIS_IMAGE_URL, width=280)
                    st.markdown(f"### Total Bayar: **Rp {total_bayar:,.0f}**")

                    pesan_wa = (
                        f"Halo Admin RAVIELLA STORE, saya sudah bayar via QRIS!\n\n"
                        f"📌 *Detail Pesanan:*\n"
                        f"- Nama: {nama_pembeli}\n"
                        f"- Email: {email_pembeli}\n"
                        f"- Produk: {produk_terpilih['nama']} ({produk_terpilih['durasi']})\n"
                        f"- Total: Rp {total_bayar:,.0f}\n\n"
                        f"Mohon diproses pesanan saya, terima kasih! 💖"
                    )
                    nomor_wa = "62895620694848"
                    link_wa = f"https://wa.me/{nomor_wa}?text={pesan_wa.replace(' ', '%20').replace('\n', '%0A')}"
                    st.link_button("✅ Konfirmasi Bukti Bayar ke WA Admin", link_wa, use_container_width=True)

                show_qris_dialog()

# ==========================================
# HALAMAN 3: DASHBOARD ADMIN
# ==========================================
elif menu == "🔒 DASHBOARD ADMIN ":
    st.title("🔒 Area Khusus Admin RAVIELLA STORE")
    pin_input = st.text_input("Masukkan PIN Admin untuk Melihat Omzet:", type="password")
    
    if pin_input == ADMIN_PIN:
        st.success("Akses Diterima! Selamat Datang Ravia 🎀")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Omzet", f"Rp {df_penjualan['harga_akhir'].sum():,.0f}")
        col2.metric("Total Pesanan", f"{len(df_penjualan)} Transaksi")
        col3.metric("Total Potongan Diskon", f"Rp {df_penjualan['diskon'].sum():,.0f}")
        
        st.divider()
        st.subheader("📈 Grafis Pendapatan Toko")
        fig = px.bar(df_penjualan, x='tanggal', y='harga_akhir', title="Omzet per Hari (Rp)", color='harga_akhir', color_continuous_scale='purples')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📋 Riwayat Penjualan")
        st.dataframe(df_penjualan, use_container_width=True)