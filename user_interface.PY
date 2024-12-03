import tkinter as tk
import bcrypt
from tkinter import ttk, messagebox, Canvas, Button, filedialog
from PIL import Image, ImageTk
from data import load_data, save_data, get_kos_by_id
from validasi import validasi_input, tambah_kos, buat_pesanan, validasi_login,simpan_admin, validasi_pembayaran, validasi_gambar
import os

class sistem_kos:
    def __init__(self, root):
        self.root = root
        self.root.title("Sitem KOS")
        self.root.geometry("960x540")
        #self.root.resizable(False,False)
        self.data_file = 'Kos_data.json'
        self.data = load_data(self.data_file)
        self.menu_utama()
        
    def menu_utama(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.canvas = Canvas(self.root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        bg_image = Image.open("BackGround.png")
        self.bg_image = ImageTk.PhotoImage(bg_image)
        self.canvas.create_image(0, 0, image = self.bg_image, anchor="nw",)
        bg_image._expand=True
        
       
        # Tambahkan tombol di atas latar belakang
        self.canvas.create_window(268, 400, window=Button(self.root, font=("Arial",12,"bold"),bg="white", width=20, height=3, text="PENYEWA", command=self.halaman_login))
        self.canvas.create_window(685, 400, window=Button(self.root, font=("Arial",12,"bold"),bg="white", width=20, height=3, text="PEMESAN", command=self.main_menu))
        
    def halaman_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Memuat gambar latar belakang
        try:
            bg_image = Image.open("up desktop.png")
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)
            messagebox.showwarning("Peringatan", "Gambar latar belakang tidak ditemukan!")

        login_frame = tk.Frame(self.root, bg="white", bd=50)
        login_frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(login_frame, text="Username:", bg="white", font=("Norwester", 12, "bold")).pack(pady=5)
        username_entry = tk.Entry(login_frame, font=("Arial", 12))
        username_entry.pack(pady=5)

        tk.Label(login_frame, text="Password:", bg="white", font=("Norwester", 12, "bold")).pack(pady=5)
        password_entry = tk.Entry(login_frame, show='*', font=("Arial", 12))
        password_entry.pack(pady=5)

        def check_credentials():
            username = username_entry.get()
            password = password_entry.get()
            success, message = validasi_login(username, password)
            if success:
                messagebox.showinfo("Success", message)
                self.input_kos()  
            else:
                messagebox.showerror("Error", message)

        tk.Button(login_frame, text="Login",width=12, height= 1,bg= '#51d451', fg='White', relief='flat', command=check_credentials, font=("Arial", 14, "bold")).pack(pady=15)
        tk.Button(login_frame, text="Register Admin", width=12, height=1,bg='#187bcd',fg='White' ,relief= 'flat', command=self.halaman_register, font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(login_frame, text="Kembali", command=self.menu_utama,bg='#f94449',fg='White',relief='flat', font=("Arial", 12, "bold")).pack(pady=25)
        
    def halaman_register(self):
       for widget in self.root.winfo_children():
        widget.destroy()

    # Memuat gambar latar belakang
        try:
            bg_image = Image.open("Bg_register.png")
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)
            messagebox.showwarning("Peringatan", "Gambar latar belakang tidak ditemukan!")

        reg_frame = tk.Frame(self.root, bg="white", bd=30)
        reg_frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(reg_frame, text="Register Admin", bg="white", font=("Norwester", 14, "bold")).pack(pady=10)

        tk.Label(reg_frame, text="Username:", bg="white", font=("Arial", 12)).pack(pady=5)
        username_entry = tk.Entry(reg_frame, font=("Arial", 12))
        username_entry.pack(pady=5)

        tk.Label(reg_frame, text="Password:", bg="white", font=("Arial", 12)).pack(pady=5)
        password_entry = tk.Entry(reg_frame, show='*', font=("Arial", 12))
        password_entry.pack(pady=5)

        def save_new_admin():
            username = username_entry.get()
            password = password_entry.get()
            success, message = simpan_admin(username, password)
            if success:
                messagebox.showinfo("Success", message)
                self.halaman_login()  # Kembali ke halaman login
            else:
                messagebox.showerror("Error", message)

        tk.Button(reg_frame, text="Register", command=save_new_admin,width=12, height= 1,bg= '#51d451', fg='White', relief='flat', font=("Norwester", 12, "bold")).pack(pady=15)
        tk.Button(reg_frame, text="Kembali", command=self.halaman_login,width=12, height= 1,bg= '#f94449', fg='White', relief='flat', font=("Norwester", 12, "bold")).pack(pady=10)
        
    def main_menu(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

        try:
        # Memuat gambar latar belakang
            bg_image = Image.open("bg_kosinz (1).png")
            bg_image = ImageTk.PhotoImage(bg_image)
        except FileNotFoundError:
            messagebox.showerror("ERROR", "Gambar Tidak ditemukan di direktori!")
            return

    # Terapkan gambar latar belakang
        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(relwidth=1, relheight=1)

    # Membuat frame tombol di atas latar belakang
        menu_frame = tk.Frame(self.root, bg="white", bd=5)
        menu_frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Button(menu_frame, text="Lihat Data Kos", command=self.list_kos, width=20, height=2).pack(pady=10)
        tk.Button(menu_frame, text="Pesan Kos", command=self.pesan_kos, width=20, height=2).pack(pady=10)
        tk.Button(menu_frame, text="Lihat Pemesanan", command=self.show_list_pemesanan, width=20, height=2).pack(pady=10)
        tk.Button(menu_frame, text="Kembali", command=self.menu_utama, width=20, height=2).pack(pady=10)

    def input_kos(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Latar belakang gambar
        try:
            bg_image = Image.open("Bg_input_kos.png")
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)

        input_frame = tk.Frame(self.root, bg="white", bd=10)
        input_frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(input_frame, text="Input Data Kos", bg="white", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(input_frame, text="Nama Kos:", bg="white").grid(row=1, column=0, sticky='w', pady=5)
        nama_kos = tk.Entry(input_frame, width=40)
        nama_kos.grid(row=1, column=1, pady=5)

        tk.Label(input_frame, text="Alamat:", bg="white").grid(row=2, column=0, sticky='w', pady=5)
        alamat = tk.Entry(input_frame, width=40)
        alamat.grid(row=2, column=1, pady=5)

        tk.Label(input_frame, text="Harga per Bulan:", bg="white").grid(row=3, column=0, sticky='w', pady=5)
        harga = tk.Entry(input_frame, width=40)
        harga.grid(row=3, column=1, pady=5)

        tk.Label(input_frame, text="Fasilitas:", bg="white").grid(row=4, column=0, sticky='w', pady=5)
        fasilitas = tk.Entry(input_frame, width=40)
        fasilitas.grid(row=4, column=1, pady=5)

        tk.Label(input_frame, text="Nomor Kamar:", bg="white").grid(row=5, column=0, sticky='w', pady=5)
        nomor_kamar = tk.Entry(input_frame, width=40)
        nomor_kamar.grid(row=5, column=1, pady=5)

        tk.Label(input_frame, text="Nomor Rekening:", bg="white").grid(row=6, column=0, sticky='w', pady=5)
        rekening = tk.Entry(input_frame, width=40)
        rekening.grid(row=6, column=1, pady=5)
        
        tk.Label(input_frame, text="Luas Kamar (m²):", bg="white").grid(row=8, column=0, sticky='w', pady=5)
        luas_kamar = tk.Entry(input_frame, width=40)
        luas_kamar.grid(row=8, column=1, pady=5)

        tk.Label(input_frame, text="Catatan:", bg="white").grid(row=7, column=0, sticky='w', pady=5)
        catatan = tk.Entry(input_frame, width=40)
        catatan.grid(row=7, column=1, pady=5)

        tk.Label(input_frame, text="Gambar Kos:", bg="white").grid(row=8, column=0, sticky='w', pady=5)
        gambar_label = tk.Label(input_frame, text="Belum ada gambar", bg="lightgrey", relief="sunken", width=30)
        gambar_label.grid(row=8, column=1, pady=5)

        def pilih_gambar():
            gambar_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            if gambar_path:
                gambar_label.config(text=gambar_path)

        tk.Button(input_frame, text="Pilih Gambar", command=pilih_gambar, font=("Arial", 10)).grid(row=9, column=1, sticky='w', pady=5)

        def simpan_data_kos():
            kos_data = {
                'id': len(self.data['kos']) + 1,
                'nama_kos': nama_kos.get(),
                'alamat': alamat.get(),
                'harga': harga.get(),
                'fasilitas': fasilitas.get(),
                'nomor_kamar': nomor_kamar.get(),
                'rekening': rekening.get(),
                'catatan': catatan.get(),
                'luas_kamar': luas_kamar.get(),
                'gambar': gambar_label.cget("text"),
                'status': 'Tersedia'
            }

        # Validasi data input
            is_valid, message = validasi_input(kos_data)
            if not is_valid:
                messagebox.showwarning("Peringatan", message)
                return

        # Tambahkan data kos ke dalam JSON
            self.data = tambah_kos(self.data, kos_data)
            save_data(self.data_file, self.data)
            messagebox.showinfo("Sukses", "Data kos berhasil disimpan!")
            self.input_kos()

        tk.Button(input_frame, text="Simpan", command=simpan_data_kos, font=("Arial", 12)).grid(row=10, column=0, columnspan=2, pady=10)
        tk.Button(input_frame, text="Kembali", command=self.menu_utama, font=("Arial", 12)).grid(row=11, column=0, columnspan=2, pady=5)

    def list_kos(self):
        # Validasi data awal
        if not self.data or 'kos' not in self.data or not isinstance(self.data['kos'], list):
            messagebox.showinfo("Info", "Tidak ada data kos untuk ditampilkan.")
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame luar
        outer_frame = tk.Frame(self.root, bg="white", bd=10)
        outer_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.9, relheight=0.8)

        # Frame 1: Daftar kos
        list_frame = tk.Frame( outer_frame, bg="white", bd=10, relief='flat')
        list_frame.place(relx=0.1, rely=0.5, anchor='w', relwidth=0.3, relheight=1.0)

        tk.Label(list_frame, text="Daftar Kos", bg="white", font=('Arial', 14, 'bold')).pack(pady=10)

        columns = ('ID', 'Nama Kos')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=100)

        for kos in self.data['kos']:
            tree.insert('', tk.END, values=(kos.get('id', 'N/A'), kos.get('nama_kos', 'N/A')))

        # Frame 2: Detail kos
        detail_frame = tk.Frame( outer_frame, bg="white", bd=10, relief='flat')
        detail_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.2, relheight=1.0)

        tk.Label(detail_frame, text="Detail Kos", bg="white", font=('Arial', 14, 'bold')).pack(pady=10)

        detail_text_label = tk.Label(detail_frame, text="", bg="white", justify="left", anchor="w", relief="sunken", width=30, height=15)
        detail_text_label.pack(fill=tk.BOTH, expand=True, pady=10)

        # Frame 3: Gambar kos
        gambar_frame = tk.Frame(outer_frame, bg="white", bd=10, relief='flat')
        gambar_frame.place(relx=0.9, rely=0.5, anchor='e', relwidth=0.3, relheight=1.0)

        tk.Label(gambar_frame, text="Gambar Kos", bg="white", font=('Arial', 14, 'bold')).pack(pady=10)

        gambar_label = tk.Label(gambar_frame, bg="lightgrey", relief="sunken", width=30, height=15)
        gambar_label.pack(fill=tk.BOTH, expand=True, pady=10)

        def update_detail(event):
            selected_item = tree.selection()
            if selected_item:
                selected_id = tree.item(selected_item)['values'][0]
                kos = get_kos_by_id(self.data, selected_id)  # Menggunakan fungsi dari data.py
                if kos:
                    detail_text = (
                        f"Nama Kos: {kos.get('nama_kos', 'N/A')}\n"
                        f"Alamat: {kos.get('alamat', 'N/A')}\n"
                        f"Harga: {kos.get('harga', 'N/A')}\n"
                        f"Fasilitas: {kos.get('fasilitas', 'N/A')}\n"
                        f"Luas Kamar: {kos.get('luas_kamar', 'N/A')} m²\n"
                        f"Status: {kos.get('status', 'N/A')}\n"
                        f"Catatan: {kos.get('catatan', 'Tidak ada catatan')}"
                    )
                    detail_text_label.config(text=detail_text)

                    # Tampilkan gambar kos
                    if kos.get('gambar'):
                        try:
                            img = Image.open(kos['gambar'])
                            img.thumbnail((200, 200))
                            img_tk = ImageTk.PhotoImage(img)
                            gambar_label.config(image=img_tk, text="", compound='top')
                            gambar_label.image = img_tk
                        except FileNotFoundError:
                            gambar_label.config(image="", text="Gambar tidak ditemukan", compound='none')
                    else:
                        gambar_label.config(image="", text="Tidak ada gambar", compound='none')

        tree.bind('<<TreeviewSelect>>', update_detail)

        tk.Button(self.root, text="Kembali", command=self.main_menu, font=("Arial", 12, "bold")).place(relx=0.5, rely=0.9, anchor='center')

    
    def pesan_kos(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    # Tambahkan latar belakang
        try:
            bg_image = Image.open("Pesan_Kos_BG.png")
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)
            messagebox.showwarning("Peringatan", "Gambar latar belakang tidak ditemukan!")

        pesan_frame = tk.Frame(self.root, bg="white", bd=10)
        pesan_frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(pesan_frame, text="Pemesanan Kos", bg="white", font=('Arial', 14, 'bold')).pack(pady=10)

    # Kos yang tersedia
        available_kos = [k for k in self.data['kos'] if k['status'] == 'Tersedia']
        if not available_kos:
            messagebox.showinfo("Info", "Tidak ada kos yang tersedia untuk dipesan.")
            self.menu_utama()
            return

        kos_options = {f"{k['id']} - {k['nama_kos']}": k for k in available_kos}
        tk.Label(pesan_frame, text="Pilih Kos:", bg="white").pack(pady=5)
        kos_var = tk.StringVar(pesan_frame)
        kos_combobox = ttk.Combobox(pesan_frame, textvariable=kos_var, values=list(kos_options.keys()), width=40)
        kos_combobox.pack(pady=5)

    # Nomor rekening
        tk.Label(pesan_frame, text="Nomor Rekening Tujuan:", bg="white").pack(pady=5)
        rekening_var = tk.StringVar(pesan_frame)
        rekening_label = tk.Label(pesan_frame, textvariable=rekening_var, bg="lightgrey", width=30)
        rekening_label.pack(pady=5)

        def update_rekening(*args):
            selected_kos = kos_var.get()
            if selected_kos in kos_options:
                rekening_var.set(kos_options[selected_kos]['rekening'])
            else:
                rekening_var.set("")

        kos_var.trace("w", update_rekening)

    # Input durasi
        tk.Label(pesan_frame, text="Durasi Sewa (bulan):", bg="white").pack(pady=5)
        durasi_entry = tk.Entry(pesan_frame, width=30)
        durasi_entry.pack(pady=5)

    # Total harga
        tk.Label(pesan_frame, text="Total Harga:", bg="white").pack(pady=5)
        total_harga_var = tk.StringVar(pesan_frame)
        total_harga_label = tk.Label(pesan_frame, textvariable=total_harga_var, bg="lightgrey", width=30)
        total_harga_label.pack(pady=5)

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

    # Nominal pembayaran
        tk.Label(pesan_frame, text="Nominal Pembayaran:", bg="white").pack(pady=5)
        nominal_entry = tk.Entry(pesan_frame, width=30)
        nominal_entry.pack(pady=5)

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

            if nominal < total_harga:
                messagebox.showwarning("Peringatan", f"Nominal pembayaran harus sama dengan total harga yaitu {total_harga}!")
                return

            kos_data['status'] = 'Tidak Tersedia'
            pemesanan_data = {
                'id': len(self.data['pemesanan']) + 1,
                'kos_id': kos_data['id'],
                'durasi': durasi,
                'total_harga': total_harga,
                'nominal': nominal,
                'rekening': kos_data['rekening']
            }
            self.data['pemesanan'].append(pemesanan_data)
            save_data(self.data_file, self.data)
            messagebox.showinfo("Sukses", f"Kos '{kos_data['nama_kos']}' berhasil dipesan!")
            self.menu_utama()

        tk.Button(pesan_frame, text="Pesan", command=proses_pesan, font=("Arial", 12)).pack(pady=10)
        tk.Button(pesan_frame, text="Kembali", command=self.menu_utama, font=("Arial", 12)).pack(pady=5)
        
    def show_list_pemesanan(self):
    # Bersihkan widget sebelumnya
        for widget in self.root.winfo_children():
            widget.destroy()

    # Tambahkan latar belakang
        try:
            image = Image.open("BackGround.png")
            bg_image = ImageTk.PhotoImage(image)
            bg_label = tk.Label(self.root, image=bg_image)
            bg_label.image = bg_image
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)
            messagebox.showwarning("Peringatan", "Gambar tidak ditemukan! Menggunakan latar belakang default.")

    # Frame untuk daftar pemesanan
        list_frame = tk.Frame(self.root, bg="white", bd=5)
        list_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.9, relheight=0.8)

        tk.Label(list_frame, text="Daftar Pemesanan", font=('Arial', 14, 'bold'), bg="white").pack(pady=10)

    # Definisikan kolom untuk Treeview
        columns = ('ID', 'Nama Kos', 'Durasi (bulan)', 'Total Harga', 'Nominal', 'Rekening', 'Status')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

    # Set nama kolom
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=120)

    # Validasi dan pengisian data
        if 'pemesanan' in self.data and isinstance(self.data['pemesanan'], list):
            for pemesanan in self.data['pemesanan']:
            # Validasi setiap data pemesanan
                if not isinstance(pemesanan, dict):
                    continue  # Lewati data yang tidak valid

                kos = next((k for k in self.data['kos'] if k['id'] == pemesanan.get('kos_id')), None)
                kos_name = kos['nama_kos'] if kos else "Kos tidak ditemukan"
                status = kos['status'] if kos else "Tidak Diketahui"

                tree.insert('', tk.END, values=(
                    pemesanan.get('id', "Tidak Ada ID"),
                    kos_name,
                    pemesanan.get('durasi', "Tidak Ada Durasi"),
                    pemesanan.get('total_harga', "Tidak Ada Harga"),
                    pemesanan.get('nominal', "Tidak Ada Nominal"),
                    pemesanan.get('rekening', "Tidak Ada Rekening"),
                    status
                ))
        else:
            messagebox.showinfo("Info", "Tidak ada data pemesanan yang tersedia.")

    # Tombol kembali
        tk.Button(self.root, text="Kembali", command=self.main_menu, font=("Arial", 12, "bold")).place(relx=0.5, rely=0.9, anchor='center')
