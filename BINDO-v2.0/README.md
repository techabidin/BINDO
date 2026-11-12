# BINDO v2.0 — Bahasa Pemrograman Indonesia
BINDO adalah proyek bahasa pemrograman dengan sintaks berbahasa Indonesia yang dikembangkan oleh `Abidin.`

BINDO dirancang untuk memudahkan pengguna menulis kode menggunakan istilah Bahasa Indonesia dan menjalankan program melalui runtime Python.

## Kebutuhan
- Python 3.10 atau lebih baru
- Kali Linux, Debian, Ubuntu, Arch Linux, Windows, atau macOS
- Tidak ada dependensi runtime pihak ketiga

## Instalasi lokal di Kali Linux
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```
Ekstrak ZIP, masuk ke folder proyek, lalu:
```bash
cd BINDO-v2.0
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```
Instalasi ini berada di virtual environment, tidak mengubah Python sistem.

## Mulai ngoding
Buat file:
```bash
nano program.bindo
```
Tulis kode:
```python
impor math

kelas Lingkaran:
    fungsi __init__(diri, jari_jari):
        diri.jari_jari = jari_jari

    fungsi luas(diri):
        kembalikan math.pi * diri.jari_jari ** 2

bentuk = Lingkaran(7)
cetak("Luas:", bentuk.luas())
```
Jalankan:
```bash
bindo jalankan program.bindo
```

## Perintah CLI
```bash
bindo --versi
bindo jalankan program.bindo
bindo run program.bindo
bindo periksa program.bindo
bindo terjemahkan program.bindo
bindo terjemahkan program.bindo -o hasil.py
bindo interaktif
```

## Kamus sintaks inti
| BINDO | Python |
|---|---|
| `jika` / `jika_lain` / `selain` | `if` / `elif` / `else` |
| `untuk` / `selama` / `dalam` | `for` / `while` / `in` |
| `dan` / `atau` / `bukan` / `adalah` | `and` / `or` / `not` / `is` |
| `fungsi` / `kembalikan` / `kelas` | `def` / `return` / `class` |
| `coba` / `kecuali` / `akhirnya` | `try` / `except` / `finally` |
| `dengan` / `sebagai` / `naikkan` | `with` / `as` / `raise` |
| `impor` / `dari` | `import` / `from` |
| `cocokkan` / `kasus` | `match` / `case` |
| `Benar` / `Salah` / `Kosong` | `True` / `False` / `None` |
| `cetak` / `masukan` | `print` / `input` |
| `rentang` / `panjang` / `jenis` | `range` / `len` / `type` |
| `teks` / `bilangan` / `desimal` / `logika` | `str` / `int` / `float` / `bool` |
| `daftar` / `kamus` / `himpunan` / `pasangan` | `list` / `dict` / `set` / `tuple` |
| `buka` / `enumerasi` / `gabungkan` | `open` / `enumerate` / `zip` |
| `jumlah` / `minimum` / `maksimum` / `urutkan` | `sum` / `min` / `max` / `sorted` |

## Library Python
```python
impor json
impor math
dari pathlib impor Path
data = {"nama": "BINDO", "aktif": Benar}
cetak(json.dumps(data))
cetak(math.sqrt(81))
cetak(Path(".").resolve())
```
Paket pihak ketiga dipasang di virtual environment yang sama, misalnya `python -m pip install requests`.

## Tes
```bash
python -m unittest discover -s tests -v
```

## Build paket
```bash
python -m pip install build
python -m build
```
Nama distribusi paket adalah `bindo-lang`; nama perintah CLI adalah `bindo`. Publikasi ke PyPI memerlukan akun, pemeriksaan ketersediaan nama, dan pengujian rilis.

## Batasan dan keamanan
- Sintaks Python yang belum diterjemahkan dapat ditulis memakai keyword Python asli; parser Python tetap menjadi penentu grammar.
- Nama yang tercantum di kamus menjadi kata khusus BINDO, sehingga tidak cocok dipakai sebagai nama variabel.
- String, komentar, dan nama atribut setelah titik tidak diterjemahkan.
- REPL saat ini mendukung satu baris per prompt; gunakan file `.bindo` untuk blok multi-baris.
- Error runtime dapat menampilkan istilah Python.
- Program BINDO mempunyai hak akses yang sama dengan proses Python. Jangan jalankan kode dari sumber yang tidak dipercaya.

Lisensi MIT — lihat `LICENSE`.
