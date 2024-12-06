import tkinter as tk
import bcrypt
from tkinter import ttk, messagebox, Canvas, Button, filedialog,Frame
from PIL import Image, ImageTk
from data import load_data, save_data, get_kos_by_id, get_kos_by_owner, get_user_data, update_user_data
from validasi import validasi_input, tambah_kos, buat_pesanan, validasi_login,simpan_admin, validasi_pembayaran, validasi_gambar
import os

class sistem_kos:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem KOS")
        self.root.geometry("1920x1080")
        self.data_file = 'Kos_data.json'
        self.data = load_data(self.data_file)
        self.current_user = None 
        self.menu_utama()
        
    def menu_utama(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        # Tambahkan gambar latar belakang
        try:
            bg_image = Image.open("Bg_up1.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
        except FileNotFoundError:
            messagebox.showerror("ERROR", "Gambar tidak ditemukan di direktori!")
            return

        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(relwidth=1, relheight=1)

        # Tombol di atas latar belakang
        Button(self.root, text="PESAN", font=("Arial", 18, "bold"), bg="#51d451", fg="white", width=20, height=2, command=self.main_menu).place(relx=0.5, rely=0.7, anchor='center')
        Button(self.root, text="SEWAKAN", font=("Arial", 18, "bold"), bg="#187bcd", fg="white", width=20, height=2, command=self.halaman_login).place(relx=0.5, rely=0.8, anchor='center')
        Button(self.root, text="Exit", font=("Arial", 18, "bold"), bg="red", fg="white", width=20, height=2, command=self.root.quit).place(relx=0.5, rely=0.9, anchor='center')
        
    def halaman_login(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

        # Gambar latar belakang
        try:
            bg_image = Image.open("Bg_up1.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="white")
            bg_label.place(relwidth=1, relheight=1)

        # Frame untuk login
        login_frame = tk.Frame(self.root, bg="white",relief='groove', bd=0.5)
        login_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.4, relheight=0.7)
        
        tk.Label(login_frame, text='SELAMAT DATANG',font=('Arial', 20, 'bold'),bg='white').place(x=220, y=100)

        tk.Label(login_frame, text='Username',bg="white", font=("Arial", 14, "bold")).place(x=100,y=190)
        username_entry = tk.Entry(login_frame,border=0,relief='flat', font=("Arial", 14))
        username_entry.place(x=110, y=235)
        Frame(login_frame,width=490, height=2, bg='black').place(x=100,y=260)
        
        tk.Label(login_frame, text="Password", bg="white", font=("Arial", 14, "bold")).place(x=100,y=280)
        password_entry = tk.Entry(login_frame,border=0,width=45, show='*', font=("Arial", 14))
        password_entry.place(x=110, y=320)
        Frame(width=490, height=2, bg='black').place(x=615,y=490)
        
        def toggle_password():
            if show_var.get():  # Jika checkbox dicentang
                password_entry.config(show="")  # Tampilkan teks sebenarnya
            else:
                password_entry.config(show="*")  # Sembunyikan teks dengan simbol '*'

        # Tambahkan Checkbutton untuk show/hide password
        show_var = tk.BooleanVar()
        show_password_cb = tk.Checkbutton(
            login_frame,
            text="Show Password",
            variable=show_var,
            command=toggle_password,
            bg="white",
            font=("Arial", 12)
        )

        show_password_cb.place(x=100, y=360)

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

        Button(login_frame,width=40,relief='flat', text="Login", bg='#51d451', fg='White', font=("Arial", 14, "bold"), command=check_credentials).place(x=100,y=400)
        Button(login_frame,width=40,relief='flat', text="Register Admin", bg='#187bcd', fg='White', font=("Arial", 14, "bold"), command=self.halaman_register).place(x=100,y=450)
        Button(login_frame, relief='flat',text="Kembali", bg='#f94449', fg='White', font=("Arial", 14, "bold"), command=self.menu_utama).place(x=295,y=550)
    
    def halaman_register(self):
       
        for widget in self.root.winfo_children():
            widget.destroy()

        # Gambar latar belakang
        try:
            bg_image = Image.open("Bg_up1.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)
            messagebox.showwarning("Peringatan", "Gambar latar belakang tidak ditemukan!")

        reg_frame = tk.Frame(self.root, bg="white", bd=30)
        reg_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.4, relheight=0.7)

        tk.Label(reg_frame, text="Register Admin", bg="white", font=("Arial", 30, "bold")).place(x=170, y=90)

        tk.Label(reg_frame, text="Username:", bg="white", font=("Arial", 14)).place(x=70,y=200)
        username_entry = tk.Entry(reg_frame,border=0,width=43, font=("Arial", 14))
        username_entry.place(x=75, y=230)
        Frame(reg_frame,width=490, height=2, bg='black').place(x=70,y=260)
            
        tk.Label(reg_frame, text="Password:", bg="white", font=("Arial", 14)).place(x=70,y=280)
        password_entry = tk.Entry(reg_frame, border=0,show='*',width=43, font=("Arial", 14))
        password_entry.place(x=75, y=310)
        Frame(width=490, height=2, bg='black').place(x=610,y=510)
        
        def toggle_password():
            if show_var.get():  
                password_entry.config(show="")  
            else:
                password_entry.config(show="*")  
                
        show_var = tk.BooleanVar()
        show_password_cb = tk.Checkbutton(
            reg_frame,
            text="Show Password",
            variable=show_var,
            command=toggle_password,
            bg="white",
            font=("Arial", 12)
        )

        show_password_cb.place(x=70, y=340)
        
        
        def save_new_admin():
            username = username_entry.get()
            password = password_entry.get()
            success, message = simpan_admin(username, password)
            if success:
                messagebox.showinfo("Sukses", message)
                self.halaman_login()
            else:
                messagebox.showerror("Error", message)

        tk.Button(reg_frame, text="Register", relief='flat', command=save_new_admin, width=40, height=2, bg='#51d451', fg='White', font=("Arial", 14, "bold")).place(x=75, y=400)
        tk.Button(reg_frame, text="Kembali",relief='flat', command=self.halaman_login, width=20, height=1, bg='#f94449', fg='White', font=("Arial", 14, "bold")).place(x=195, y= 550)

    def halaman_profil(self, background_image_path=None):

        for widget in self.root.winfo_children():
            widget.destroy()

        # Tambahkan gambar latar belakang
        try:
            if background_image_path:
                bg_image = Image.open(background_image_path).resize((1920, 1080))
            else:
                bg_image = Image.open("Profil_BG.png").resize((1920, 1080))  # Default
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="white")
            bg_label.place(relwidth=1, relheight=1)
            print("DEBUG: Gambar latar belakang tidak ditemukan!")

        # Ambil data pengguna yang sedang login
        user_data = get_user_data(self.data, self.current_user)
        print(f"DEBUG: User Data - {user_data}")

        # Ambil kos milik pengguna (owner)
        kos_list = [kos for kos in self.data['kos'] if kos.get('owner') == self.current_user]
        print(f"DEBUG: Kos List for {self.current_user} - {kos_list}")

        if not kos_list:
            kos_list = []  # Pastikan kosong untuk pengolahan berikutnya

        # Frame untuk data diri
        frame_data_diri = tk.Frame(self.root, bg="white", bd=5, relief="ridge")
        frame_data_diri.place(relx=0.05, rely=0.05, relwidth=0.4, relheight=0.4)

        tk.Label(frame_data_diri, text="Data Diri", bg="white", font=("Arial", 14, "bold")).pack(pady=10)

        data_diri = user_data.get('data_diri', {})
        if not data_diri:
            tk.Label(frame_data_diri, text="Belum ada data diri.", bg="white", font=("Arial", 12)).pack(anchor='w', padx=10)
        else:
            tk.Label(frame_data_diri, text=f"Nama: {data_diri.get('nama', 'Belum diisi')}", bg="white", font=("Arial", 12)).pack(anchor='w', padx=10)
            tk.Label(frame_data_diri, text=f"Alamat: {data_diri.get('alamat', 'Belum diisi')}", bg="white", font=("Arial", 12)).pack(anchor='w', padx=10)
            tk.Label(frame_data_diri, text=f"Kontak: {data_diri.get('kontak', 'Belum diisi')}", bg="white", font=("Arial", 12)).pack(anchor='w', padx=10)

        tk.Button(frame_data_diri, text="Tambah/Ubah Data Diri", command=self.halaman_tambah_data_diri, bg="blue", fg="white", font=("Arial", 12)).pack(pady=10)

        # Frame untuk daftar kos
        frame_list = tk.Frame(self.root, bg="white", bd=10)
        frame_list.place(relx=0.05, rely=0.5, relwidth=0.4, relheight=0.4)

        tk.Label(frame_list, text="Daftar Kos", bg="white", font=("Arial", 16, "bold")).pack(pady=10)

        tree = ttk.Treeview(frame_list, columns=('ID', 'Nama Kos'), show='headings')
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

        tree.heading('ID', text='ID')
        tree.heading('Nama Kos', text='Nama Kos')
        tree.column('ID', width=50, anchor='center')
        tree.column('Nama Kos', width=200, anchor='center')

        for kos in kos_list:
            tree.insert('', tk.END, values=(kos.get('id', 'N/A'), kos.get('nama_kos', 'N/A')))

        frame_detail = tk.Frame(self.root, bg="white", bd=10)
        frame_detail.place(relx=0.5, rely=0.05, relwidth=0.4, relheight=0.4)

        tk.Label(frame_detail, text="Detail Kos", bg="white", font=("Arial", 16, "bold")).pack(pady=10)

        detail_label = tk.Label(frame_detail, bg="white", justify="left", anchor="nw", font=("Arial", 12), relief="sunken", width=40, height=10)
        detail_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        frame_gambar = tk.Frame(self.root, bg="white", bd=10)
        frame_gambar.place(relx=0.5, rely=0.5, relwidth=0.4, relheight=0.4)

        tk.Label(frame_gambar, text="Gambar Kos", bg="white", font=("Arial", 16, "bold")).pack(pady=10)

        gambar_label = tk.Label(frame_gambar, bg="lightgrey", relief="sunken", width=40, height=10)
        gambar_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        def update_detail(event):
            selected_item = tree.selection()
            if selected_item:
                selected_kos = tree.item(selected_item)['values'][0]
                kos = next((k for k in kos_list if str(k['id']) == str(selected_kos)), None)
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

                    if kos.get('gambar') and os.path.isfile(kos['gambar']):
                        try:
                            img = Image.open(kos['gambar'])
                            img.thumbnail((300, 300))
                            img_tk = ImageTk.PhotoImage(img)
                            gambar_label.config(image=img_tk, text="", compound='top')
                            gambar_label.image = img_tk
                        except FileNotFoundError:
                            gambar_label.config(image="", text="Gambar tidak ditemukan", compound='none')
                    else:
                        gambar_label.config(image="", text="Tidak ada gambar", compound='none')

        tree.bind('<<TreeviewSelect>>', update_detail)

        tk.Button(self.root, text="Kembali", command=self.menu_utama, font=("Arial", 14), bg="red", fg="white").place(relx=0.9, rely=0.9, anchor="center")
        tk.Button(self.root, text="Tambah Kos", command=self.input_kos, font=("Arial", 14), bg="green", fg="white").place(relx=0.7, rely=0.9, anchor="center")
    
    def halaman_tambah_data_diri(self):
            # Hapus semua widget
            for widget in self.root.winfo_children():
                widget.destroy()

            # Ambil data pengguna yang sedang login
            user_data = get_user_data(self.data, self.current_user)
            data_diri = user_data.get('data_diri', {})

            # Frame utama
            data_diri_frame = tk.Frame(self.root, bg="white", bd=10)
            data_diri_frame.place(relx=0.5, rely=0.5, anchor='center', width=900, height=600)

            tk.Label(data_diri_frame, text="Input atau Perbarui Data Diri", bg="white", font=("Arial", 20, "bold")).pack(pady=20)

            tk.Label(data_diri_frame, text="Nama:", bg="white", font=("Arial", 12)).pack(anchor='w', padx=20)
            nama_entry = tk.Entry(data_diri_frame, font=("Arial", 12))
            nama_entry.insert(0, data_diri.get('nama', ''))
            nama_entry.pack(anchor='w', padx=20)

            tk.Label(data_diri_frame, text="Alamat:", bg="white", font=("Arial", 12)).pack(anchor='w', padx=20)
            alamat_entry = tk.Entry(data_diri_frame, font=("Arial", 12))
            alamat_entry.insert(0, data_diri.get('alamat', ''))
            alamat_entry.pack(anchor='w', padx=20)

            tk.Label(data_diri_frame, text="Kontak:", bg="white", font=("Arial", 12)).pack(anchor='w', padx=20)
            kontak_entry = tk.Entry(data_diri_frame, font=("Arial", 12))
            kontak_entry.insert(0, data_diri.get('kontak', ''))
            kontak_entry.pack(anchor='w', padx=20)

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

            tk.Button(data_diri_frame, text="Simpan", command=simpan_data_diri, bg="green", fg="white", font=("Arial", 12)).pack(pady=20)

            tk.Button(data_diri_frame, text="Kembali", command=self.halaman_profil, bg="red", fg="white", font=("Arial", 12)).pack(pady=10)

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
        
        for widget in self.root.winfo_children():
            widget.destroy()

        # Tambahkan gambar latar belakang
        try:
            bg_image = Image.open("Bg_input_kos.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            messagebox.showerror("Error", "Gambar latar belakang tidak ditemukan!")
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)

        # Frame untuk input kos
        input_frame = tk.Frame(self.root, bg="white", bd=20)
        input_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.6, relheight=0.8)

        # Header
        tk.Label(input_frame, text="Input Data Kos", bg="white", font=('Arial', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)

        # Input nama kos
        tk.Label(input_frame, text="Nama Kos:", bg="white", font=('Arial', 14)).grid(row=1, column=0, sticky='w', pady=10, padx=20)
        nama_kos = tk.Entry(input_frame, width=40, font=('Arial', 14))
        nama_kos.grid(row=1, column=1, pady=10, padx=20)

        # Input alamat
        tk.Label(input_frame, text="Alamat:", bg="white", font=('Arial', 14)).grid(row=2, column=0, sticky='w', pady=10, padx=20)
        alamat = tk.Entry(input_frame, width=40, font=('Arial', 14))
        alamat.grid(row=2, column=1, pady=10, padx=20)

        # Input harga per bulan
        tk.Label(input_frame, text="Harga per Bulan:", bg="white", font=('Arial', 14)).grid(row=3, column=0, sticky='w', pady=10, padx=20)
        harga = tk.Entry(input_frame, width=40, font=('Arial', 14))
        harga.grid(row=3, column=1, pady=10, padx=20)

        # Input fasilitas
        tk.Label(input_frame, text="Fasilitas:", bg="white", font=('Arial', 14)).grid(row=4, column=0, sticky='w', pady=10, padx=20)
        fasilitas = tk.Entry(input_frame, width=40, font=('Arial', 14))
        fasilitas.grid(row=4, column=1, pady=10, padx=20)

        # Input nomor rekening
        tk.Label(input_frame, text="Nomor Rekening:", bg="white", font=('Arial', 14)).grid(row=5, column=0, sticky='w', pady=10, padx=20)
        rekening = tk.Entry(input_frame, width=40, font=('Arial', 14))
        rekening.grid(row=5, column=1, pady=10, padx=20)

        # Input luas tempat
        tk.Label(input_frame, text="Luas Tempat (m²):", bg="white", font=('Arial', 14)).grid(row=6, column=0, sticky='w', pady=10, padx=20)
        luas_tempat = tk.Entry(input_frame, width=40, font=('Arial', 14))
        luas_tempat.grid(row=6, column=1, pady=10, padx=20)

        # Input catatan
        tk.Label(input_frame, text="Catatan:", bg="white", font=('Arial', 14)).grid(row=7, column=0, sticky='w', pady=10, padx=20)
        catatan = tk.Entry(input_frame, width=40, font=('Arial', 14))
        catatan.grid(row=7, column=1, pady=10, padx=20)

        # Input gambar kos
        tk.Label(input_frame, text="Gambar Kos:", bg="white", font=('Arial', 14)).grid(row=8, column=0, sticky='w', pady=10, padx=20)
        gambar_label = tk.Label(input_frame, text="Belum ada gambar", bg="lightgrey", font=('Arial', 12), relief="sunken", width=40)
        gambar_label.grid(row=8, column=1, pady=10, padx=20)

        def pilih_gambar():
            gambar_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            if gambar_path:
                gambar_label.config(text=gambar_path)

        tk.Button(input_frame, text="Pilih Gambar", command=pilih_gambar, font=('Arial', 12)).grid(row=9, column=1, sticky='w', pady=10, padx=20)

        # Fungsi untuk menyimpan data kos
        def simpan_data_kos():
            
            try:
                harga_value = int(harga.get())
                luas_value = float(luas_tempat.get())
                if harga_value <= 0 or luas_value <= 0:
                    messagebox.showwarning("Peringatan", "Harga dan luas tempat harus angka positif!")
                    return
            except ValueError:
                messagebox.showwarning("Peringatan", "Harga dan luas tempat harus berupa angka!")
                return

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
                'owner': self.current_user  # Tambahkan username pemilik
            }

            is_valid, message = validasi_input(kos_data)
            if not is_valid:
                messagebox.showwarning("Peringatan", message)
                return

            self.data = tambah_kos(self.data, kos_data)
            save_data(self.data_file, self.data)
            messagebox.showinfo("Sukses", "Data kos berhasil disimpan!")
            self.halaman_profil()  # Kembali ke halaman profil

        tk.Button(input_frame, text="Simpan", command=simpan_data_kos, font=('Arial', 14), bg='#51d451', fg='white').grid(row=10, column=0, columnspan=2, pady=15)
        tk.Button(input_frame, text="Kembali", command=self.menu_utama, font=('Arial', 14), bg='#f94449', fg='white').grid(row=11, column=0, columnspan=2, pady=10)
               
    def list_kos(self):
    
        for widget in self.root.winfo_children():
            widget.destroy()

        # Gambar latar belakang
        try:
            bg_image = Image.open("Bg_list_kos.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)
            messagebox.showwarning("Peringatan", "Gambar latar belakang tidak ditemukan!")

        # Frame untuk filter harga
        filter_frame = tk.Frame(self.root, bg="white", bd=10)
        filter_frame.place(relx=0.5, rely=0.1, anchor='center', relwidth=0.8, relheight=0.15)

        tk.Label(filter_frame, text="Filter Kos Berdasarkan Harga", bg="white", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=4, pady=5)

        tk.Label(filter_frame, text="Harga Minimum:", bg="white", font=("Arial", 14)).grid(row=1, column=0, sticky='e', padx=5)
        min_price_entry = tk.Entry(filter_frame, width=20, font=("Arial", 14))
        min_price_entry.grid(row=1, column=1, padx=5)

        tk.Label(filter_frame, text="Harga Maksimum:", bg="white", font=("Arial", 14)).grid(row=1, column=2, sticky='e', padx=5)
        max_price_entry = tk.Entry(filter_frame, width=20, font=("Arial", 14))
        max_price_entry.grid(row=1, column=3, padx=5)

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
                return

            update_list(filtered_kos)

        tk.Button(filter_frame, text="Terapkan Filter", command=filter_kos, bg="#51d451", fg="white", font=("Arial", 14, "bold")).grid(row=2, column=1, columnspan=1, pady=5)

        # Tambahkan tombol rekomendasi
        def rekomendasi_kos():
            try:
                min_price = int(min_price_entry.get()) if min_price_entry.get().isdigit() else 0
                max_price = int(max_price_entry.get()) if max_price_entry.get().isdigit() else float('inf')
            except ValueError:
                messagebox.showerror("Error", "Harga harus berupa angka!")
                return

            recommended_kos = [kos for kos in self.data['kos'] if min_price <= int(kos['harga']) <= max_price]
            if not recommended_kos:
                messagebox.showinfo("Info", "Tidak ada kos yang sesuai untuk rekomendasi.")
                return

            update_list(recommended_kos)

        tk.Button(filter_frame, text="Rekomendasi", command=rekomendasi_kos, bg="#187bcd", fg="white", font=("Arial", 14, "bold")).grid(row=2, column=2, columnspan=1, pady=5)
        
        # Frame untuk ID Kos
        id_frame = tk.Frame(self.root, bg="white", bd=10)
        id_frame.place(relx=0.1, rely=0.5, anchor='w', relwidth=0.2, relheight=0.6)
        tk.Label(id_frame, text="ID Kos", bg="white", font=('Arial', 16, 'bold')).pack(pady=10)

        id_tree = ttk.Treeview(id_frame, columns=('ID'), show='headings', height=20)
        id_tree.pack(fill=tk.BOTH, expand=True, pady=10)
        id_tree.heading('ID', text='ID')
        id_tree.column('ID', anchor='center', width=100)

        # Frame untuk Detail Kos
        detail_frame = tk.Frame(self.root, bg="white", bd=10)
        detail_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.4, relheight=0.6)
        tk.Label(detail_frame, text="Detail Kos", bg="white", font=('Arial', 16, 'bold')).pack(pady=10)

        detail_text_label = tk.Label(detail_frame, text="", bg="white", justify="left", anchor="nw", relief="sunken", font=("Arial", 14), width=40, height=15)
        detail_text_label.pack(fill=tk.BOTH, expand=True, pady=10)

        # Frame untuk Gambar Kos
        gambar_frame = tk.Frame(self.root, bg="white", bd=10)
        gambar_frame.place(relx=0.9, rely=0.5, anchor='e', relwidth=0.2, relheight=0.6)
        tk.Label(gambar_frame, text="Gambar Kos", bg="white", font=('Arial', 16, 'bold')).pack(pady=10)

        gambar_label = tk.Label(gambar_frame, bg="lightgrey", relief="sunken", width=30, height=15)
        gambar_label.pack(fill=tk.BOTH, expand=True, pady=10)

        def update_list(kos_list):
            for item in id_tree.get_children():
                id_tree.delete(item)
            for kos in kos_list:
                id_tree.insert('', tk.END, values=(kos.get('id', 'N/A')))

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
                    detail_text_label.config(text=detail_text)

                    if kos.get('gambar'):
                        try:
                            img = Image.open(kos['gambar'])
                            img.thumbnail((300, 300))
                            img_tk = ImageTk.PhotoImage(img)
                            gambar_label.config(image=img_tk, text="", compound='top')
                            gambar_label.image = img_tk
                        except FileNotFoundError:
                            gambar_label.config(image="", text="Gambar tidak ditemukan", compound='none')
                    else:
                        gambar_label.config(image="", text="Tidak ada gambar", compound='none')

        id_tree.bind('<<TreeviewSelect>>', update_detail)

        update_list(self.data['kos'])

        tk.Button(self.root, text="Kembali", command=self.main_menu, font=("Arial", 14, "bold"), bg='#f94449', fg='white', relief='flat').place(relx=0.5, rely=0.9, anchor='center')
        
    def pesan_kos(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

        # Tambahkan latar belakang
        try:
            bg_image = Image.open("Pesan_Kos_BG.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)
            messagebox.showwarning("Peringatan", "Gambar latar belakang tidak ditemukan!")

        # Frame utama
        pesan_frame = tk.Frame(self.root, bg="white", bd=10)
        pesan_frame.place(relx=0.5, rely=0.5, anchor='center', width=900, height=600)

        # Judul
        tk.Label(pesan_frame, text="Pemesanan Kos", bg="white", font=('Arial', 20, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)

        # Kos yang tersedia
        available_kos = [k for k in self.data['kos'] if k['status'] == 'Tersedia']
        if not available_kos:
            messagebox.showinfo("Info", "Tidak ada kos yang tersedia untuk dipesan.")
            self.menu_utama()
            return

        kos_options = {f"{k['id']} - {k['nama_kos']}": k for k in available_kos}

        # Input Pilih Kos
        tk.Label(pesan_frame, text="Pilih Kos:", bg="white", font=("Arial", 14)).grid(row=1, column=0, sticky="w", padx=20, pady=10)
        kos_var = tk.StringVar(pesan_frame)
        kos_combobox = ttk.Combobox(pesan_frame, textvariable=kos_var, values=list(kos_options.keys()), width=40, font=("Arial", 12))
        kos_combobox.grid(row=1, column=1, sticky="w", padx=20, pady=10)

        # Nomor Rekening
        tk.Label(pesan_frame, text="Nomor Rekening Tujuan:", bg="white", font=("Arial", 14)).grid(row=2, column=0, sticky="w", padx=20, pady=10)
        rekening_var = tk.StringVar(pesan_frame)
        rekening_label = tk.Label(pesan_frame, textvariable=rekening_var, bg="lightgrey", font=("Arial", 12), width=30, anchor="w")
        rekening_label.grid(row=2, column=1, sticky="w", padx=20, pady=10)

        def update_rekening(*args):
            selected_kos = kos_var.get()
            if selected_kos in kos_options:
                rekening_var.set(kos_options[selected_kos]['rekening'])
            else:
                rekening_var.set("")

        kos_var.trace("w", update_rekening)

        # Input Durasi Sewa
        tk.Label(pesan_frame, text="Durasi Sewa (bulan):", bg="white", font=("Arial", 14)).grid(row=3, column=0, sticky="w", padx=20, pady=10)
        durasi_entry = tk.Entry(pesan_frame, width=10, font=("Arial", 12))
        durasi_entry.grid(row=3, column=1, sticky="w", padx=20, pady=10)

        # Total Harga
        tk.Label(pesan_frame, text="Total Harga:", bg="white", font=("Arial", 14)).grid(row=4, column=0, sticky="w", padx=20, pady=10)
        total_harga_var = tk.StringVar(pesan_frame)
        total_harga_label = tk.Label(pesan_frame, textvariable=total_harga_var, bg="lightgrey", font=("Arial", 12), width=30, anchor="w")
        total_harga_label.grid(row=4, column=1, sticky="w", padx=20, pady=10)

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
        tk.Label(pesan_frame, text="Nominal Pembayaran:", bg="white", font=("Arial", 14)).grid(row=5, column=0, sticky="w", padx=20, pady=10)
        nominal_entry = tk.Entry(pesan_frame, width=30, font=("Arial", 12))
        nominal_entry.grid(row=5, column=1, sticky="w", padx=20, pady=10)

        # Upload Bukti Pembayaran
        tk.Label(pesan_frame, text="Upload Bukti Pembayaran:", bg="white", font=("Arial", 14)).grid(row=6, column=0, sticky="w", padx=20, pady=10)
        upload_label = tk.Label(pesan_frame, text="Belum ada file", bg="lightgrey", font=("Arial", 12), width=30, anchor="w")
        upload_label.grid(row=6, column=1, sticky="w", padx=20, pady=10)

        def upload_file():
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            if file_path:
                upload_label.config(text=file_path)

        tk.Button(pesan_frame, text="Pilih File", relief='flat',command=upload_file, width=30,font=("Arial", 12), bg="#187bcd", fg="white").grid(row=7, column=1, sticky="w", padx=20, pady=10)

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

            if nominal < total_harga:
                messagebox.showwarning("Peringatan", f"Nominal pembayaran harus sama dengan total harga yaitu {total_harga}!")
                return

            if "Belum ada file" in upload_label.cget("text"):
                messagebox.showwarning("Peringatan", "Unggah bukti pembayaran terlebih dahulu!")
                return

            kos_data['status'] = 'Tidak Tersedia'
            pemesanan_data = {
                'id': len(self.data['pemesanan']) + 1,
                'kos_id': kos_data['id'],
                'durasi': durasi,
                'total_harga': total_harga,
                'nominal': nominal,
                'rekening': kos_data['rekening'],
                'bukti_pembayaran': upload_label.cget("text")
            }
            self.data['pemesanan'].append(pemesanan_data)
            save_data(self.data_file, self.data)
            messagebox.showinfo("Sukses", f"Kos '{kos_data['nama_kos']}' berhasil dipesan!")
            self.menu_utama()

        # Tombol Pesan dan Kembali
        tk.Button(pesan_frame, text="Pesan", command=proses_pesan, font=("Arial", 14), bg="green", fg="white", width=15).grid(row=9, column=0, padx=40, pady=70)
        tk.Button(pesan_frame, text="Kembali", command=self.menu_utama, font=("Arial", 14), bg="red", fg="white", width=15).grid(row=9, column=1, padx=80, pady=20)
                        
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
