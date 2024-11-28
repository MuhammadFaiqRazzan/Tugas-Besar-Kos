import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Button
from PIL import Image, ImageTk
from data import load_data, save_data
from validasi import validasi_input, tambah_kos, buat_pesanan

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
            
        image = Image.open("Bg_login.png") 
        bg_image = ImageTk.PhotoImage(image)
        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.image = bg_image 
        bg_label.place(relwidth=1, relheight=1) 

        login_frame = tk.Frame(self.root, bg="white", bd=10)
        login_frame.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(login_frame, text="Masukkan Password:", bg="white", font=("Norwester", 12, "bold")).pack(pady=10)
        password_entry = tk.Entry(login_frame, show='*', font=("Arial", 12))
        password_entry.pack(pady=5)

        def check_password():
            if password_entry.get() == "admin123":
                self.input_kos()
            else:
                messagebox.showerror("Error", "Password salah!")

        submit_button = tk.Button(login_frame, text="Submit", command=check_password, font=("Arial", 12, "bold"))
        submit_button.pack(pady=15)
        
        back_button = tk.Button(login_frame, text="Kembali", command=self.menu_utama, font=("Arial", 12, "bold"))
        back_button.pack(pady=10)

        
    def main_menu(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

        try:
        # Memuat gambar latar belakang
            bg_image = Image.open("bg_kosinnew.png")
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

        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=20, pady=20)

        tk.Label(input_frame, text="Input Data Kos", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(input_frame, text="Nama Kos:").grid(row=1, column=0, sticky='w', pady=5)
        nama_kos = tk.Entry(input_frame, width=40)
        nama_kos.grid(row=1, column=1, pady=5)

        tk.Label(input_frame, text="Alamat:").grid(row=2, column=0, sticky='w', pady=5)
        alamat = tk.Entry(input_frame, width=40)
        alamat.grid(row=2, column=1, pady=5)

        tk.Label(input_frame, text="Harga per Bulan:").grid(row=3, column=0, sticky='w', pady=5)
        harga = tk.Entry(input_frame, width=40)
        harga.grid(row=3, column=1, pady=5)

        tk.Label(input_frame, text="Fasilitas:").grid(row=4, column=0, sticky='w', pady=5)
        fasilitas = tk.Entry(input_frame, width=40)
        fasilitas.grid(row=4, column=1, pady=5)
        
        def simpan_data_kos():
            kos_data = {
                'id': len(self.data['kos']) + 1,
                'nama_kos': nama_kos.get(),
                'alamat': alamat.get(),
                'harga': harga.get(),
                'fasilitas': fasilitas.get(),
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

        tk.Button(input_frame, text="Simpan", command=simpan_data_kos).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(input_frame, text="Kembali", command=self.menu_utama).grid(row=6, column=0, columnspan=2, pady=5)
        
    def list_kos(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        try:
            image = Image.open("bg_kosinz.png")
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

        # Dropdown untuk memilih kos yang tersedia
        tk.Label(pesan_frame, text="Pilih Kos:").grid(row=1, column=0, sticky='w', pady=5)
        available_kos = [k for k in self.data['kos'] if k['status'] == 'Tersedia']
        kos_options = {k['nama_kos']: k['id'] for k in available_kos}
        kos_var = tk.StringVar(pesan_frame)
        ttk.Combobox(pesan_frame, textvariable=kos_var, values=list(kos_options.keys())).grid(row=1, column=1, pady=5)

        # Form input pemesanan
        tk.Label(pesan_frame, text="Nama Pemesan:").grid(row=2, column=0, sticky='w', pady=5)
        nama_pemesan = tk.Entry(pesan_frame, width=40)
        nama_pemesan.grid(row=2, column=1, pady=5)

        tk.Label(pesan_frame, text="No. Telepon:").grid(row=3, column=0, sticky='w', pady=5)
        telepon = tk.Entry(pesan_frame, width=40)
        telepon.grid(row=3, column=1, pady=5)

        tk.Label(pesan_frame, text="Tanggal Masuk (YYYY-MM-DD):").grid(row=4, column=0, sticky='w', pady=5)
        tanggal = tk.Entry(pesan_frame, width=40)
        tanggal.grid(row=4, column=1, pady=5)

        tk.Label(pesan_frame, text="Durasi (bulan):").grid(row=5, column=0, sticky='w', pady=5)
        durasi = tk.Entry(pesan_frame, width=40)
        durasi.grid(row=5, column=1, pady=5)

        tk.Label(pesan_frame, text="Metode Pembayaran:").grid(row=6, column=0, sticky='w', pady=5)
        metode_var = tk.StringVar(pesan_frame)
        ttk.Combobox(pesan_frame, textvariable=metode_var, values=["Transfer", "Tunai"]).grid(row=6, column=1, pady=5)
    
        def save_kos():
            if not kos_var.get():
                messagebox.showwarning("Peringatan", "Pilih kos yang ingin dipesan!")
                return
            pemesanan_data = {
                'nama_pemesan': nama_pemesan.get(),
                'telepon': telepon.get(),
                'kos_id': kos_options[kos_var.get()],
                'tanggal_masuk': tanggal.get(),
                'durasi': durasi.get(),
                'metode_pembayaran': metode_var.get()
            }
        # Log debugging untuk pemesanan data
            print("Mencoba membuat pesanan dengan data:", pemesanan_data)

            self.data, message = buat_pesanan(self.data, pemesanan_data)
            if message == "Pemesanan berhasil!":
                save_data(self.data_file, self.data)
                messagebox.showinfo("Sukses", message)
                self.pesan_kos()
            else:
                messagebox.showerror("Error", message)
                print("Pesan error:", message)

        tk.Button(pesan_frame, text="Pesan", command=save_kos, width=20, height=2).grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(pesan_frame, text="Kembali", command=self.main_menu, width=20, height=2).grid(row=8, column=0, columnspan=2, pady=5)

    def show_list_pemesanan(self):
    # Membersihkan antarmuka
        for widget in self.root.winfo_children():
            widget.destroy()

        try:
        # Memastikan gambar dapat diload
            image = Image.open("Bg_all.png")
            bg_image = ImageTk.PhotoImage(image)
        except FileNotFoundError:
            messagebox.showerror("ERROR", "Gambar Tidak ditemukan di direktori!")
            return

    # Terapkan gambar latar belakang
        bg_label = tk.Label(self.root, image=bg_image)
        bg_label.image = bg_image  # Simpan referensi gambar agar tidak dibuang oleh garbage collector
        bg_label.place(relwidth=1, relheight=1)

    # Membuat frame untuk daftar pemesanan
        list_frame = tk.Frame(self.root, bg="white", bd=5)
        list_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8, relheight=0.7)

    # Judul daftar pemesanan
        tk.Label(list_frame, text="Daftar Pemesanan", font=('Arial', 14, 'bold')).pack(pady=10)

    # Tabel untuk menampilkan daftar pemesanan
        columns = ('ID', 'Nama Pemesan', 'No. Telepon', 'Kos ID', 'Tanggal Masuk', 'Durasi', 'Metode Pembayaran')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

    # Mengisi data ke dalam tabel
        if 'pemesanan' in self.data and self.data['pemesanan']:
            for pemesanan in self.data['pemesanan']:
                tree.insert('', tk.END, values=(
                    pemesanan['id'],
                    pemesanan['nama_pemesan'],
                    pemesanan['telepon'],
                    pemesanan['kos_id'],
                    pemesanan['tanggal_masuk'],
                    pemesanan['durasi'],
                    pemesanan['metode_pembayaran']
                ))
        else:
            messagebox.showinfo("Info", "Tidak ada data pemesanan yang tersedia.")

    # Tombol kembali
        back_button = tk.Button(self.root, text="Kembali", command=self.main_menu, font=("Arial", 12, "bold"))
        back_button.place(relx=0.5, rely=0.9, anchor='center')



