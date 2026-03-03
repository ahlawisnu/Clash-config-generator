📖 Tutorial Install Script di Termux Android

1. Persiapan Termux
- Unduh aplikasi Termux dari F-Droid (disarankan, karena versi Play Store sudah lama tidak diperbarui).
- Setelah terpasang, buka Termux dan jalankan update:
  ```
  pkg update && pkg upgrade
  ```

2. Install Paket Dasar
- Pasang Python dan Git:
- 
  ```
  pkg install python git -y
  ```
- Pastikan versi Python sudah terpasang dengan:
  ```
  python --version
  ```

3. Clone Repository
- Masuk ke direktori kerja Anda, lalu clone repo:
- 
  ```
  git clone https://github.com/ahlawisnu/Clash-config-generator.git
  ```
- Masuk ke folder hasil clone:
  ```
  cd Clash-config-generator
  ```

4. Jalankan Script
- Jalankan script Python:
  ```
  python clash_generator.py
  ```
- Jika script membutuhkan library tambahan, biasanya akan muncul error ModuleNotFoundError. Untuk mengatasinya, install library yang diminta dengan:
  ```
  pip install nama-library
  ```
  (contoh: pip install requests)

5. Konfigurasi Output
- Script ini berfungsi untuk menghasilkan file konfigurasi Clash. Output biasanya berupa file .yaml atau .yml.
- Setelah berhasil dijalankan, Anda bisa membuka file hasilnya dengan editor teks di Termux atau memindahkannya ke folder konfigurasi Clash di Android.

---

Tips Tambahan
- Jika ingin lebih rapi, buat virtual environment:
  ```
  python -m venv venv
  source venv/bin/activate
  ```
- Gunakan pip install -r requirements.txt jika repo menyediakan file requirements.txt.
