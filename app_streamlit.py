import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(
    page_title="Smart IT Asset Lifecycle - Universitas",
    page_icon="💻",
    layout="wide"
)

# Inisialisasi Session State untuk Database Mock / In-Memory Storage
if "assets" not in st.session_state:
    st.session_state.assets = [
        {
            "id": "AST-001",
            "name": "PC Lab Komputer 01",
            "category": "Komputer",
            "unit": "Fakultas Teknik",
            "purchase_date": "2023-01-15",
            "status": "Aktif",
            "health_score": 85,
            "recommendation": "Pertahankan / Layak Pakai",
            "history": [{"date": "2024-06-10", "desc": "Pembersihan debu & ganti pasta termal", "cost": 50000}]
        },
        {
            "id": "AST-002",
            "name": "Core Switch Ruang Server",
            "category": "Jaringan",
            "unit": "Pusat TIK",
            "purchase_date": "2021-05-20",
            "status": "Perlu Perhatian",
            "health_score": 48,
            "recommendation": "Rekomendasi Pensiun / E-Waste",
            "history": [
                {"date": "2023-08-12", "desc": "Penggantian modul power supply", "cost": 750000},
                {"date": "2025-01-10", "desc": "Perbaikan port LAN terbakar", "cost": 300000}
            ]
        }
    ]

# Header Aplikasi
st.title("💻 Smart IT Asset Lifecycle (Universitas)")
st.markdown("Sistem pemantauan umur, kondisi, riwayat perawatan, dan rekomendasi perpanjangan masa pakai berbasis AI.")
st.markdown("---")

# Sidebar untuk Navigasi & Tambah Aset
st.sidebar.header("⚙️ Menu Navigasi")
menu = st.sidebar.radio("Pilih Menu:", ["Dashboard & Daftar Aset", "Tambah Aset Baru"])

# Filter Ringkasan
assets = st.session_state.assets
total_assets = len(assets)
layak_pakai = len([a for a in assets if a["health_score"] >= 60])
perlu_afkir = len([a for a in assets if a["health_score"] < 60])

# Metrik Dashboard Atas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Aset", f"{total_assets} Unit")
with col2:
    st.metric("Layak Pakai", f"{layak_pakai} Unit")
with col3:
    st.metric("Perlu Perhatian / Afkir", f"{perlu_afkir} Unit")

st.markdown("---")

if menu == "Dashboard & Daftar Aset":
    st.subheader("📋 Daftar Aset IT & Rekomendasi Siklus Hidup")
    
    if not assets:
        st.info("Belum ada data aset yang terdaftar.")
    else:
        for idx, asset in enumerate(assets):
            with st.expander(f"📌 [{asset['id']}] {asset['name']} - {asset['unit']} (Skor: {asset['health_score']}%)"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Kategori:** {asset['category']}")
                    st.write(f"**Unit Penempatan:** {asset['unit']}")
                    st.write(f"**Tanggal Pembelian:** {asset['purchase_date']}")
                with c2:
                    st.write(f"**Skor Kesehatan AI:** {asset['health_score']}%")
                    st.markdown(f"**Rekomendasi Siklus:** `:red[{asset['recommendation']}]`" if asset['health_score'] < 60 else f"**Rekomendasi Siklus:** `:green[{asset['recommendation']}]`")
                
                st.markdown("---")
                st.write("🛠️ **Riwayat Perawatan & Servis:**")
                if asset["history"]:
                    for h in asset["history"]:
                        st.caption(f"- Tanggal: {h['date']} | {h['desc']} (Biaya: Rp {h['cost']:,})")
                else:
                    st.caption("Belum ada riwayat perawatan tercatat.")
                
                # Form Tambah Perawatan dalam Expander
                with st.form(key=f"form_maint_{asset['id']}"):
                    st.write("Tambah Catatan Perawatan / Servis")
                    f_date = st.date_input("Tanggal Perbaikan", key=f"date_{asset['id']}")
                    f_desc = st.text_input("Deskripsi Perbaikan (Cth: Ganti SSD/Kipas)", key=f"desc_{asset['id']}")
                    f_cost = st.number_input("Biaya Servis (Rp)", min_value=0, step=10000, key=f"cost_{asset['id']}")
                    
                    submit_maint = st.form_submit_button("Simpan Perawatan & Update AI")
                    if submit_maint:
                        asset["history"].append({"date": str(f_date), "desc": f_desc, "cost": f_cost})
                        asset["health_score"] = max(15, asset["health_score"] - 15)
                        if asset["health_score"] > 75:
                            asset["recommendation"] = "Pertahankan / Layak Pakai"
                        elif asset["health_score"] > 45:
                            asset["recommendation"] = "Rekomendasi Upgrade Komponen (RAM/SSD)"
                        else:
                            asset["recommendation"] = "Rekomendasi Pensiun / E-Waste"
                        st.success(f"Perawatan untuk {asset['id']} berhasil ditambahkan!")
                        st.rerun()

elif menu == "Tambah Aset Baru":
    st.subheader("➕ Form Tambah Aset IT Baru")
    
    with st.form("form_add_asset"):
        new_id = st.text_input("ID Aset (Cth: AST-003)")
        name = st.text_input("Nama Perangkat (Cth: PC Lab Jaringan)")
        category = st.selectbox("Kategori", ["Komputer", "Laptop", "Jaringan", "Server"])
        unit = st.text_input("Unit / Fakultas (Cth: Fakultas Ilmu Komputer)")
        purchase_date = st.date_input("Tanggal Pembelian")
        
        submitted = st.form_submit_button("Simpan Aset Baru")
        if submitted:
            if new_id and name and unit:
                st.session_state.assets.append({
                    "id": new_id,
                    "name": name,
                    "category": category,
                    "unit": unit,
                    "purchase_date": str(purchase_date),
                    "status": "Aktif",
                    "health_score": 90,
                    "recommendation": "Pertahankan / Layak Pakai",
                    "history": []
                })
                st.success(f"Aset {new_id} berhasil ditambahkan!")
            else:
                st.error("Mohon isi semua kolom yang wajib diisi!")