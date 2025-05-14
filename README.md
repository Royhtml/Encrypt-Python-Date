# Panduan Penggunaan Encrypt di `encrypy.py`

## 1. Persiapan
Pastikan Anda sudah memiliki file `encrypy.py` di direktori project Anda.

## 2. Instalasi Library (Jika Diperlukan)
Jika `encrypy.py` menggunakan library eksternal (misal: `cryptography`), install terlebih dahulu:
```bash
pip install cryptography
```

## 3. Cara Menggunakan Encrypt

### a. Import dan Inisialisasi
```python
from encrypy import encrypt

# Contoh penggunaan
teks = "Ini adalah data rahasia"
kunci = "passwordku"
hasil_enkripsi = encrypt(teks, kunci)
print(hasil_enkripsi)
```

### b. Penjelasan Parameter
- **teks**: Data yang ingin dienkripsi (string).
- **kunci**: Kata sandi atau kunci enkripsi (string).

### c. Output
Fungsi `encrypt` akan menghasilkan string terenkripsi yang hanya bisa dibuka dengan kunci yang sama.

## 4. Contoh Lengkap
```python
from encrypy import encrypt

data = "Contoh data penting"
key = "kunciku123"
encrypted = encrypt(data, key)
print("Data terenkripsi:", encrypted)
```

## 5. Video Tutorial
Berikut video penjelasan lengkap penggunaan encrypt di `encrypy.py`:

<a href ="https://www.tiktok.com/@royhtml/video/7504045070161677574?is_from_webapp=1&sender_device=pc&web_id=7489705398321759751"><img src ="https://www.mdpi.com/applsci/applsci-13-13071/article_deploy/html/images/applsci-13-13071-g001.png"></a>

> Klik gambar di atas untuk menonton video.

---

**Catatan:**  
Pastikan untuk selalu menjaga kerahasiaan kunci enkripsi Anda.
