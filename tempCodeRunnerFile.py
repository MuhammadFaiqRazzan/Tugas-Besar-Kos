        username = username_entry.get()
            password = password_entry.get()
            success, message = simpan_admin(username, password)
            if success:
                messagebox.showinfo("Sukses", message)
                self.halaman_login()
            else:
                messagebox.showerror("Error", message)