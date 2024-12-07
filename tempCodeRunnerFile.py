     if not self.current_user:
            messagebox.showwarning("Peringatan", "Anda harus login terlebih dahulu!")
            self.halaman_login()
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        # Tambahkan latar belakang
        try:
            bg_image = Image.open("BackGround.png").resize((1920, 1080))
            self.bg_image = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            bg_label = tk.Label(self.root, bg="lightgrey")
            bg_label.place(relwidth=1, relheight=1)

        tk.Label(self.root, text="Daftar Pemesanan Anda", font=("Arial", 18, "bold"), bg="white").place(relx=0.5, rely=0.1, anchor="center")

        user_pemesanan = [p for p in self.data['pemesanan'] if 'username' in p and p['username'] == self.current_user]

        tree = ttk.Treeview(self.root, columns=("ID", "Nama Kos", "Durasi", "Total Harga", "Status"), show="headings")
        tree.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.5)

        tree.heading("ID", text="ID")
        tree.heading("Nama Kos", text="Nama Kos")
        tree.heading("Durasi", text="Durasi (bulan)")
        tree.heading("Total Harga", text="Total Harga")
        tree.heading("Status", text="Status")

        tree.column("ID", anchor="center", width=50)
        tree.column("Nama Kos", anchor="w", width=200)
        tree.column("Durasi", anchor="center", width=100)
        tree.column("Total Harga", anchor="center", width=100)
        tree.column("Status", anchor="center", width=100)

        for pemesanan in user_pemesanan:
            kos = next((k for k in self.data['kos'] if k['id'] == pemesanan['kos_id']), None)
            kos_name = kos['nama_kos'] if kos else "Kos Tidak Ditemukan"
            tree.insert('', tk.END, values=(pemesanan['id'], kos_name, pemesanan['durasi'], pemesanan['total_harga'], pemesanan['status']))

        tk.Button(self.root, text="Kembali", command=self.menu_utama, bg="red", fg="white", font=("Arial", 14)).place(relx=0.5, rely=0.9, anchor="center")
