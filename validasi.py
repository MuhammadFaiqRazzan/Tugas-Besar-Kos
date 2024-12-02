def validasi_input(data):
    if not all(data.values()):
        return False, "Harap isi semua data!"
    
    if not data['harga'].isdigit() or int(data['harga']) <= 0:
        return False, "Harga harus berupa angka positif!"
    
    if not data['rekening'].isdigit():
        return False, "Rekening harus berupa angka!"
    
    return True, 
def tambah_kos(data, kos_data):
    data['kos'].append(kos_data)
    return data

def buat_pesanan(data, data_pesanan):
    kos = next((k for k in data['kos'] if k['id'] == data_pesanan['kos_id']), None)
    if kos and kos['status'] == 'Tersedia':
        kos['status'] = 'Tidak Tersedia'
        data['pemesanan'].append(data_pesanan)
        return data, "Pesanan Berhasil"
    else:
        return data, "Kos tidak Tersedia!"
    
def validasi_pembayaran(nominal, rekening_input, kos_data):
    try:
        nominal = int(nominal)
    except ValueError:
        return False, "Nominal harus berupa angka!"
    
    if rekening_input != kos_data['rekening']:
        return False, "Rekening tujuan tidak sesuai!"
    
    total_harga = int(kos_data['harga'])
    if nominal < total_harga:
        return False, f"Nominal pembayaran kurang! Harus sebesar {total_harga}."
    
    return True, 