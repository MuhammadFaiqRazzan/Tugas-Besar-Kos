import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class KosSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Pemesanan Kos")
        self.root.geometry("800x600")
        
        # Initialize data storage
        self.data_file = 'kos_data.json'
        self.load_data()
        
        # Display main menu
        self.setup_main_menu()
        
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'kos': [],
                'pemesanan': []
            }
            self.save_data()
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)
        
    def setup_main_menu(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Menu frame
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(expand=True)
        
        # Menu buttons
        tk.Button(menu_frame, text="Input Data Kos", command=self.show_input_kos, 
                 width=20, height=2).pack(pady=10)
        tk.Button(menu_frame, text="Lihat Data Kos", command=self.show_list_kos, 
                 width=20, height=2).pack(pady=10)
        tk.Button(menu_frame, text="Pesan Kos", command=self.show_pesan_kos, 
                 width=20, height=2).pack(pady=10)
        tk.Button(menu_frame, text="Lihat Pemesanan", command=self.show_list_pemesanan, 
                 width=20, height=2).pack(pady=10)
        
    def show_input_kos(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=20, pady=20)
        
        # Kos input form
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
        fasilitas = tk.Text(input_frame, width=30, height=4)
        fasilitas.grid(row=4, column=1, pady=5)
        
        def save_kos():
            if not all([nama_kos.get(), alamat.get(), harga.get()]):
                messagebox.showwarning("Peringatan", "Harap isi semua field!")
                return
                
            try:
                new_kos = {
                    'id': len(self.data['kos']) + 1,
                    'nama_kos': nama_kos.get(),
                    'alamat': alamat.get(),
                    'harga': int(harga.get()),
                    'fasilitas': fasilitas.get("1.0", tk.END).strip(),
                    'status': 'Tersedia'
                }
                self.data['kos'].append(new_kos)
                self.save_data()
                messagebox.showinfo("Sukses", "Data kos berhasil disimpan!")
                self.setup_main_menu()
            except ValueError:
                messagebox.showerror("Error", "Harga harus berupa angka!")
        
        tk.Button(input_frame, text="Simpan", command=save_kos).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(input_frame, text="Kembali", command=self.setup_main_menu).grid(row=6, column=0, columnspan=2, pady=5)
        
    def show_list_kos(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        list_frame = tk.Frame(self.root)
        list_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        tk.Label(list_frame, text="Daftar Kos", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Treeview for data display
        columns = ('ID', 'Nama Kos', 'Alamat', 'Harga', 'Fasilitas', 'Status')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Display data
        for kos in self.data['kos']:
            tree.insert('', tk.END, values=(
                kos['id'],
                kos['nama_kos'],
                kos['alamat'],
                kos['harga'],
                kos['fasilitas'],
                kos['status']
            ))
            
        tk.Button(list_frame, text="Kembali", command=self.setup_main_menu).pack(pady=10)
        
    def show_pesan_kos(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        pesan_frame = tk.Frame(self.root)
        pesan_frame.pack(padx=20, pady=20)
        
        tk.Label(pesan_frame, text="Pemesanan Kos", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Select kos
        tk.Label(pesan_frame, text="Pilih Kos:").grid(row=1, column=0, sticky='w', pady=5)
        available_kos = [k for k in self.data['kos'] if k['status'] == 'Tersedia']
        kos_options = {k['nama_kos']: k['id'] for k in available_kos}
        kos_var = tk.StringVar(pesan_frame)
        kos_dropdown = ttk.Combobox(pesan_frame, textvariable=kos_var, values=list(kos_options.keys()))
        kos_dropdown.grid(row=1, column=1, pady=5)
        
        # Order form
        tk.Label(pesan_frame, text="Nama Pemesan:").grid(row=2, column=0, sticky='w', pady=5)
        nama_pemesan = tk.Entry(pesan_frame, width=40)
        nama_pemesan.grid(row=2, column=1, pady=5)
        
        tk.Label(pesan_frame, text="No. Telepon:").grid(row=3, column=0, sticky='w', pady=5)
        telepon = tk.Entry(pesan_frame, width=40)
        telepon.grid(row=3, column=1, pady=5)
        
        tk.Label(pesan_frame, text="Tanggal Masuk:").grid(row=4, column=0, sticky='w', pady=5)
        tanggal = tk.Entry(pesan_frame, width=40)
        tanggal.grid(row=4, column=1, pady=5)
        tanggal.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        tk.Label(pesan_frame, text="Durasi (bulan):").grid(row=5, column=0, sticky='w', pady=5)
        durasi = tk.Entry(pesan_frame, width=40)
        durasi.grid(row=5, column=1, pady=5)
        
        tk.Label(pesan_frame, text="Metode Pembayaran:").grid(row=6, column=0, sticky='w', pady=5)
        metode = ttk.Combobox(pesan_frame, values=['Transfer Bank', 'Cash'])
        metode.grid(row=6, column=1, pady=5)
        
        def save_pemesanan():
            if not all([kos_var.get(), nama_pemesan.get(), telepon.get(), durasi.get(), metode.get()]):
                messagebox.showwarning("Peringatan", "Harap isi semua field!")
                return
                
            try:
                kos_id = kos_options[kos_var.get()]
                kos = next(k for k in self.data['kos'] if k['id'] == kos_id)
                total = kos['harga'] * int(durasi.get())
                
                new_pemesanan = {
                    'id': len(self.data['pemesanan']) + 1,
                    'kos_id': kos_id,
                    'nama_pemesan': nama_pemesan.get(),
                    'telepon': telepon.get(),
                    'tanggal_masuk': tanggal.get(),
                    'durasi': int(durasi.get()),
                    'total_harga': total,
                    'metode_pembayaran': metode.get()
                }
                
                self.data['pemesanan'].append(new_pemesanan)
                
                # Update kos status
                kos['status'] = 'Terisi'
                self.save_data()
                
                messagebox.showinfo("Sukses", f"Pemesanan berhasil!\nTotal yang harus dibayar: Rp{total:,}")
                self.setup_main_menu()
            except ValueError:
                messagebox.showerror("Error", "Durasi harus berupa angka!")
        
        tk.Button(pesan_frame, text="Pesan", command=save_pemesanan).grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(pesan_frame, text="Kembali", command=self.setup_main_menu).grid(row=8, column=0, columnspan=2, pady=5)
        
    def show_list_pemesanan(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        list_frame = tk.Frame(self.root)
        list_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        tk.Label(list_frame, text="Daftar Pemesanan", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Treeview for data display
        columns = ('ID', 'Nama Kos', 'Nama Pemesan', 'Telepon', 'Tanggal Masuk', 
                  'Durasi', 'Total Harga', 'Metode Pembayaran')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Display data
        for pemesanan in self.data['pemesanan']:
            kos = next(k for k in self.data['kos'] if k['id'] == pemesanan['kos_id'])
            tree.insert('', tk.END, values=(
                pemesanan['id'],
                kos['nama_kos'],
                pemesanan['nama_pemesan'],
                pemesanan['telepon'],
                pemesanan['tanggal_masuk'],
                pemesanan['durasi'],
                f"Rp{pemesanan['total_harga']:,}",
                pemesanan['metode_pembayaran']
            ))
            
        tk.Button(list_frame, text="Kembali", command=self.setup_main_menu).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = KosSystem(root)
    root.mainloop()