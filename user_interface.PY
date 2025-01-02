import tkinter as tk
import bcrypt
from tkinter import ttk, messagebox, Canvas, Button, filedialog,Frame
from calendar import month_name
import calendar
from PIL import Image, ImageTk
from data import load_data, save_data, get_kos_by_id, get_kos_by_owner, get_user_data, update_user_data,simpan_pemesan, update_kamar_status
from validasi import validasi_input, tambah_kos, buat_pesanan, validasi_login,simpan_admin, validasi_pembayaran, validasi_gambar,validasi_login_pemesan, validasi_bukti_transfer, validasi_nominal
import os

class sistem_kos:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem KOS")
        self.root.geometry("1920x1080")
        self.data_file = 'Kos_data.json'
        self.data = load_data(self.data_file)
        style = ttk.Style()
        style.configure("Custom.Treeview", highlightthickness=0, borderwidth=0, background="white", foreground="black", fieldbackground="white")

        self.refresh_status_kamar()
        self.current_user = None 
        self.menu_utama()
        
    def menu_utama(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        # Tambahkan gambar latar belakang
        try:
            bg_image = Image.open("BA1.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
        except FileNotFoundError:
            messagebox.showerror("ERROR", "Gambar tidak ditemukan di direktori!")
            return

        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(relwidth=1, relheight=1)

        # Tombol di atas latar belakang
        Button(self.root, text="PESAN", font=("Arial", 18, "bold"), bg="white", fg="black", width=40, height=3, relief='flat', command=self.halaman_login_pemesan).place(relx=0.5, rely=0.67, anchor='center')
        Button(self.root, text="SEWAKAN", font=("Arial", 18, "bold"), bg="white", fg="black", width=40, height=1,relief='flat', command=self.halaman_login).place(relx=0.5, rely=0.8, anchor='center')
        Button(self.root, text="Exit", font=("Arial", 18, "bold"), bg="red", fg="white", width=20, height=1,relief='flat', command=self.root.quit).place(relx=0.5, rely=0.9, anchor='center')
            
    def halaman_login(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

        # Gambar latar belakang
        try:
            bg_image = Image.open("BLogX.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="white")
            bg_label.place(relwidth=1, relheight=1)

        # Label dan input untuk Username
        tk.Label(self.root, text="Login Admin", font=("Arial", 20, "bold"), bg="white").place(relx=0.5, rely=0.2, anchor='center')
        tk.Label(self.root, text="Username", bg="white", font=("Arial", 14, "bold")).place(relx=0.35, rely=0.35, anchor="w")
        username_entry = tk.Entry(self.root, font=("Arial", 14))
        username_entry.place(relx=0.48, rely=0.35, anchor="w", width=300)

        # Label dan input untuk Password
        tk.Label(self.root, text="Password", bg="white", font=("Arial", 14, "bold")).place(relx=0.35, rely=0.45, anchor="w")
        password_entry = tk.Entry(self.root, show='*', font=("Arial", 14))
        password_entry.place(relx=0.48, rely=0.45, anchor="w", width=300)

        # Checkbutton untuk show/hide password
        show_var = tk.BooleanVar()
        tk.Checkbutton(
            self.root, text="Show Password", variable=show_var,
            command=lambda: password_entry.config(show='' if show_var.get() else '*'),
            bg="white", font=("Arial", 12)
        ).place(relx=0.5, rely=0.52, anchor="w")

        # Fungsi untuk validasi login
        def check_credentials():
            username = username_entry.get()
            password = password_entry.get()
            success, message = validasi_login(username, password)
            if success:
                self.current_user = username  # Simpan pengguna yang sedang login
                messagebox.showinfo("Sukses", message)
                self.halaman_profil()
            else:
                messagebox.showerror("Gagal", message)

        # Tombol Login dan Register
        tk.Button(self.root, text="Login",height=1, bg="#51d451",relief='flat', fg="white", font=("Arial", 14, "bold"), 
                command=check_credentials).place(relx=0.4, rely=0.6, anchor="center", width=200)
        tk.Button(self.root, text="Register Admin",height=1,relief='flat', bg="#187bcd", fg="white", font=("Arial", 14, "bold"), 
                command=self.halaman_register).place(relx=0.6, rely=0.6, anchor="center", width=200)

        # Tombol Kembali
        tk.Button(self.root, text="Kembali", bg="red", fg="white",relief='flat', font=("Arial", 14, "bold"), 
                command=self.menu_utama).place(relx=0.5, rely=0.7, anchor="center", width=200)
  
    def halaman_register(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

        # Gambar latar belakang
        try:
            bg_image = Image.open("BLogX.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)

        # Label dan input untuk Username
        tk.Label(self.root, text="Register Admin", font=("Arial", 20, "bold"), bg="white").place(relx=0.5, rely=0.2, anchor='center')
        tk.Label(self.root, text="Username", bg="white", font=("Arial", 14, "bold")).place(relx=0.35, rely=0.35, anchor="w")
        username_entry = tk.Entry(self.root, font=("Arial", 14))
        username_entry.place(relx=0.48, rely=0.35, anchor="w", width=300)

        # Label dan input untuk Password
        tk.Label(self.root, text="Password", bg="white", font=("Arial", 14, "bold")).place(relx=0.35, rely=0.45, anchor="w")
        password_entry = tk.Entry(self.root, show='*', font=("Arial", 14))
        password_entry.place(relx=0.48, rely=0.45, anchor="w", width=300)

        # Checkbutton untuk show/hide password
        show_var = tk.BooleanVar()
        tk.Checkbutton(
            self.root, text="Show Password", variable=show_var,
            command=lambda: password_entry.config(show='' if show_var.get() else '*'),
            bg="white", font=("Arial", 12)
        ).place(relx=0.5, rely=0.52, anchor="w")

        # Fungsi untuk menyimpan data admin baru
        def save_new_admin():
            
            username = username_entry.get()
            password = password_entry.get()
            success, message = simpan_admin(username, password)
            if success:
                messagebox.showinfo("Sukses", message)
                self.halaman_login()
            else:
                messagebox.showerror("Error", message)

        # Tombol Register dan Kembali
        tk.Button(self.root, text="Register", relief='flat', height=2, bg="#51d451", fg="white", font=("Arial", 14, "bold"),
                command=save_new_admin).place(relx=0.5, rely=0.6, anchor="center", width=500)
        tk.Button(self.root, text="Kembali", relief='flat', bg="red", fg="white", font=("Arial", 14, "bold"),
                command=self.halaman_login).place(relx=0.5, rely=0.68, anchor="center", width=200)

    def halaman_login_pemesan(self):
    
        for widget in self.root.winfo_children():
            widget.destroy()

        # Gambar latar belakang
        try:
            bg_image = Image.open("BLogX.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="white")
            bg_label.place(relwidth=1, relheight=1)

        # Input username dan password
        tk.Label(self.root, text="Login Pemesan", font=("Arial", 20, "bold"), bg="white").place(relx=0.5, rely=0.2, anchor='center')
        tk.Label(self.root, text="Username", bg="white", font=("Arial", 14,'bold')).place(relx=0.35, rely=0.35, anchor="w")
        username_entry = tk.Entry(self.root, font=("Arial", 14))
        username_entry.place(relx=0.48, rely=0.35, anchor="w", width=300)

        tk.Label(self.root, text="Password", bg="white", font=("Arial", 14)).place(relx=0.35, rely=0.45, anchor="w")
        password_entry = tk.Entry(self.root, show='*', font=("Arial", 14, 'bold'))
        password_entry.place(relx=0.48, rely=0.45, anchor="w", width=300)

        # Fungsi validasi login
        def check_login_pemesan():
            username = username_entry.get()
            password = password_entry.get()
            success, pemesan_data = validasi_login_pemesan(username, password)
            if success:
                self.current_user = pemesan_data  # Simpan data pemesan yang login
                messagebox.showinfo("Sukses", "Login berhasil!")
                self.main_menu()
            else:
                messagebox.showerror("Error", pemesan_data)

        # Tombol Login dan Register
        tk.Button(self.root, text="Login", bg="#51d451", fg="white", font=("Arial", 14, "bold"),
                command=check_login_pemesan).place(relx=0.4, rely=0.6, anchor="center", width=150)
        tk.Button(self.root, text="Register", bg="#187bcd", fg="white", font=("Arial", 14, "bold"),
                command=self.halaman_register_pemesan).place(relx=0.6, rely=0.6, anchor="center", width=150)

        # Tombol Kembali
        tk.Button(self.root, text="Kembali", bg="red", fg="white", font=("Arial", 14, "bold"),
                command=self.menu_utama).place(relx=0.5, rely=0.7, anchor="center", width=150)

    def halaman_register_pemesan(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Gambar latar belakang
        try:
            bg_image = Image.open("BLogX.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)

        # Input username dan password
        tk.Label(self.root, text="Register Pemesan", font=("Arial", 20, "bold"), bg="white").place(relx=0.5, rely=0.2, anchor='center')
        tk.Label(self.root, text="Username", bg="white", font=("Arial", 14)).place(relx=0.35, rely=0.35, anchor="w")
        username_entry = tk.Entry(self.root, font=("Arial", 14))
        username_entry.place(relx=0.48, rely=0.35, anchor="w", width=300)

        tk.Label(self.root, text="Password", bg="white", font=("Arial", 14)).place(relx=0.35, rely=0.45, anchor="w")
        password_entry = tk.Entry(self.root, show='*', font=("Arial", 14))
        password_entry.place(relx=0.48, rely=0.45, anchor="w", width=300)

        # Fungsi untuk menyimpan data pemesan baru
        def save_register_pemesan():
            username = username_entry.get()
            password = password_entry.get()
            success, message = simpan_pemesan(username, password)
            if success:
                messagebox.showinfo("Sukses", message)
                self.halaman_login_pemesan()
            else:
                messagebox.showerror("Error", message)

        # Tombol Register dan Kembali
        tk.Button(self.root, text="Register", height=2,bg="#51d451", fg="white", font=("Arial", 14, "bold"),
                command=save_register_pemesan).place(relx=0.5, rely=0.6, anchor="center", width=500)
        tk.Button(self.root, text="Kembali", bg="red", fg="white", font=("Arial", 14, "bold"),
                command=self.halaman_login_pemesan).place(relx=0.5, rely=0.68, anchor="center", width=150)
    
    def halaman_profil(self, background_image_path=None):
     
        for widget in self.root.winfo_children():
            widget.destroy()

        # Tambahkan gambar latar belakang
        try:
            if background_image_path:
                bg_image = Image.open(background_image_path).resize((1920, 1080))
            else:
                bg_image = Image.open("BSew.png").resize((1920, 1080))  # Default
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="white")
            bg_label.place(relwidth=1, relheight=1)

        # Ambil data kos milik pengguna
        user_data = get_user_data(self.data, self.current_user)
        kos_list = [kos for kos in self.data['kos'] if kos.get('owner') == self.current_user]

        # Data Diri
        tk.Label(self.root, text="Data Diri", bg="white", font=("Arial", 14, "bold")).place(relx=0.05, rely=0.05, anchor="nw")
        data_diri = user_data.get('data_diri', {})
        data_text = (
            f"Nama: {data_diri.get('nama', 'Belum diisi')}\n"
            f"Alamat: {data_diri.get('alamat', 'Belum diisi')}\n"
            f"Kontak: {data_diri.get('kontak', 'Belum diisi')}"
        )
        tk.Label(self.root, text=data_text, bg="white", font=("Arial", 12), justify="left").place(relx=0.05, rely=0.1, anchor="nw")
        tk.Button(
            self.root, text="Tambah/Ubah Data Diri", command=self.halaman_tambah_data_diri,
            bg="blue", fg="white", font=("Arial", 12)
        ).place(relx=0.05, rely=0.2, anchor="nw")

        # Frame untuk Daftar Kos
        frame_daftar_kos = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        frame_daftar_kos.place(relx=0.05, rely=0.3, relwidth=0.3, relheight=0.6)

        tk.Label(frame_daftar_kos, text="Daftar Kos", bg="white", font=("Arial", 16, "bold")).pack(pady=5)
        kos_tree = ttk.Treeview(frame_daftar_kos, columns=("ID", "Nama Kos"), show="headings")
        kos_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        kos_tree.heading("ID", text="ID")
        kos_tree.heading("Nama Kos", text="Nama Kos")

        kos_tree.column("ID", width=50, anchor="center")
        kos_tree.column("Nama Kos", width=200, anchor="w")

        # Isi daftar kos
        for kos in kos_list:
            kos_tree.insert("", "end", values=(kos['id'], kos['nama_kos']))

        # Frame untuk Daftar Kamar
        frame_daftar_kamar = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        frame_daftar_kamar.place(relx=0.4, rely=0.3, relwidth=0.3, relheight=0.6)

        tk.Label(frame_daftar_kamar, text="Daftar Kamar", bg="white", font=("Arial", 16, "bold")).pack(pady=5)
        kamar_tree = ttk.Treeview(frame_daftar_kamar, columns=("Nomor", "Ukuran", "Harga", "Fasilitas", "Status"), show="headings")
        kamar_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        kamar_tree.heading("Nomor", text="Nomor")
        kamar_tree.heading("Ukuran", text="Ukuran")
        kamar_tree.heading("Harga", text="Harga")
        kamar_tree.heading("Fasilitas", text="Fasilitas")
        kamar_tree.heading("Status", text="Status")

        kamar_tree.column("Nomor", width=50, anchor="center")
        kamar_tree.column("Ukuran", width=100, anchor="center")
        kamar_tree.column("Harga", width=100, anchor="center")
        kamar_tree.column("Fasilitas", width=200, anchor="w")
        kamar_tree.column("Status", width=100, anchor="center")

        # Frame untuk Detail dan Gambar
        frame_detail = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        frame_detail.place(relx=0.75, rely=0.3, relwidth=0.2, relheight=0.6)

        tk.Label(frame_detail, text="Detail Kos/Kamar", bg="white", font=("Arial", 16, "bold")).pack(pady=5)
        detail_label = tk.Label(frame_detail, text="", bg="white", anchor="nw", justify="left", font=("Arial", 12), wraplength=200)
        detail_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        gambar_label = tk.Label(frame_detail, bg="lightgrey")
        gambar_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Fungsi untuk memperbarui daftar kamar berdasarkan kos yang dipilih
        def update_kamar(event):
            selected_item = kos_tree.selection()
            if selected_item:
                selected_id = kos_tree.item(selected_item)['values'][0]
                selected_kos = next((k for k in kos_list if k['id'] == selected_id), None)
                if selected_kos:
                    # Perbarui daftar kamar
                    kamar_tree.delete(*kamar_tree.get_children())
                    for kamar in selected_kos.get('kamar', []):
                        kamar_tree.insert("", "end", values=(
                            kamar['nomor'], kamar['ukuran'], kamar['harga'], kamar['fasilitas'], kamar['status']
                        ))

        # Fungsi untuk memperbarui detail dan gambar berdasarkan kamar yang dipilih
        def update_detail(event):
            selected_item = kamar_tree.selection()
            if selected_item:
                kamar_data = kamar_tree.item(selected_item)['values']
                selected_kos_item = kos_tree.selection()
                if selected_kos_item:
                    selected_kos_id = kos_tree.item(selected_kos_item)['values'][0]
                    selected_kos = next((k for k in kos_list if k['id'] == selected_kos_id), None)
                    if selected_kos:
                        detail_text = (
                            f"Nama Kos: {selected_kos['nama_kos']}\n"
                            f"Alamat: {selected_kos['alamat']}\n"
                            f"Fasilitas Kos: {selected_kos['fasilitas']}\n"
                            f"Catatan: {selected_kos['catatan']}\n\n"
                            f"Nomor Kamar: {kamar_data[0]}\n"
                            f"Ukuran: {kamar_data[1]}\n"
                            f"Harga: {kamar_data[2]}\n"
                            f"Fasilitas Kamar: {kamar_data[3]}\n"
                            f"Status: {kamar_data[4]}"
                        )
                        detail_label.config(text=detail_text)

                        # Tampilkan gambar kos
                        if selected_kos.get('gambar') and os.path.isfile(selected_kos['gambar']):
                            try:
                                img = Image.open(selected_kos['gambar'])
                                img.thumbnail((200, 200))
                                img_tk = ImageTk.PhotoImage(img)
                                gambar_label.config(image=img_tk)
                                gambar_label.image = img_tk
                            except Exception:
                                gambar_label.config(image="", text="Gambar tidak ditemukan")
                        else:
                            gambar_label.config(image="", text="Tidak ada gambar")

        # Bind event untuk memperbarui data
        kos_tree.bind("<<TreeviewSelect>>", update_kamar)
        kamar_tree.bind("<<TreeviewSelect>>", update_detail)

        # Tombol Kembali dan Tambah Kos
        tk.Button(self.root, text="Kembali", command=self.menu_utama, font=("Arial", 14, "bold"), bg="red", fg="white").place(
            relx=0.05, rely=0.95, anchor="w", width=150, height=40)
        tk.Button(self.root, text="Tambah Kos", command=self.input_kos, font=("Arial", 14, "bold"), bg="green", fg="white").place(
            relx=0.2, rely=0.95, anchor="w", width=150, height=40)

    def halaman_tambah_data_diri(self):
        # Hapus semua widget
        for widget in self.root.winfo_children():
            widget.destroy()
            
        try:
            bg_image = Image.open("BUDD.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)

        # Ambil data pengguna yang sedang login
        user_data = get_user_data(self.data, self.current_user)
        data_diri = user_data.get('data_diri', {})

        # Judul Halaman
        tk.Label(self.root, text="Input atau Perbarui Data Diri", bg="white", font=("Arial", 20, "bold")).place(relx=0.5, rely=0.1, anchor="center")

        # Input Nama
        tk.Label(self.root, text="Nama:", bg="white", font=("Arial", 12)).place(relx=0.3, rely=0.2, anchor="w")
        nama_entry = tk.Entry(self.root, font=("Arial", 12))
        nama_entry.insert(0, data_diri.get('nama', ''))
        nama_entry.place(relx=0.5, rely=0.2, anchor="w", width=300)

        # Input Alamat
        tk.Label(self.root, text="Alamat:", bg="white", font=("Arial", 12)).place(relx=0.3, rely=0.3, anchor="w")
        alamat_entry = tk.Entry(self.root, font=("Arial", 12))
        alamat_entry.insert(0, data_diri.get('alamat', ''))
        alamat_entry.place(relx=0.5, rely=0.3, anchor="w", width=300)

        # Input Kontak
        tk.Label(self.root, text="Kontak:", bg="white", font=("Arial", 12)).place(relx=0.3, rely=0.4, anchor="w")
        kontak_entry = tk.Entry(self.root, font=("Arial", 12))
        kontak_entry.insert(0, data_diri.get('kontak', ''))
        kontak_entry.place(relx=0.5, rely=0.4, anchor="w", width=300)

        # Fungsi Simpan Data
        def simpan_data_diri():
            user_data['data_diri'] = {
                'nama': nama_entry.get(),
                'alamat': alamat_entry.get(),
                'kontak': kontak_entry.get()
            }
            self.data = update_user_data(self.data, self.current_user, user_data)
            save_data(self.data_file, self.data)
            messagebox.showinfo("Sukses", "Data diri berhasil disimpan!")
            self.halaman_profil()

        # Tombol Simpan
        tk.Button(
            self.root, text="Simpan", command=simpan_data_diri, bg="green", fg="white", font=("Arial", 12)
        ).place(relx=0.5, rely=0.5, anchor="center", width=150, height=40)

        # Tombol Kembali
        tk.Button(
            self.root, text="Kembali", command=self.halaman_profil, bg="red", fg="white", font=("Arial", 12)
        ).place(relx=0.5, rely=0.6, anchor="center", width=150, height=40)

    def main_menu (self):
        
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Memuat gambar latar belakang
        try:
            bg_image = Image.open("BMM.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
        except FileNotFoundError:
            messagebox.showerror("ERROR", "Gambar tidak ditemukan di direktori!")

        # Terapkan gambar latar belakang
        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(relwidth=1, relheight=1)

        # Tombol di atas latar belakang tanpa frame
        lihat_data_kos_button = tk.Button(
            self.root, text="Lihat Data Kos",relief='flat', font=("Arial", 18, "bold"),
            bg="white", fg="black", width=20, height=2, command=self.list_kos
        )
        lihat_data_kos_button.place(relx=0.5, rely=0.4, anchor="center")

        pesan_kos_button = tk.Button(
            self.root, text="Pesan Kos",relief='flat', font=("Arial", 18, "bold"),
            bg="white", fg="black", width=20, height=2, command=self.pesan_kos
        )
        pesan_kos_button.place(relx=0.5, rely=0.5, anchor="center")

        lihat_pemesanan_button = tk.Button(
            self.root, text="Lihat Pemesanan",relief='flat', font=("Arial", 18, "bold"),
            bg="white", fg="black", width=20, height=2, command=self.show_list_pemesanan
        )
        lihat_pemesanan_button.place(relx=0.5, rely=0.6, anchor="center")

        kembali_button = tk.Button(
            self.root, text="Kembali",relief='flat', font=("Arial", 18, "bold"),
            bg="red", fg="white", width=20, height=2, command=self.menu_utama
        )
        kembali_button.place(relx=0.5, rely=0.7, anchor="center")

    def input_kos(self):
 
        for widget in self.root.winfo_children():
            widget.destroy()

        # Tambahkan gambar latar belakang
        try:
            bg_image = Image.open("background.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)

        # Frame utama
        main_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.8)

        tk.Label(main_frame, text="Pesan Kos", bg="white", font=("Arial", 18, "bold")).pack(pady=10)

        # Dropdown Kos
        tk.Label(main_frame, text="Pilih Kos:", bg="white", font=("Arial", 12)).pack(anchor="w", padx=20)
        kos_dropdown = ttk.Combobox(main_frame, font=("Arial", 12), values=[kos['nama_kos'] for kos in self.data['kos']])
        kos_dropdown.set("Pilih Kos")
        kos_dropdown.pack(fill="x", padx=20, pady=5)

        # Dropdown Kamar
        tk.Label(main_frame, text="Pilih Kamar:", bg="white", font=("Arial", 12)).pack(anchor="w", padx=20)
        kamar_dropdown = ttk.Combobox(main_frame, font=("Arial", 12))
        kamar_dropdown.set("Pilih Kamar")
        kamar_dropdown.pack(fill="x", padx=20, pady=5)

        # Rekening Pemilik Kos
        rekening_label = tk.Label(main_frame, text="Rekening Pemilik: -", bg="white", font=("Arial", 12, "italic"))
        rekening_label.pack(anchor="w", padx=20, pady=5)

        def update_kamar(*args):
            selected_kos = kos_dropdown.get()
            if selected_kos != "Pilih Kos":
                kos_data = next((k for k in self.data['kos'] if k['nama_kos'] == selected_kos), None)
                if kos_data:
                    kamar_dropdown['values'] = [f"Kamar {k['nomor']}" for k in kos_data['kamar']]
                    kamar_dropdown.set("Pilih Kamar")
                    rekening_label.config(text=f"Rekening Pemilik: {kos_data['rekening']}")

        kos_dropdown.bind("<<ComboboxSelected>>", update_kamar)

        # Input Durasi
        tk.Label(main_frame, text="Bulan Awal:", bg="white", font=("Arial", 12)).pack(anchor="w", padx=20)
        bulan_awal = ttk.Combobox(main_frame, font=("Arial", 12), values=list(month_name[1:]))
        bulan_awal.set("Pilih Bulan")
        bulan_awal.pack(fill="x", padx=20, pady=5)

        tk.Label(main_frame, text="Bulan Akhir:", bg="white", font=("Arial", 12)).pack(anchor="w", padx=20)
        bulan_akhir = ttk.Combobox(main_frame, font=("Arial", 12), values=list(month_name[1:]))
        bulan_akhir.set("Pilih Bulan")
        bulan_akhir.pack(fill="x", padx=20, pady=5)

        # Total Harga
        total_harga_label = tk.Label(main_frame, text="Total Harga: Rp 0", bg="white", font=("Arial", 14, "bold"))
        total_harga_label.pack(anchor="w", padx=20, pady=5)

        # Input Pembayaran
        tk.Label(main_frame, text="Jumlah Uang Dibayarkan:", bg="white", font=("Arial", 12)).pack(anchor="w", padx=20)
        jumlah_uang = tk.Entry(main_frame, font=("Arial", 12))
        jumlah_uang.pack(fill="x", padx=20, pady=5)

        # Bukti Transfer
        bukti_transfer_path = tk.StringVar()
        tk.Label(main_frame, text="Upload Bukti Transfer:", bg="white", font=("Arial", 12)).pack(anchor="w", padx=20)
        tk.Entry(main_frame, textvariable=bukti_transfer_path, font=("Arial", 12), state="readonly").pack(fill="x", padx=20, pady=5)

        def upload_bukti_transfer():
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
            if file_path:
                bukti_transfer_path.set(file_path)

        tk.Button(main_frame, text="Upload", command=upload_bukti_transfer, bg="#51d451", font=("Arial", 12, "bold")).pack(pady=10)

        # Fungsi untuk Memesan
        def pesan_kamar():
            selected_kos = kos_dropdown.get()
            selected_kamar = kamar_dropdown.get()
            if selected_kos == "Pilih Kos" or selected_kamar == "Pilih Kamar" or bulan_awal.get() == "Pilih Bulan" or bulan_akhir.get() == "Pilih Bulan":
                messagebox.showerror("Error", "Harap lengkapi semua data sebelum memesan!")
                return

            kos_data = next((k for k in self.data['kos'] if k['nama_kos'] == selected_kos), None)
            kamar_data = next((k for k in kos_data['kamar'] if f"Kamar {k['nomor']}" == selected_kamar), None)

            bulan_awal_index = list(month_name[1:]).index(bulan_awal.get()) + 1
            bulan_akhir_index = list(month_name[1:]).index(bulan_akhir.get()) + 1
            durasi = bulan_akhir_index - bulan_awal_index + 1
            total_harga = int(kamar_data['harga']) * durasi

            if not jumlah_uang.get() or int(jumlah_uang.get()) < total_harga:
                messagebox.showerror("Error", f"Jumlah uang yang dibayarkan kurang! Minimal: Rp {total_harga:,}")
                return

            # Simpan Pesanan
            pesanan = {
                "kos_id": kos_data['id'],
                "kamar_nomor": kamar_data['nomor'],
                "durasi": durasi,
                "total_harga": total_harga,
            }
            from validasi import buat_pesanan  # Pastikan validasi diimpor
            self.data, pesan = buat_pesanan(self.data, pesanan)
            if pesan == "Pesanan berhasil dibuat.":
                self.refresh_status_kamar()
                messagebox.showinfo("Sukses", pesan)
                self.menu_utama()
            else:
                messagebox.showerror("Error", pesan)

        tk.Button(main_frame, text="Pesan Kamar", command=pesan_kamar, font=("Arial", 14, "bold"), bg="blue", fg="white").pack(pady=10)
        tk.Button(main_frame, text="Kembali", command=self.menu_utama, font=("Arial", 14, "bold"), bg="red", fg="white").pack(pady=10)

    def list_kos(self):
  
        for widget in self.root.winfo_children():
            widget.destroy()

        # Tambahkan gambar latar belakang
        try:
            bg_image = Image.open("BLDKF.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)

        # Filter Harga Kamar
        tk.Label(self.root, text="Filter Kamar Berdasarkan Harga", bg="white", font=("Arial", 16, "bold")).place(relx=0.05, rely=0.03, anchor='w')
        tk.Label(self.root, text="Harga Minimum:", bg="white", font=("Arial", 14)).place(relx=0.05, rely=0.08, anchor='w')
        min_price_entry = tk.Entry(self.root, font=("Arial", 14), width=15)
        min_price_entry.place(relx=0.2, rely=0.08, anchor='w')

        tk.Label(self.root, text="Harga Maksimum:", bg="white", font=("Arial", 14)).place(relx=0.4, rely=0.08, anchor='w')
        max_price_entry = tk.Entry(self.root, font=("Arial", 14), width=15)
        max_price_entry.place(relx=0.55, rely=0.08, anchor='w')

        # Fungsi untuk memfilter kos dan kamar
        def filter_kamar():
            try:
                min_price = int(min_price_entry.get()) if min_price_entry.get() else 0
                max_price = int(max_price_entry.get()) if max_price_entry.get() else float('inf')
            except ValueError:
                messagebox.showerror("Error", "Harga harus berupa angka!")
                return

            # Filter kos berdasarkan kamar yang sesuai harga
            global filtered_kos
            filtered_kos = []
            for kos in self.data['kos']:
                # Ambil hanya kamar yang sesuai dengan filter harga
                kamar_sesuai = [
                    kamar for kamar in kos.get('kamar', [])
                    if min_price <= int(kamar['harga']) <= max_price
                ]
                if kamar_sesuai:  # Kos hanya ditampilkan jika ada kamar yang sesuai
                    kos_copy = kos.copy()
                    kos_copy['kamar'] = kamar_sesuai
                    filtered_kos.append(kos_copy)

            if not filtered_kos:
                messagebox.showinfo("Info", "Tidak ada kos dengan kamar yang sesuai dengan rentang harga.")
            update_kos_tree(filtered_kos)

        tk.Button(self.root, text="Terapkan Filter", command=filter_kamar, bg="#51d451", fg="white", font=("Arial", 14, "bold")).place(relx=0.75, rely=0.08, anchor='w')

        # Frame untuk Daftar Kos
        frame_daftar_kos = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        frame_daftar_kos.place(relx=0.05, rely=0.15, relwidth=0.3, relheight=0.75)

        tk.Label(frame_daftar_kos, text="Daftar Kos", bg="white", font=("Arial", 16, "bold")).pack(pady=5)
        kos_tree = ttk.Treeview(frame_daftar_kos, columns=("ID", "Nama Kos"), show="headings")
        kos_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        kos_tree.heading("ID", text="ID")
        kos_tree.heading("Nama Kos", text="Nama Kos")

        kos_tree.column("ID", width=50, anchor="center")
        kos_tree.column("Nama Kos", width=150, anchor="w")

        # Frame untuk Daftar Kamar
        frame_daftar_kamar = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        frame_daftar_kamar.place(relx=0.4, rely=0.15, relwidth=0.3, relheight=0.75)

        tk.Label(frame_daftar_kamar, text="Daftar Kamar", bg="white", font=("Arial", 16, "bold")).pack(pady=5)
        kamar_tree = ttk.Treeview(frame_daftar_kamar, columns=("Nomor", "Ukuran", "Harga", "Fasilitas", "Status"), show="headings")
        kamar_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        kamar_tree.heading("Nomor", text="Nomor")
        kamar_tree.heading("Ukuran", text="Ukuran")
        kamar_tree.heading("Harga", text="Harga")
        kamar_tree.heading("Fasilitas", text="Fasilitas")
        kamar_tree.heading("Status", text="Status")

        kamar_tree.column("Nomor", width=50, anchor="center")
        kamar_tree.column("Ukuran", width=100, anchor="center")
        kamar_tree.column("Harga", width=100, anchor="center")
        kamar_tree.column("Fasilitas", width=150, anchor="w")
        kamar_tree.column("Status", width=100, anchor="center")

        # Frame untuk Detail dan Gambar
        frame_detail = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        frame_detail.place(relx=0.75, rely=0.15, relwidth=0.2, relheight=0.75)

        tk.Label(frame_detail, text="Detail Kos/Kamar", bg="white", font=("Arial", 16, "bold")).pack(pady=5)
        detail_label = tk.Label(frame_detail, text="", bg="white", anchor="nw", justify="left", font=("Arial", 12), wraplength=200)
        detail_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        gambar_label = tk.Label(frame_detail, bg="lightgrey")
        gambar_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Fungsi untuk memperbarui daftar kos
        def update_kos_tree(kos_list):
            kos_tree.delete(*kos_tree.get_children())
            for kos in kos_list:
                kos_tree.insert("", "end", values=(kos['id'], kos['nama_kos']))

        # Fungsi untuk memperbarui daftar kamar berdasarkan kos yang dipilih
        def update_kamar(event):
            selected_item = kos_tree.selection()
            if selected_item:
                selected_id = kos_tree.item(selected_item)['values'][0]
                selected_kos = next((k for k in filtered_kos if k['id'] == selected_id), None)
                if selected_kos:
                    kamar_tree.delete(*kamar_tree.get_children())
                    for kamar in selected_kos.get('kamar', []):  # Kamar sudah difilter sebelumnya
                        kamar_tree.insert("", "end", values=(
                            kamar['nomor'], kamar['ukuran'], kamar['harga'], kamar['fasilitas'], kamar['status']
                        ))

        # Fungsi untuk memperbarui detail dan gambar berdasarkan kamar yang dipilih
        def update_detail(event):
            selected_item = kamar_tree.selection()
            if selected_item:
                kamar_data = kamar_tree.item(selected_item)['values']
                selected_kos_item = kos_tree.selection()
                if selected_kos_item:
                    selected_kos_id = kos_tree.item(selected_kos_item)['values'][0]
                    selected_kos = next((k for k in filtered_kos if k['id'] == selected_kos_id), None)
                    if selected_kos:
                        detail_text = (
                            f"Nama Kos: {selected_kos['nama_kos']}\n"
                            f"Alamat: {selected_kos['alamat']}\n"
                            f"Fasilitas Kos: {selected_kos['fasilitas']}\n"
                            f"Catatan: {selected_kos['catatan']}\n\n"
                            f"Nomor Kamar: {kamar_data[0]}\n"
                            f"Ukuran: {kamar_data[1]}\n"
                            f"Harga: {kamar_data[2]}\n"
                            f"Fasilitas Kamar: {kamar_data[3]}\n"
                            f"Status: {kamar_data[4]}"
                        )
                        detail_label.config(text=detail_text)

                        # Tampilkan gambar kos
                        if selected_kos.get('gambar') and os.path.isfile(selected_kos['gambar']):
                            try:
                                img = Image.open(selected_kos['gambar'])
                                img.thumbnail((200, 200))
                                img_tk = ImageTk.PhotoImage(img)
                                gambar_label.config(image=img_tk)
                                gambar_label.image = img_tk
                            except Exception:
                                gambar_label.config(image="", text="Gambar tidak ditemukan")
                        else:
                            gambar_label.config(image="", text="Tidak ada gambar")

        # Bind event untuk memperbarui data
        kos_tree.bind("<<TreeviewSelect>>", update_kamar)
        kamar_tree.bind("<<TreeviewSelect>>", update_detail)

        # Isi awal daftar kos
        global filtered_kos
        filtered_kos = self.data['kos']
        update_kos_tree(filtered_kos)

        # Tombol Kembali
        tk.Button(self.root, text="Kembali", command=self.main_menu, font=("Arial", 14, "bold"), bg="red", fg="white").place(
            relx=0.5, rely=0.95, anchor="center", width=200, height=40)

    def pesan_kos(self):
        # Bersihkan layar
        for widget in self.root.winfo_children():
            widget.destroy()

        # Tambahkan gambar latar belakang
        try:
            bg_image = Image.open("background.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)

        # Frame utama
        main_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.8)

        tk.Label(main_frame, text="Pesan Kos", bg="white", font=("Arial", 18, "bold")).pack(pady=10)

        # Dropdown Kos
        tk.Label(main_frame, text="Pilih Kos:", bg="white", font=("Arial", 12)).pack(anchor="w", padx=20)
        kos_dropdown = ttk.Combobox(main_frame, font=("Arial", 12), values=[kos['nama_kos'] for kos in self.data['kos']])
        kos_dropdown.set("Pilih Kos")
        kos_dropdown.pack(fill="x", padx=20, pady=5)

        # Dropdown Kamar
        tk.Label(main_frame, text="Pilih Kamar:", bg="white", font=("Arial", 12)).pack(anchor="w", padx=20)
        kamar_dropdown = ttk.Combobox(main_frame, font=("Arial", 12))
        kamar_dropdown.set("Pilih Kamar")
        kamar_dropdown.pack(fill="x", padx=20, pady=5)

        # Rekening Pemilik Kos
        rekening_label = tk.Label(main_frame, text="Rekening Pemilik: -", bg="white", font=("Arial", 12, "italic"))
        rekening_label.pack(anchor="w", padx=20, pady=5)

        # Total Harga
        total_harga_label = tk.Label(main_frame, text="Total Harga: Rp 0", bg="white", font=("Arial", 14, "bold"))
        total_harga_label.pack(anchor="w", padx=20, pady=5)

        # Pilihan Bulan Awal dan Akhir
        tk.Label(main_frame, text="Bulan Awal:", bg="white", font=("Arial", 12)).pack(anchor="w", padx=20)
        bulan_awal = ttk.Combobox(main_frame, font=("Arial", 12), values=list(calendar.month_name[1:]))
        bulan_awal.set("Pilih Bulan")
        bulan_awal.pack(fill="x", padx=20, pady=5)

        tk.Label(main_frame, text="Bulan Akhir:", bg="white", font=("Arial", 12)).pack(anchor="w", padx=20)
        bulan_akhir = ttk.Combobox(main_frame, font=("Arial", 12), values=list(calendar.month_name[1:]))
        bulan_akhir.set("Pilih Bulan")
        bulan_akhir.pack(fill="x", padx=20, pady=5)

        # Input Jumlah Uang
        tk.Label(main_frame, text="Jumlah Uang Dibayarkan:", bg="white", font=("Arial", 12)).pack(anchor="w", padx=20)
        jumlah_uang = tk.Entry(main_frame, font=("Arial", 12))
        jumlah_uang.pack(fill="x", padx=20, pady=5)

        # Unggah Bukti Pembayaran
        bukti_transfer_path = tk.StringVar()
        tk.Label(main_frame, text="Upload Bukti Pembayaran:", bg="white", font=("Arial", 12)).pack(anchor="w", padx=20)
        tk.Entry(main_frame, textvariable=bukti_transfer_path, font=("Arial", 12), state="readonly").pack(fill="x", padx=20, pady=5)

        def upload_bukti_transfer():
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
            if file_path:
                bukti_transfer_path.set(file_path)

        tk.Button(main_frame, text="Upload", command=upload_bukti_transfer, bg="#51d451", font=("Arial", 12, "bold")).pack(pady=10)

        # Perbarui kamar dan total harga saat kos, kamar, atau durasi berubah
        def update_total_harga(*args):
            selected_kos = kos_dropdown.get()
            selected_kamar = kamar_dropdown.get()

            if selected_kos != "Pilih Kos" and selected_kamar != "Pilih Kamar" and bulan_awal.get() != "Pilih Bulan" and bulan_akhir.get() != "Pilih Bulan":
                kos_data = next((k for k in self.data['kos'] if k['nama_kos'] == selected_kos), None)
                if kos_data:
                    kamar_data = next((k for k in kos_data['kamar'] if f"Kamar {k['nomor']}" in selected_kamar), None)
                    if kamar_data:
                        bulan_awal_index = list(calendar.month_name).index(bulan_awal.get())
                        bulan_akhir_index = list(calendar.month_name).index(bulan_akhir.get())
                        durasi = bulan_akhir_index - bulan_awal_index + 1

                        if durasi > 0:
                            total_harga = int(kamar_data['harga']) * durasi
                            total_harga_label.config(text=f"Total Harga: Rp {total_harga:,}")

        # Perbarui kamar saat kos dipilih
        def update_kamar(*args):
            selected_kos = kos_dropdown.get()
            if selected_kos != "Pilih Kos":
                kos_data = next((k for k in self.data['kos'] if k['nama_kos'] == selected_kos), None)
                if kos_data:
                    kamar_dropdown['values'] = [f"Kamar {k['nomor']} ({k['status']})" for k in kos_data['kamar']]
                    kamar_dropdown.set("Pilih Kamar")
                    rekening_label.config(text=f"Rekening Pemilik: {kos_data['rekening']}")
            update_total_harga()

        kos_dropdown.bind("<<ComboboxSelected>>", update_kamar)
        kamar_dropdown.bind("<<ComboboxSelected>>", update_total_harga)
        bulan_awal.bind("<<ComboboxSelected>>", update_total_harga)
        bulan_akhir.bind("<<ComboboxSelected>>", update_total_harga)

        # Fungsi untuk Memesan
        def pesan_kamar():
            selected_kos = kos_dropdown.get()
            selected_kamar = kamar_dropdown.get()

            if selected_kos == "Pilih Kos" or selected_kamar == "Pilih Kamar" or bulan_awal.get() == "Pilih Bulan" or bulan_akhir.get() == "Pilih Bulan" or not jumlah_uang.get().isdigit() or not bukti_transfer_path.get():
                messagebox.showerror("Error", "Harap lengkapi semua data dengan benar, termasuk jumlah uang dan bukti pembayaran!")
                return

            kos_data = next((k for k in self.data['kos'] if k['nama_kos'] == selected_kos), None)
            if kos_data is None:
                messagebox.showerror("Error", "Kos tidak ditemukan!")
                return

            kamar_data = next((k for k in kos_data['kamar'] if f"Kamar {k['nomor']}" in selected_kamar), None)
            if kamar_data is None:
                messagebox.showerror("Error", "Kamar tidak ditemukan!")
                return

            bulan_awal_index = list(calendar.month_name).index(bulan_awal.get())
            bulan_akhir_index = list(calendar.month_name).index(bulan_akhir.get())
            durasi = bulan_akhir_index - bulan_awal_index + 1

            if durasi <= 0:
                messagebox.showerror("Error", "Durasi tidak valid. Pastikan bulan akhir setelah bulan awal!")
                return

            total_harga = int(kamar_data['harga']) * durasi
            if int(jumlah_uang.get()) < total_harga:
                messagebox.showerror("Error", f"Jumlah uang yang dibayarkan kurang! Minimal: Rp {total_harga:,}")
                return

            # Simpan Pesanan
            pesanan = {
                "kos_id": kos_data['id'],
                "kamar_nomor": kamar_data['nomor'],
                "durasi": durasi,
                "bukti_pembayaran": bukti_transfer_path.get(),
                "jumlah_uang": jumlah_uang.get()
            }
            from validasi import buat_pesanan
            self.data, pesan = buat_pesanan(self.data, pesanan)
            if pesan == "Pesanan berhasil dibuat.":
                self.refresh_status_kamar()
                messagebox.showinfo("Sukses", pesan)
                self.menu_utama()
            else:
                messagebox.showerror("Error", pesan)

        tk.Button(main_frame, text="Pesan Kamar", command=pesan_kamar, font=("Arial", 14, "bold"), bg="blue", fg="white").pack(pady=10)
        tk.Button(main_frame, text="Kembali", command=self.menu_utama, font=("Arial", 14, "bold"), bg="red", fg="white").pack(pady=10)

    def refresh_status_kamar(self):
        self.data = update_kamar_status(self.data)
        save_data(self.data_file, self.data)
    
    def show_list_pemesanan(self):

        if not self.current_user:
            messagebox.showwarning("Peringatan", "Anda harus login terlebih dahulu!")
            self.halaman_login()
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        # Tambahkan latar belakang
        try:
            bg_image = Image.open("BLP2.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)

        tk.Label(self.root, text="Daftar Pemesanan Anda", font=("Arial", 18, "bold"), bg="white").place(relx=0.5, rely=0.1, anchor="center")

        # Filter pemesanan untuk pengguna yang login
        user_pemesanan = [p for p in self.data['pemesanan'] if p.get('username') == self.current_user]

        # Periksa apakah ada pemesanan
        if not user_pemesanan:
            messagebox.showinfo("Info", "Belum ada pemesanan untuk pengguna ini.")
            self.main_menu()
            return

        # Frame untuk Treeview tanpa border
        tree_frame = tk.Frame(self.root, bg="white", bd=0, relief="flat")
        tree_frame.place(relx=0.1, rely=0.2, relwidth=0.5, relheight=0.5)

        # Treeview untuk daftar pemesanan tanpa border
        tree = ttk.Treeview(tree_frame, columns=("ID", "Nama Kos", "Durasi", "Total Harga"), show="headings", style="Custom.Treeview")
        tree.pack(fill=tk.BOTH, expand=True)
        tree.heading("ID", text="ID")
        tree.heading("Nama Kos", text="Nama Kos")
        tree.heading("Durasi", text="Durasi (bulan)")
        tree.heading("Total Harga", text="Total Harga")

        tree.column("ID", anchor="center", width=50)
        tree.column("Nama Kos", anchor="w", width=200)
        tree.column("Durasi", anchor="center", width=100)
        tree.column("Total Harga", anchor="center", width=100)

        for pemesanan in user_pemesanan:
            kos = next((k for k in self.data['kos'] if k['id'] == pemesanan['kos_id']), None)
            kos_name = kos['nama_kos'] if kos else "Kos Tidak Ditemukan"
            durasi = pemesanan.get('durasi', "Tidak Diketahui")
            total_harga = pemesanan.get('total_harga', "Tidak Diketahui")

            tree.insert('', tk.END, values=(pemesanan['id'], kos_name, durasi, total_harga))

        # Area Gambar Kos
        gambar_label = tk.Label(self.root, bg="lightgrey")
        gambar_label.place(relx=0.7, rely=0.2, width=400, height=300)

        # Area Detail Kos
        detail_frame = tk.Frame(self.root, bg="white", bd=0, relief="flat")
        detail_frame.place(relx=0.7, rely=0.55, relwidth=0.25, relheight=0.3)
        tk.Label(detail_frame, text="Detail Kos", bg="white", font=("Arial", 14, "bold")).pack(pady=5)
        detail_label = tk.Label(detail_frame, bg="white", anchor="nw", justify="left", font=("Arial", 12), wraplength=300)
        detail_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        def update_detail(event):
            selected_item = tree.selection()
            if selected_item:
                selected_id = tree.item(selected_item)['values'][0]
                pemesanan = next((p for p in user_pemesanan if p['id'] == selected_id), None)
                if pemesanan:
                    kos = next((k for k in self.data['kos'] if k['id'] == pemesanan['kos_id']), None)
                    if kos:
                        detail_text = (
                            f"Nama Kos: {kos.get('nama_kos', 'N/A')}\n"
                            f"Alamat: {kos.get('alamat', 'N/A')}\n"
                            f"Harga: {kos.get('harga', 'N/A')}\n"
                            f"Fasilitas: {kos.get('fasilitas', 'N/A')}\n"
                            f"Luas Kamar: {kos.get('luas_tempat', 'N/A')} m²\n"
                            f"Status: {kos.get('status', 'N/A')}\n"
                            f"Catatan: {kos.get('catatan', 'Tidak ada catatan')}"
                        )
                        detail_label.config(text=detail_text)

                        # Tampilkan gambar kos
                        if kos.get('gambar') and os.path.isfile(kos['gambar']):
                            try:
                                img = Image.open(kos['gambar'])
                                img.thumbnail((400, 300))
                                img_tk = ImageTk.PhotoImage(img)
                                gambar_label.config(image=img_tk)
                                gambar_label.image = img_tk
                            except FileNotFoundError:
                                gambar_label.config(image="", text="Gambar tidak ditemukan")
                        else:
                            gambar_label.config(image="", text="Tidak ada gambar")

        tree.bind('<<TreeviewSelect>>', update_detail)

        tk.Button(self.root, text="Kembali", command=self.main_menu, bg="red", fg="white", font=("Arial", 14)).place(relx=0.5, rely=0.9, anchor="center")
