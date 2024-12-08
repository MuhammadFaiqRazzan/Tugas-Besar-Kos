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