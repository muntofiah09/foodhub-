import streamlit as st
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(
    page_title="FoodHub",
    layout="wide",  # Mengatur layout menjadi wide untuk responsivitas
    initial_sidebar_state="expanded"
)

# Data Menu
menu_makanan = {
    "Nasi Goreng": 25000,
    "Mie Goreng": 20000,
    "Ayam Geprek": 22000,
    "Ayam Penyet": 20000,
    "Sate Ayam": 35000,
    "Ikan Goreng": 15000,
    "Ikan Bakar": 18000,
    "Gado Gado": 17000,
    "Burger": 10000,
    "Kentang Goreng": 10000,
}

menu_minuman = {
    "Teh Manis": 5000,
    "Lemon Tea": 7000,
    "Kopi": 7000,
    "Es Jeruk": 10000,
    "Air Mineral": 3000,
    "Soda": 12000,
    "Milkshake": 25000,
    "Jus": 12000
}

# Inisialisasi sesi pengguna
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "users" not in st.session_state:
    st.session_state.users = {"admin": "admin123", "user1": "12345"}  # Data pengguna contoh
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "order_history" not in st.session_state:
    st.session_state.order_history = {}

# Fungsi untuk autentikasi pengguna
def login(username, password):
    if username in st.session_state.users and st.session_state.users[username] == password:
        st.session_state.logged_in = True
        st.session_state.current_user = username
        if username not in st.session_state.order_history:
            st.session_state.order_history[username] = []
        st.success("Login berhasil!")
    else:
        st.error("Username atau password salah!")

def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.success("Anda telah logout.")

# Fungsi untuk menambahkan item ke keranjang
def add_to_cart(item, quantity):
    if item in st.session_state.cart:
        st.session_state.cart[item] += quantity
    else:
        st.session_state.cart[item] = quantity
    st.success(f"{quantity} {item} ditambahkan ke keranjang!")

# Fungsi untuk menghapus item dari keranjang
def remove_from_cart(item):
    if item in st.session_state.cart:
        del st.session_state.cart[item]
        st.success(f"{item} dihapus dari keranjang!")

# Fungsi untuk menghitung total harga
def calculate_total():
    total = 0
    for item, quantity in st.session_state.cart.items():
        if item in menu_makanan:
            total += menu_makanan[item] * quantity
        elif item in menu_minuman:
            total += menu_minuman[item] * quantity
    return total

# Header aplikasi
st.title("FoodHub")

# Sidebar untuk Autentikasi
with st.sidebar:
    if not st.session_state.logged_in:
        st.header("Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")
            if login_button:
                login(username, password)
    else:
        st.write(f"Selamat datang, {st.session_state.current_user}!")
        if st.button("Logout"):
            logout()

# Tampilkan halaman hanya jika pengguna sudah login
if st.session_state.logged_in:
    # Menu Navigasi
    menu_option = st.sidebar.radio("Navigasi", ["Tampilan Menu", "Pemesanan Makanan", "Bayar Pesanan", "Riwayat Pesanan"])

    # Halaman Tampilan Menu
    if menu_option == "Tampilan Menu":
        st.header("Menu Makanan dan Minuman")
        # Pilihan kategori menu
        kategori = st.selectbox("PILIH KATEGORI MENU", ("Makanan", "Minuman"))

        # Menampilkan daftar menu berdasarkan kategori yang dipilih
        if kategori == "Makanan":
            st.subheader("Daftar Makanan")
            for makanan, harga in menu_makanan.items():
                st.write(f"{makanan}: Rp {harga}")
        elif kategori == "Minuman":
            st.subheader("Daftar Minuman")
            for minuman, harga in menu_minuman.items():
                st.write(f"{minuman}: Rp {harga}")

    # Halaman Pemesanan Makanan
    elif menu_option == "Pemesanan Makanan":
        st.header("Pemesanan Makanan & Minuman")
        with st.form("form_pemesanan"):
            col1, col2 = st.columns(2)  # Form dua kolom
            with col1:
                item = st.selectbox("Pilih Item", list(menu_makanan.keys()) + list(menu_minuman.keys()))
            with col2:
                quantity = st.number_input("Jumlah", min_value=1, step=1)
            submit = st.form_submit_button("Tambahkan ke Keranjang")
            if submit:
                add_to_cart(item, quantity)

        # Keranjang
        st.subheader("Keranjang")
        if st.session_state.cart:
            cart_cols = st.columns(3)  # Desain tabel keranjang tiga kolom
            cart_cols[0].write("Item")
            cart_cols[1].write("Jumlah")
            cart_cols[2].write("Total")
            for item, quantity in st.session_state.cart.items():
                with cart_cols[0]:
                    st.write(item)
                with cart_cols[1]:
                    st.write(quantity)
                with cart_cols[2]:
                    # Pilih menu yang sesuai dengan item
                    if item in menu_makanan:
                        menu = menu_makanan
                    else:
                        menu = menu_minuman
                    st.write(f"Rp {menu[item] * quantity:,}")
                    if st.button(f"Hapus {item}", key=item):
                        remove_from_cart(item)

            st.write(f"Total Harga: Rp {calculate_total():,}")

    # Halaman Bayar Pesanan
    elif menu_option == "Bayar Pesanan":
        st.header("Bayar Pesanan")
        if st.session_state.cart:
            st.subheader("Detail Pesanan")
            for item, quantity in st.session_state.cart.items():
                if item in menu_makanan:
                    menu = menu_makanan
                else:
                    menu = menu_minuman
                st.write(f"{item}: {quantity} x Rp {menu[item]:,} = Rp {menu[item] * quantity:,}")
            total = calculate_total()
            st.write(f"Total: Rp {total:,}")

            # Formulir informasi pembeli
            st.subheader("Informasi Pembeli")
            with st.form("form_pembeli"):
                nama_pembeli = st.text_input("Nama")
                metode_pembayaran = st.radio("Pilih metode pembayaran", ["Tunai", "Kartu Debit", "Qris"])
                submit_pembayaran = st.form_submit_button("Bayar Sekarang")
                if submit_pembayaran:
                    if nama_pembeli:
                        st.success(f"Pesanan berhasil dibayar dengan {metode_pembayaran}!")
                        # Simpan ke riwayat pesanan
                        st.session_state.order_history[st.session_state.current_user].append({
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "items": st.session_state.cart.copy(),
                            "total": total,
                            "payment_method": metode_pembayaran,
                            "pembeli": {
                                "nama": nama_pembeli,
                            }
                        })

    # Halaman Riwayat Pesanan
    elif menu_option == "Riwayat Pesanan":
        st.header("Riwayat Pesanan")
        if st.session_state.order_history[st.session_state.current_user]:
            for order in st.session_state.order_history[st.session_state.current_user]:
                st.write(f"Tanggal  :  {order['date']}")
                st.write(f"Nama Pembeli  :  {order['pembeli']['nama']}")
                for item, quantity in order["items"].items():
                    if item in menu_makanan:
                        menu = menu_makanan
                    else:
                        menu = menu_minuman
                    st.write(f"{item}: {quantity} x Rp {menu[item]:,} = Rp {menu[item] * quantity:,}")
                st.write(f"Total  :  Rp {order['total']:,}")
                st.write(f"Metode Pembayaran  :  {order['payment_method']}")
                st.write("---")
        else:
            st.info("Belum ada riwayat pesanan.")
