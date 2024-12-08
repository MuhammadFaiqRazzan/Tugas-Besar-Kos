import tkinter as tk
import bcrypt
from tkinter import ttk, messagebox, Canvas, Button, filedialog,Frame
from PIL import Image, ImageTk
from data import load_data, save_data, get_kos_by_id, get_kos_by_owner, get_user_data, update_user_data,simpan_pemesan
from validasi import validasi_input, tambah_kos, buat_pesanan, validasi_login,simpan_admin, validasi_pembayaran, validasi_gambar,validasi_login_pemesan
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
        tk.Label(self.root, text="SELAMAT DATANG", font=("Arial", 20, "bold"), bg="white").place(relx=0.5, rely=0.2, anchor='center')
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
                bg_image = Image.open("bg_simple4.png").resize((1920, 1080))  # Default
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="white")
            bg_label.place(relwidth=1, relheight=1)

        # Ambil data pengguna yang sedang login
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
        ).place(relx=0.05, rely=0.25, anchor="nw")

        # Frame untuk Daftar Kos
        frame_daftar_kos = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        frame_daftar_kos.place(relx=0.05, rely=0.35, relwidth=0.32, relheight=0.5)

        # Label dan Treeview untuk Daftar Kos
        tk.Label(frame_daftar_kos, text="Daftar Kos", bg="white", font=("Arial", 16, "bold")).pack(pady=5)
        tree = ttk.Treeview(frame_daftar_kos, columns=('ID', 'Nama Kos'), show='headings')
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tree.heading('ID', text='ID')
        tree.heading('Nama Kos', text='Nama Kos')
        tree.column('ID', width=50, anchor='center')
        tree.column('Nama Kos', width=200, anchor='center')

        for kos in kos_list:
            tree.insert('', tk.END, values=(kos.get('id', 'N/A'), kos.get('nama_kos', 'N/A')))

        # Frame untuk Detail Kos
        detail_frame = tk.Frame(self.root, bg="white", bd=1, relief="solid")
        detail_frame.place(relx=0.4, rely=0.35, relwidth=0.18, relheight=0.3)

        tk.Label(detail_frame, text="Detail Kos", bg="white", font=("Arial", 16, "bold")).pack(pady=5)
        detail_label = tk.Label(
            detail_frame, bg="white", justify="left", anchor="nw", font=("Arial", 12, 'bold'),
            relief="flat"
        )
        detail_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Gambar Kos
        gambar_label = tk.Label(self.root, bg="white")
        gambar_label.place(relx=0.61, rely=0.35, anchor="nw", width=400, height=400)

        # Fungsi untuk memperbarui detail dan gambar kos
        def update_detail(event):
            selected_item = tree.selection()
            if selected_item:
                selected_kos = tree.item(selected_item)['values'][0]
                kos = next((k for k in kos_list if str(k['id']) == str(selected_kos)), None)
                if kos:
                    # Update detail kos
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

                    # Update gambar kos
                    if kos.get('gambar') and os.path.isfile(kos['gambar']):
                        try:
                            img = Image.open(kos['gambar'])
                            img.thumbnail((400, 400))
                            img_tk = ImageTk.PhotoImage(img)
                            gambar_label.config(image=img_tk)
                            gambar_label.image = img_tk
                        except FileNotFoundError:
                            gambar_label.config(image="", text="Gambar tidak ditemukan")
                    else:
                        gambar_label.config(image="", text="Tidak ada gambar")

        tree.bind('<<TreeviewSelect>>', update_detail)

        # Tombol Kembali dan Tambah Kos
        tk.Button(
            self.root, text="Kembali", command=self.menu_utama, font=("Arial", 14, "bold"),
            bg="red", fg="white"
        ).place(relx=0.61, rely=0.85, anchor="nw", width=150, height=40)
        tk.Button(
            self.root, text="Tambah Kos", command=self.input_kos, font=("Arial", 14, "bold"),
            bg="green", fg="white"
        ).place(relx=0.76, rely=0.85, anchor="nw", width=150, height=40)

    def halaman_tambah_data_diri(self):
        # Hapus semua widget
        for widget in self.root.winfo_children():
            widget.destroy()

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

        try:
            # Memuat gambar latar belakang
            bg_image = Image.open("Bg_up1.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
        except FileNotFoundError:
            messagebox.showerror("ERROR", "Gambar tidak ditemukan di direktori!")
            return

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
        # Hapus semua widget
        for widget in self.root.winfo_children():
            widget.destroy()

        # Judul Halaman
        tk.Label(self.root, text="Input Data Kos", bg="white", font=("Arial", 18, "bold")).place(relx=0.5, rely=0.1, anchor="center")

        # Input Nama Kos
        tk.Label(self.root, text="Nama Kos:", bg="white", font=("Arial", 12)).place(relx=0.3, rely=0.2, anchor="w")
        nama_kos = tk.Entry(self.root, font=("Arial", 12))
        nama_kos.place(relx=0.5, rely=0.2, anchor="w", width=300)

        # Input Alamat
        tk.Label(self.root, text="Alamat:", bg="white", font=("Arial", 12)).place(relx=0.3, rely=0.25, anchor="w")
        alamat = tk.Entry(self.root, font=("Arial", 12))
        alamat.place(relx=0.5, rely=0.25, anchor="w", width=300)

        # Input Harga
        tk.Label(self.root, text="Harga per Bulan:", bg="white", font=("Arial", 12)).place(relx=0.3, rely=0.3, anchor="w")
        harga = tk.Entry(self.root, font=("Arial", 12))
        harga.place(relx=0.5, rely=0.3, anchor="w", width=300)

        # Input Fasilitas
        tk.Label(self.root, text="Fasilitas:", bg="white", font=("Arial", 12)).place(relx=0.3, rely=0.35, anchor="w")
        fasilitas = tk.Entry(self.root, font=("Arial", 12))
        fasilitas.place(relx=0.5, rely=0.35, anchor="w", width=300)

        # Input Nomor Rekening
        tk.Label(self.root, text="Nomor Rekening:", bg="white", font=("Arial", 12)).place(relx=0.3, rely=0.4, anchor="w")
        rekening = tk.Entry(self.root, font=("Arial", 12))
        rekening.place(relx=0.5, rely=0.4, anchor="w", width=300)

        # Input Luas Tempat
        tk.Label(self.root, text="Luas Tempat (m²):", bg="white", font=("Arial", 12)).place(relx=0.3, rely=0.45, anchor="w")
        luas_tempat = tk.Entry(self.root, font=("Arial", 12))
        luas_tempat.place(relx=0.5, rely=0.45, anchor="w", width=300)

        # Input Catatan
        tk.Label(self.root, text="Catatan:", bg="white", font=("Arial", 12)).place(relx=0.3, rely=0.5, anchor="w")
        catatan = tk.Entry(self.root, font=("Arial", 12))
        catatan.place(relx=0.5, rely=0.5, anchor="w", width=300)

        # Pilihan Gambar Kos
        tk.Label(self.root, text="Gambar Kos:", bg="white", font=("Arial", 12)).place(relx=0.3, rely=0.55, anchor="w")
        gambar_label = tk.Label(self.root, text="Belum ada gambar", bg="lightgrey", font=("Arial", 10), width=40)
        gambar_label.place(relx=0.5, rely=0.55, anchor="w", width=300)

        def pilih_gambar():
            gambar_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            if gambar_path:
                gambar_label.config(text=gambar_path)

        tk.Button(self.root, text="Pilih Gambar", command=pilih_gambar, font=("Arial", 12)).place(relx=0.5, rely=0.6, anchor="w")

        # Fungsi Simpan Data Kos
        def simpan_data_kos():
            kos_data = {
                'id': len(self.data['kos']) + 1,
                'nama_kos': nama_kos.get(),
                'alamat': alamat.get(),
                'harga': harga.get(),
                'fasilitas': fasilitas.get(),
                'rekening': rekening.get(),
                'luas_tempat': luas_tempat.get(),
                'catatan': catatan.get(),
                'gambar': gambar_label.cget("text"),
                'status': 'Tersedia',
                'owner': self.current_user
            }

            is_valid, message = validasi_input(kos_data)
            if not is_valid:
                messagebox.showwarning("Peringatan", message)
                return

            self.data = tambah_kos(self.data, kos_data)
            save_data(self.data_file, self.data)
            messagebox.showinfo("Sukses", "Data kos berhasil disimpan!")
            self.halaman_profil()

        # Tombol Simpan
        tk.Button(
            self.root, text="Simpan", command=simpan_data_kos, font=("Arial", 12), bg="#51d451", fg="white"
        ).place(relx=0.4, rely=0.7, anchor="center", width=150, height=40)

        # Tombol Kembali
        tk.Button(
            self.root, text="Kembali", command=self.halaman_profil, font=("Arial", 12), bg="red", fg="white"
        ).place(relx=0.6, rely=0.7, anchor="center", width=150, height=40)
        
    def list_kos(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

        # Gambar latar belakang
        try:
            bg_image = Image.open("BLDK2.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)

        # Filter Harga
        tk.Label(self.root, text="Filter Kos Berdasarkan Harga", bg="white", font=("Arial", 16, "bold")).place(relx=0.5, rely=0.05, anchor='n')
        tk.Label(self.root, text="Harga Minimum:", bg="white", font=("Arial", 14)).place(relx=0.3, rely=0.12, anchor='w')
        min_price_entry = tk.Entry(self.root, font=("Arial", 14), width=15)
        min_price_entry.place(relx=0.4, rely=0.12, anchor='w')

        tk.Label(self.root, text="Harga Maksimum:", bg="white", font=("Arial", 14)).place(relx=0.5, rely=0.12, anchor='w')
        max_price_entry = tk.Entry(self.root, font=("Arial", 14), width=15)
        max_price_entry.place(relx=0.6, rely=0.12, anchor='w')

        def filter_kos():
            try:
                min_price = int(min_price_entry.get()) if min_price_entry.get().isdigit() else 0
                max_price = int(max_price_entry.get()) if max_price_entry.get().isdigit() else float('inf')
            except ValueError:
                messagebox.showerror("Error", "Harga harus berupa angka!")
                return

            filtered_kos = [kos for kos in self.data['kos'] if min_price <= int(kos['harga']) <= max_price]
            if not filtered_kos:
                messagebox.showinfo("Info", "Tidak ada kos yang sesuai dengan rentang harga.")
            else:
                update_list(filtered_kos)

        tk.Button(self.root, text="Terapkan Filter", command=filter_kos, bg="#51d451", fg="white", font=("Arial", 14, "bold")).place(relx=0.45, rely=0.17, anchor='w')

        # Frame untuk ID Kos
        id_tree = ttk.Treeview(self.root, columns=('ID', 'Nama Kos'), show='headings', height=20, style="Custom.Treeview")
        id_tree.place(relx=0.05, rely=0.3, relwidth=0.2, relheight=0.5)
        id_tree.heading('ID', text='ID')
        id_tree.heading('Nama Kos', text='Nama Kos')
        id_tree.column('ID', anchor='center', width=50)
        id_tree.column('Nama Kos', anchor='w', width=150)

        def update_list(kos_list):
            for item in id_tree.get_children():
                id_tree.delete(item)
            for kos in kos_list:
                id_tree.insert('', tk.END, values=(kos.get('id', 'N/A'), kos.get('nama_kos', 'N/A')))

        # Frame untuk Detail Kos tanpa border
        detail_frame = tk.Frame(self.root, bg="white", bd=0, relief="flat")
        detail_frame.place(relx=0.3, rely=0.3, relwidth=0.25, relheight=0.5)
        tk.Label(detail_frame, text="Detail Kos", bg="white", font=("Arial", 14, "bold")).pack(pady=5)
        detail_label = tk.Label(detail_frame, bg="white", anchor="nw", justify="left", font=("Arial", 12), wraplength=300)
        detail_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Gambar Kos tanpa border
        gambar_label = tk.Label(self.root, bg="lightgrey")
        gambar_label.place(relx=0.6, rely=0.3, width=400, height=400)

        def update_detail(event):
            selected_item = id_tree.selection()
            if selected_item:
                selected_id = id_tree.item(selected_item)['values'][0]
                kos = next((k for k in self.data['kos'] if str(k['id']) == str(selected_id)), None)
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
                            img.thumbnail((400, 400))
                            img_tk = ImageTk.PhotoImage(img)
                            gambar_label.config(image=img_tk)
                            gambar_label.image = img_tk
                        except FileNotFoundError:
                            gambar_label.config(image="", text="Gambar tidak ditemukan")
                    else:
                        gambar_label.config(image="", text="Tidak ada gambar")

        id_tree.bind('<<TreeviewSelect>>', update_detail)

        update_list(self.data['kos'])

        tk.Button(self.root, text="Kembali", command=self.main_menu, bg="red", fg="white", font=("Arial", 14)).place(relx=0.5, rely=0.9, anchor='center')

    def pesan_kos(self):
    
        if not self.current_user:
            messagebox.showwarning("Peringatan", "Anda harus login terlebih dahulu!")
            self.halaman_login()
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        # Gambar latar belakang
        try:
            bg_image = Image.open("BPK3.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)
            messagebox.showwarning("Peringatan", "Gambar latar belakang tidak ditemukan!")

        # Judul
        tk.Label(self.root, text="Pemesanan Kos", bg="white", font=('Arial', 20, 'bold')).place(relx=0.5, rely=0.1, anchor='center')

        # Ambil data kos yang tersedia
        available_kos = [k for k in self.data['kos'] if k['status'] == 'Tersedia']
        if not available_kos:
            messagebox.showinfo("Info", "Tidak ada kos yang tersedia untuk dipesan.")
            self.main_menu()
            return

        kos_options = {f"{k['id']} - {k['nama_kos']}": k for k in available_kos}

        # Input Pilih Kos
        tk.Label(self.root, text="Pilih Kos:", bg="white", font=("Arial", 14)).place(relx=0.3, rely=0.23, anchor="w")
        kos_var = tk.StringVar(self.root)
        kos_combobox = ttk.Combobox(self.root, textvariable=kos_var, values=list(kos_options.keys()), width=40, font=("Arial", 12))
        kos_combobox.place(relx=0.5, rely=0.23, anchor="w")

        # Input Durasi Sewa
        tk.Label(self.root, text="Durasi Sewa (bulan):", bg="white", font=("Arial", 14)).place(relx=0.3, rely=0.3, anchor="w")
        durasi_entry = tk.Entry(self.root, width=10, font=("Arial", 12))
        durasi_entry.place(relx=0.5, rely=0.3, anchor="w")

        # Nomor Rekening
        tk.Label(self.root, text="Nomor Rekening Tujuan:", bg="white", font=("Arial", 14)).place(relx=0.3, rely=0.37, anchor="w")
        rekening_var = tk.StringVar(self.root)
        rekening_label = tk.Label(self.root, textvariable=rekening_var, bg="lightgrey", font=("Arial", 12), width=30, anchor="w")
        rekening_label.place(relx=0.5, rely=0.37, anchor="w")

        def update_rekening(*args):
            selected_kos = kos_var.get()
            if selected_kos in kos_options:
                rekening_var.set(kos_options[selected_kos]['rekening'])
            else:
                rekening_var.set("")

        kos_var.trace("w", update_rekening)

        # Total Harga
        tk.Label(self.root, text="Total Harga:", bg="white", font=("Arial", 14)).place(relx=0.3, rely=0.44, anchor="w")
        total_harga_var = tk.StringVar(self.root)
        total_harga_label = tk.Label(self.root, textvariable=total_harga_var, bg="lightgrey", font=("Arial", 12), width=30, anchor="w")
        total_harga_label.place(relx=0.5, rely=0.44, anchor="w")

        def update_total_harga(*args):
            selected_kos = kos_var.get()
            if selected_kos in kos_options:
                try:
                    kos_data = kos_options[selected_kos]
                    durasi = int(durasi_entry.get())
                    if durasi > 0:
                        total_harga = int(kos_data['harga']) * durasi
                        total_harga_var.set(f"{total_harga:,}")
                    else:
                        total_harga_var.set("Durasi tidak valid")
                except ValueError:
                    total_harga_var.set("Durasi harus angka")

        durasi_entry.bind("<KeyRelease>", update_total_harga)

        # Input Nominal Pembayaran
        tk.Label(self.root, text="Nominal Pembayaran:", bg="white", font=("Arial", 14)).place(relx=0.3, rely=0.51, anchor="w")
        nominal_entry = tk.Entry(self.root, width=30, font=("Arial", 12))
        nominal_entry.place(relx=0.5, rely=0.51, anchor="w")

        # Upload Bukti Pembayaran
        tk.Label(self.root, text="Upload Bukti Pembayaran:", bg="white", font=("Arial", 14)).place(relx=0.3, rely=0.58, anchor="w")
        upload_label = tk.Label(self.root, text="Belum ada file", bg="lightgrey", font=("Arial", 12), width=40, anchor="w")
        upload_label.place(relx=0.5, rely=0.58, anchor="w")

        def upload_file():
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                upload_label.config(text=file_path)

        tk.Button(self.root, text="Pilih File", command=upload_file, font=("Arial", 12), bg="#187bcd", fg="white").place(relx=0.75, rely=0.58, anchor="w")

        # Tombol Proses Pesan
        def proses_pesan():
            selected_kos = kos_var.get()
            if not selected_kos or selected_kos not in kos_options:
                messagebox.showwarning("Peringatan", "Pilih kos yang ingin dipesan!")
                return

            try:
                kos_data = kos_options[selected_kos]
                durasi = int(durasi_entry.get())
                total_harga = int(total_harga_var.get().replace(",", ""))
                nominal = int(nominal_entry.get())
            except ValueError:
                messagebox.showwarning("Peringatan", "Durasi, nominal, atau total harga tidak valid!")
                return

            # Validasi jika bukti pembayaran belum diunggah
            bukti_pembayaran = upload_label.cget("text")
            if bukti_pembayaran == "Belum ada file":
                messagebox.showwarning("Peringatan", "Unggah bukti pembayaran terlebih dahulu!")
                return

            if nominal < total_harga:
                messagebox.showwarning("Peringatan", f"Nominal pembayaran harus sama dengan total harga yaitu {total_harga:,}!")
                return

            pemesanan_data = {
                'id': len(self.data['pemesanan']) + 1,
                'kos_id': kos_data['id'],
                'durasi': durasi,
                'total_harga': total_harga,
                'nominal': nominal,
                'rekening': kos_data['rekening'],
                'bukti_pembayaran': bukti_pembayaran,
                'username': self.current_user
            }

            # Update status kos dan simpan data pemesanan
            kos_data['status'] = 'Tidak Tersedia'
            self.data['pemesanan'].append(pemesanan_data)
            save_data(self.data_file, self.data)

            messagebox.showinfo("Sukses", f"Kos '{kos_data['nama_kos']}' berhasil dipesan!")
            self.main_menu()

        tk.Button(self.root, text="Pesan", command=proses_pesan, font=("Arial", 14), bg="green", fg="white", width=15).place(relx=0.4, rely=0.7, anchor="center")
        tk.Button(self.root, text="Kembali", command=self.main_menu, font=("Arial", 14), bg="red", fg="white", width=15).place(relx=0.6, rely=0.7, anchor="center")

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
        user_pemesanan = [p for p in self.data['pemesanan'] if 'username' in p and p['username'] == self.current_user]

        # Treeview untuk daftar pemesanan
        tree = ttk.Treeview(self.root, columns=("ID", "Nama Kos", "Durasi", "Total Harga"), show="headings")
        tree.place(relx=0.1, rely=0.2, relwidth=0.5, relheight=0.5)

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
        detail_frame = tk.Frame(self.root, bg="white", bd=2, relief="flat")
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
