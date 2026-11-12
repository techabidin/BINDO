import sys
from pathlib import Path
from .translator import terjemahkan

def kompilasi(teks, nama_file="<BINDO>", mode="exec"):
    return compile(terjemahkan(teks), nama_file, mode)

def jalankan(teks, nama_file="<BINDO>", argv=None):
    kode = kompilasi(teks, nama_file)
    ruang = {"__name__": "__main__", "__file__": nama_file, "__package__": None, "__builtins__": __builtins__}
    lama = sys.argv[:]
    try:
        sys.argv = [nama_file] + list(argv or [])
        exec(kode, ruang, ruang)
    finally:
        sys.argv = lama
    return ruang

def jalankan_file(lokasi, argv=None):
    path = Path(lokasi).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"File BINDO tidak ditemukan: {path}")
    return jalankan(path.read_text(encoding="utf-8"), str(path), argv)
