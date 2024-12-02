import tkinter as tk
import bcrypt
from tkinter import ttk, messagebox, Canvas, Button
from PIL import Image, ImageTk
from data import load_data, save_data
from validasi import validasi_input, tambah_kos, buat_pesanan, validasi_login,simpan_admin, validasi_pembayaran

class sistem_kos:
    def __init__(self, root):
        self.root = root
        self.root.title("Sitem KOS")
        self.root.geometry("960x540")
        self.root.resizable(False,False)
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
            bg_image = Image.open("Bg_login.png")
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)
            messagebox.showwarning("Peringatan", "Gambar latar belakang tidak ditemukan!")

        login_frame = tk.Frame(self.root, bg="white", bd=10)
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

        tk.Button(login_frame, text="Login", command=check_credentials, font=("Arial", 12, "bold")).pack(pady=15)
        tk.Button(login_frame, text="Register Admin", command=self.halaman_register, font=("Arial", 12, "bold")).pack(pady=10)
        tk.Button(login_frame, text="Kembali", command=self.menu_utama, font=("Arial", 12, "bold")).pack(pady=10)
        
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

        reg_frame = tk.Frame(self.root, bg="white", bd=10)
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

        tk.Button(reg_frame, text="Register", command=save_new_admin, font=("Arial", 12, "bold")).pack(pady=15)
        tk.Button(reg_frame, text="Kembali", command=self.halaman_login, font=("Arial", 12, "bold")).pack(pady=10)
        
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

    # Memuat gambar latar belakang
        try:
            bg_image = Image.open("Bg_input_kos.png")
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)
            messagebox.showwarning("Peringatan", "Gambar latar belakang tidak ditemukan!")

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

        tk.Label(input_frame, text="Nomor Rekening:", bg="white").grid(row=5, column=0, sticky='w', pady=5)
        rekening = tk.Entry(input_frame, width=40)
        rekening.grid(row=5, column=1, pady=5)

        tk.Label(input_frame, text="Ukuran Kos:", bg="white").grid(row=6, column=0, sticky='w', pady=5)
        ukuran_kos = tk.Entry(input_frame, width=40)
        ukuran_kos.grid(row=6, column=1, pady=5)

        tk.Label(input_frame, text="Nomor Kos:", bg="white").grid(row=7, column=0, sticky='w', pady=5)
        nomor_kos = tk.Entry(input_frame, width=40)
        nomor_kos.grid(row=7, column=1, pady=5)

        tk.Label(input_frame, text="Catatan Tambahan:", bg="white").grid(row=8, column=0, sticky='w', pady=5)
        catatan_tambahan = tk.Entry(input_frame, width=40)
        catatan_tambahan.grid(row=8, column=1, pady=5)

        def simpan_data_kos():
            try:
                harga_value = int(harga.get())
                if harga_value <= 0:
                    messagebox.showwarning("Peringatan", "Harga harus berupa angka positif!")
                    return
            except ValueError:
                messagebox.showwarning("Peringatan", "Harga harus berupa angka!")
                return

            kos_data = {
                'id': len(self.data['kos']) + 1,
                'nama_kos': nama_kos.get(),
                'alamat': alamat.get(),
                'harga': harga.get(),
                'fasilitas': fasilitas.get(),
                'rekening': rekening.get(),
                'ukuran_kos': ukuran_kos.get(),
                'nomor_kos': nomor_kos.get(),
                'catatan': catatan_tambahan.get(),
                'status': 'Tersedia'
            }

            is_valid, message = validasi_input(kos_data)
            if not is_valid:
                messagebox.showwarning("Peringatan", message)
                return
        
            self.data = tambah_kos(self.data, kos_data)
            save_data(self.data_file, self.data)
            messagebox.showinfo("Sukses", "Data kos berhasil disimpan!")
            self.input_kos()

        tk.Button(input_frame, text="Simpan", command=simpan_data_kos, font=("Arial", 12)).grid(row=9, column=0, columnspan=2, pady=10)
        tk.Button(input_frame, text="Kembali", command=self.menu_utama, font=("Arial", 12)).grid(row=10, column=0, columnspan=2, pady=5)

        
    def list_kos(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        try:
            image = Image.open("BackGround.png")
            bg_image = ImageTk.PhotoImage(image)
        except FileNotFoundError:
            messagebox.showerror("ERROR", "Gambar Back Ground Tidak ditemukan ")
            return
        
        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(relwidth=1,relheight=1)

        list_frame = tk.Frame(self.root, bg="white", bd=5)
        list_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8, relheight=0.7)

        tk.Label(list_frame, text="Daftar Kos", font=('Arial', 14, 'bold')).pack(pady=10)
       
        columns = ('ID', 'Nama Kos', 'Alamat', 'Harga', 'Fasilitas', 'Status')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        tree.pack(fill=tk.BOTH, expand=True, pady=10  )
        
        for col in columns:
            tree.heading(col, text=col)
        tree.column(col, width=150)
        tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Mengisi data ke dalam tabel
        for kos in self.data['kos']:
            tree.insert('', tk.END, values=(
                kos['id'],
                kos['nama_kos'],
                kos['alamat'],
                kos['harga'],
                kos['fasilitas'],
                kos['status']
            ))
        
        back_button = tk.Button(self.root, text="Kembali", command=self.main_menu, font=("Arial",12,"bold"))
        back_button.place(relx=0.5, rely=0.9, anchor='center')

   
    def pesan_kos(self):
    
        for widget in self.root.winfo_children():
            widget.destroy()

        pesan_frame = tk.Frame(self.root)
        pesan_frame.pack(padx=20, pady=20)

        tk.Label(pesan_frame, text="Pemesanan Kos", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

    # Menampilkan kos yang tersedia
        available_kos = [k for k in self.data['kos'] if k['status'] == 'Tersedia']
        if not available_kos:
            messagebox.showinfo("Info", "Tidak ada kos yang tersedia untuk dipesan.")
            self.menu_utama()
            return

        kos_options = {f"{k['id']} - {k['nama_kos']}": k for k in available_kos}
        tk.Label(pesan_frame, text="Pilih Kos:").grid(row=1, column=0, sticky='w', pady=5)
        kos_var = tk.StringVar(pesan_frame)
        ttk.Combobox(pesan_frame, textvariable=kos_var, values=list(kos_options.keys())).grid(row=1, column=1, pady=5)

    # Input nominal pembayaran
        tk.Label(pesan_frame, text="Nominal Transfer:").grid(row=2, column=0, sticky='w', pady=5)
        nominal = tk.Entry(pesan_frame, width=40)
        nominal.grid(row=2, column=1, pady=5)

    # Rekening tujuan (diambil otomatis dari kos)
        rekening_var = tk.StringVar(pesan_frame)
        tk.Label(pesan_frame, text="Rekening Tujuan:").grid(row=3, column=0, sticky='w', pady=5)
        rekening_label = tk.Label(pesan_frame, textvariable=rekening_var, bg="white", relief="sunken", width=40)
        rekening_label.grid(row=3, column=1, pady=5)

        def update_rekening(*args):
            selected_kos = kos_var.get()
            if selected_kos in kos_options:
                rekening_var.set(kos_options[selected_kos]['rekening'])
            else:
                rekening_var.set("")

        kos_var.trace("w", update_rekening)

        def validasi_dan_pesan():
            if not kos_var.get():
                messagebox.showwarning("Peringatan", "Pilih kos yang ingin dipesan!")
                return
            kos_data = kos_options.get(kos_var.get())
            if not kos_data:
                messagebox.showerror("Error", "Kos tidak ditemukan!")
                return

            try:
                nominal_value = int(nominal.get())
            except ValueError:
                messagebox.showwarning("Peringatan", "Nominal harus berupa angka!")
                return

            total_harga = int(kos_data['harga'])
            if nominal_value < total_harga:
                messagebox.showwarning("Peringatan", f"Nominal pembayaran kurang! Harus sebesar {total_harga}.")
                return

            confirm = messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin memesan kos '{kos_data['nama_kos']}'?")
            if not confirm:
                return

        # Proses pemesanan
            data_pesanan = {
                'id': len(self.data.get('pemesanan', [])) + 1,
                'kos_id': kos_data['id'],
                'nama_pemesan': "Anonim",
                'telepon': "0000",
                'tanggal_masuk': "TBD",
                'durasi': "TBD",
                'metode_pembayaran': "Transfer Bank",
                'nominal': nominal.get(),
                'rekening': kos_data['rekening']
            }
            self.data, message = buat_pesanan(self.data, data_pesanan)
            if message == "Pemesanan berhasil!":
                save_data(self.data_file, self.data)
                messagebox.showinfo("Sukses", message)
                self.pesan_kos()
            else:
                messagebox.showerror("Error", message)

        tk.Button(pesan_frame, text="Pesan", command=validasi_dan_pesan).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(pesan_frame, text="Kembali", command=self.main_menu).grid(row=5, column=0, columnspan=2, pady=5)

    def show_list_pemesanan(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        try:
            image = Image.open("BackGround.png")
            bg_image = ImageTk.PhotoImage(image)
        except FileNotFoundError:
            bg_image = None
            self.root.configure(bg="lightgrey")
            messagebox.showwarning("Peringatan", "Gambar tidak ditemukan. Menggunakan latar belakang default.")

        if bg_image:
            bg_label = tk.Label(self.root, image=bg_image)
            bg_label.image = bg_image
            bg_label.place(relwidth=1, relheight=1)

        list_frame = tk.Frame(self.root, bg="white", bd=5)
        list_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8, relheight=0.7)

        tk.Label(list_frame, text="Daftar Pemesanan", font=('Arial', 14, 'bold')).pack(pady=10)

        columns = ('ID', 'Nama Kos', 'Nominal', 'Rekening', 'Status')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        if 'pemesanan' in self.data and self.data['pemesanan']:
            for pemesanan in self.data['pemesanan']:
                kos = next((k for k in self.data['kos'] if k['id'] == pemesanan['kos_id']), None)
                kos_name = kos['nama_kos'] if kos else "Tidak Ditemukan"
                tree.insert('', tk.END, values=(
                    pemesanan['id'],
                    kos_name,
                    pemesanan['nominal'],
                    pemesanan['rekening'],
                    kos['status'] if kos else "Tidak Diketahui"
                ))
        else:
            messagebox.showinfo("Info", "Tidak ada data pemesanan yang tersedia.")

        tk.Button(self.root, text="Kembali", command=self.main_menu, font=("Arial", 12, "bold")).place(relx=0.5, rely=0.9, anchor='center')



