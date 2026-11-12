import argparse
import sys
import traceback
from pathlib import Path
from . import __version__
from .runtime import kompilasi, jalankan_file
from .translator import terjemahkan

def main(argv=None):
    p = argparse.ArgumentParser(prog="bindo", description="BINDO — Bahasa Pemrograman Indonesia")
    p.add_argument("--versi", "--version", action="version", version=f"BINDO {__version__}")
    sub = p.add_subparsers(dest="aksi")
    r = sub.add_parser("jalankan", aliases=["run"], help="Jalankan file .bindo")
    r.add_argument("file"); r.add_argument("argumen", nargs=argparse.REMAINDER)
    c = sub.add_parser("periksa", help="Periksa sintaks"); c.add_argument("file")
    t = sub.add_parser("terjemahkan", aliases=["translate"], help="Terjemahkan ke Python")
    t.add_argument("file"); t.add_argument("-o", "--keluaran")
    sub.add_parser("interaktif", aliases=["repl"], help="Mode interaktif")
    a = p.parse_args(argv)
    if a.aksi is None: p.print_help(); return 0
    if a.aksi in ("interaktif", "repl"):
        print(f"BINDO {__version__} — ketik keluar() untuk berhenti")
        ruang = {"__name__": "__console__", "__builtins__": __builtins__}
        while True:
            try:
                baris = input("bindo>>> ")
                if baris.strip() in ("keluar()", "exit()", "quit()"): break
                if baris.strip(): exec(kompilasi(baris, "<BINDO-REPL>"), ruang, ruang)
            except (EOFError, KeyboardInterrupt): print(); break
            except Exception: traceback.print_exc()
        return 0
    path = Path(a.file).expanduser()
    if not path.is_file(): print(f"[BINDO] File tidak ditemukan: {path}", file=sys.stderr); return 2
    try:
        source = path.read_text(encoding="utf-8")
        if a.aksi == "periksa":
            kompilasi(source, str(path)); print(f"[BINDO] Sintaks valid: {path}")
        elif a.aksi in ("terjemahkan", "translate"):
            out = terjemahkan(source)
            if a.keluaran: Path(a.keluaran).write_text(out, encoding="utf-8"); print(f"[BINDO] Disimpan: {a.keluaran}")
            else: print(out, end="")
        elif a.aksi in ("jalankan", "run"):
            jalankan_file(str(path), a.argumen)
        return 0
    except SystemExit: raise
    except Exception: traceback.print_exc(); return 1
