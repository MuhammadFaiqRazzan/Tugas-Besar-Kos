     # Tambahkan gambar latar belakang
        try:
            if background_image_path:
                bg_image = Image.open(background_image_path).resize((1920, 1080))
            else:
                bg_image = Image.open("Profil_BG.png").resize((1920, 1080))  # Default background
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="white")
            bg_label.place(relwidth=1, relheight=1)
            messagebox.showwarning("Peringatan", "Gambar latar belakang tidak ditemukan!")

        # Ambil data pengguna yang sedang login
        user_data = get_user_data(self.data, self.current_user)

        # Jika belum ada data diri, inisialisasi data kosong
        if 'data_diri' not in user_data:
            user_data['data_diri'] = {'nama': '', 'alamat': '', 'kontak': ''}
            self.data = update_user_data(self.data, self.current_user, user_data)
            save_data(self.data_file, self.data)

        # Frame utama
        profil_frame = tk.Frame(self.root, bg="white", bd=10)
        profil_frame.place(relx=0.5, rely=0.5, anchor='center', width=900, height=600)

        # Judul halaman
        tk.Label(profil_frame, text=f"Profil {self.current_user}", bg="white", font=("Arial", 20, "bold")).pack(pady=20)

        # Bagian Data Diri
        tk.Label(profil_frame, text="Data Diri", bg="white", font=("Arial", 14, "bold")).pack(pady=10)
        data_diri = user_data.get('data_diri', {})

        tk.Label(profil_frame, text="Nama:", bg="white", font=("Arial", 12)).pack(anchor='w', padx=20)
        nama_entry = tk.Entry(profil_frame, font=("Arial", 12))
        nama_entry.insert(0, data_diri.get('nama', ''))
        nama_entry.pack(anchor='w', padx=20)

        tk.Label(profil_frame, text="Alamat:", bg="white", font=("Arial", 12)).pack(anchor='w', padx=20)
        alamat_entry = tk.Entry(profil_frame, font=("Arial", 12))
        alamat_entry.insert(0, data_diri.get('alamat', ''))
        alamat_entry.pack(anchor='w', padx=20)

        tk.Label(profil_frame, text="Kontak:", bg="white", font=("Arial", 12)).pack(anchor='w', padx=20)
        kontak_entry = tk.Entry(profil_frame, font=("Arial", 12))
        kontak_entry.insert(0, data_diri.get('kontak', ''))
        kontak_entry.pack(anchor='w', padx=20)

        def simpan_data_diri():
            # Simpan data diri pengguna ke struktur data
            updated_data_diri = {
                'nama': nama_entry.get(),
                'alamat': alamat_entry.get(),
                'kontak': kontak_entry.get()
            }
            user_data['data_diri'] = updated_data_diri
            self.data = update_user_data(self.data, self.current_user, user_data)
            save_data(self.data_file, self.data)
            messagebox.showinfo("Sukses", "Data diri berhasil disimpan!")

        tk.Button(profil_frame, text="Simpan Data Diri", command=simpan_data_diri, bg="green", fg="white", font=("Arial", 12)).pack(pady=10)

        # Bagian Daftar Kos
        tk.Label(profil_frame, text="Daftar Kos", bg="white", font=("Arial", 14, "bold")).pack(pady=10)

        kos_list = get_kos_by_owner(self.data, self.current_user)

        # Debug log untuk memastikan data kos
        print("Debug: Kos list untuk user", self.current_user, kos_list)

        if not kos_list:
            tk.Label(profil_frame, text="Tidak ada kos yang terdaftar.", bg="white", font=("Arial", 12)).pack()
        else:
            tree = ttk.Treeview(profil_frame, columns=('ID', 'Nama', 'Status'), show='headings')
            tree.pack(fill=tk.BOTH, expand=True, pady=10)

            tree.heading('ID', text='ID')
            tree.heading('Nama', text='Nama Kos')
            tree.heading('Status', text='Status')

            for kos in kos_list:
                tree.insert('', tk.END, values=(kos['id'], kos['nama_kos'], kos['status']))

        def tambah_kos():
            self.input_kos()

        # Tambahkan tombol Tambah Kos
        tk.Button(profil_frame, text="Tambah Kos", command=tambah_kos, bg="blue", fg="white", font=("Arial", 12)).pack(pady=10)

        # Tombol kembali
        tk.Button(profil_frame, text="Kembali", command=self.menu_utama, font=("Arial", 14), bg="red", fg="white").pack(pady=10)