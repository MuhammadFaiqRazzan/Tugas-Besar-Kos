# Tugas Besar Kos #

# Kelompok 14 kelas B

Muhammad Faiq Razzan Fawwaz(I0324054)

Rafa Mawlahanif Mardiansyaf(I0324060)

Muhammad Charits Athaya Ramadhan(I0324086)

# Penjelasan kodingan

Sebuah sistem pemesanan dan penjualan kamar kost. dalam sistem tersebut pemesan ataupun penyedia kamar dapat memberikan tipe-tipe kamar kost beserta harga dan fasilitasnya yang akan dipesan ataupun ditawarkan. Trerdapat 4 pilihan yang diberikan yaitu untuk menginput kos dengan data seperti fasilitas kos, harga perbulan, dan alamat, dan terdapat pilihan user sebagai orang yang menywa kos juga data dari kos yang sudah dimasukan dapat ditampilkan.

# Library
Library yang kami gunakan agar program ini berjalan adalah:
1. tkinter
2. pillow
3. json
4. bcrypt
5. OS

# Fitur Kodingan

Terdapat pilihan yang dapat dipilih oleh user yaitu

- Memasukan Data kos : disini user dapat memasukan data kos yang ingin dimasukan meliputi : nama kos, Harga perbulan, Fasilitas kos

- Menunjukkan data Kos : User dapat melihat data kos yang disediakan dengan kriteria yang sudah di masukan pula pada pilihan mesukan data kos

- Memesan kos : User dapat memilih kos uang tersedia dan dapat memilih cara untuk membayar

- Menampilkan kos yang sudah dipesan : User dapat melihat data kos yang duah di pesan

# Flow Chart
![flowchart1 drawio](https://github.com/user-attachments/assets/32c506fc-9dd4-4f1c-a637-649d14f77f16)

# Flow Chart Baru

![flowchart2 drawio](https://github.com/MuhammadFaiqRazzan/Tugas-Besar-Kos/blob/main/Flowchart%20tubes%20kos.jpg)

# Revisi Flow Chart

![flowchart2 drawio](https://github.com/MuhammadFaiqRazzan/Tugas-Besar-Kos/blob/8b57591c514efacaafccea6ebe1c7334fb4fa599/revisiflowchart.jpg)

Pada flowchart baru terdapat fitu baru yang di tambahakan dimana kita menambahkan fitur untuk melakukan register dan login di bagiana owner dan pemesan dari kos. Dimana data yang di masukan oleh owner dan data yang di pesan oleh pemesan dapat berbeda tergantung dengan account yang login dan melakukan kegiatan menginput data.

# Site Map

![Screenshot 2024-12-08 205001](https://github.com/user-attachments/assets/59b2e58c-cb62-457c-b16b-1c8fa736b6f0)

Penjelasan Site Map
1. Masuk aplikasi
2. Terdapat dua pilihan(Pesan dan Sewakan)
   Jika anda mimilih opsi pesan:
   1. Anda dapat registrasi akun KOSIN khusus pemesan terlebih dahulu dengan membuat username dan password sesuai keingginan anda
   2. Jika anda sudah registrasi atau sudah memiliki akun KOSIN anda dapat login dengan memasukan username dan passwoed anda
   3. Anda dapat milih opsi: Lihat data kos, Pesan kos, dan Lihat data pemesanan
   4. Jika anda memilih opsi lihat data kos anda dapat memfilter harga kos minimum dan maximum yang anda inginkan
   5. Setelah memfilter harga kos akan muncul nama kos dan detail data kos
   6. Ketika anda memilih pesan kos anda dapat memilih kos yang anda akan sewa dan memasukan durasi sewa kos
   7. Setelah anda memilih kos dan durasinya akan muncul harganya, anda dapat nominal yang akan anda akan bayar dan measukan bukti pembayarnnya
   8. Setelahh melakukan langkah 6 dan 7 anda dapat langsung memesan kos
   9. Jika anda memilih opsi lihat data pemesanan, anda dapat melihat data pemesanan anda apakah sudah masuk atau belum

   Jika anda mimilih opsi sewakan:
   1. Anda dapat registrasi akun KOSIN khusus penyedia sewa kos terlebih dahulu dengan membuat username dan password sesuai keingginan anda
   2. Jika anda sudah registrasi atau sudah memiliki akun KOSIN anda dapat login dengan memasukan username dan passwoed anda
   3. Terdapat opsi : tambah/ubah data diri, dan tambah kos
   4. Jika anda memilih opsi tambah/ubah data diri, anda dapat memasukan data diri anda: Nama, alamat, dan kontak yang dapat dihubungi dan menyimpannya
   5. Jika anda memilih opsi tambah kos anda dapat memasukan data kos yang akan anda sewakan dan masukan gambar lalu simpan.




