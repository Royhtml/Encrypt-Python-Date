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

[![Tata Cara Penggunaan Encrypt di encrypy.py](https://img.youtube.com/vi/2z0d5b7k5OI/0.jpg)](https://www.youtube.com/watch?v=2z0d5b7k5OI)

> Klik gambar di atas untuk menonton video.

---

**Catatan:**  
Pastikan untuk selalu menjaga kerahasiaan kunci enkripsi Anda.
