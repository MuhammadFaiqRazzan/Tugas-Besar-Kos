def validasi_input(data):
    if not all(data.values()):
        return False, "Harap isi semua Data!"
    return True, ""

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