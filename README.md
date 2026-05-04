# Multi Auto Clicker Pro

Untuk anda yang ingin mendapatkan aplikasi multi auto clicker, dibuat dengan tujuan untuk memudahkan pekerjaan. Apk ini berjalan di lokal jadi tidak akan membawa apapun yang berbahaya untuk anda, Silahkan mencoba dan see yaa.

Sebuah aplikasi Auto Clicker modern yang memungkinkan Anda untuk merekam dan menjalankan banyak urutan titik klik di layar, dengan dukungan antarmuka grafis yang bersih menggunakan `CustomTkinter`.

## Fitur Utama

- **Multi Click Points**: Tambahkan urutan titik klik sesuai kebutuhan.
- **Pengaturan Lengkap**: Tiap titik klik dapat diatur secara spesifik:
  - Koordinat X dan Y
  - Delay Awal (jeda sebelum klik terjadi)
  - Interval (jeda setelah klik, sebelum berpindah ke titik lain)
  - Jenis Tombol: Kiri, Kanan, Tengah
  - Jenis Klik: Single, Double
- **Pengambilan Koordinat Otomatis**: Tekan tombol `F8` untuk menyimpan posisi kursor saat ini.
- **Sistem Profil**: Simpan konfigurasi klik Anda dan gunakan lagi di masa mendatang. Data disimpan dalam format JSON.
- **Global Hotkey**:
  - `F6` : Start / Stop aplikasi dari mana saja
  - `F7` : Pause / Lanjutkan tanpa harus mereset urutan dari awal
  - `F8` : Ambil titik koordinat
- **Fitur Failsafe**: Jika program berjalan di luar kendali (runaway loop), gerakkan paksa kursor Anda ke salah satu **pojok layar** (kiri atas, kanan atas, kiri bawah, kanan bawah) untuk mematikan klik secara darurat.
- **Tampilan Modern**: Dukungan Dark Mode & Light mode untuk GUI.

## Prasyarat Instalasi

1. Pastikan Anda telah menginstal **Python 3.x**.
2. Buka terminal, masuk ke folder project aplikasi ini (misal: `d:\laragon\www\Apk_Clicker`).
3. Install dependensi dengan menjalankan perintah:
   ```bash
   pip install -r requirements.txt
   ```

## Menjalankan Aplikasi

Jalankan perintah berikut di terminal:
```bash
python main.py
```

## Struktur Project (Arsitektur MVC Modular)

```
Apk_Clicker/
├── core/                  # Berisi logic dasar program
│   ├── click_engine.py    # Logika eksekusi mouse (pynput, failsafe)
│   ├── scheduler.py       # Loop engine pada background thread
│   └── hotkey_manager.py  # Global keyboard listener
├── models/
│   └── profile.py         # Struktur data dataclasses & JSON save/load
├── ui/
│   └── main_window.py     # Frontend menggunakan CustomTkinter
├── utils/
│   └── logger.py          # Sistem pencatatan error dan log
├── profiles/              # (Otomatis dibuat) Penyimpanan konfigurasi .json
├── logs/                  # (Otomatis dibuat) Penyimpanan file log
├── main.py                # Entry point
└── requirements.txt
```

## Bonus / Pengembangan Lebih Lanjut
Jika Anda ingin melakukan build aplikasi menjadi single-file `.exe` untuk didistribusikan ke komputer lain tanpa perlu menginstall Python, Anda dapat menggunakan PyInstaller:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --name "Multi_Auto_Clicker" main.py
```
Aplikasi `.exe` nantinya akan berada di dalam folder `dist`.
