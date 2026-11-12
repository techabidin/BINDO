import argparse
import sys
import os
import time
import traceback
from pathlib import Path

from . import __version__
from .runtime import kompilasi, jalankan_file
from .translator import terjemahkan


riwayat = []


def tulis(*args, **kwargs):
    print(*args, **kwargs)


def masukan(teks=""):
    return input(teks)


def bersihkan():
    os.system("cls" if os.name == "nt" else "clear")


def bantuan():
    print("""
╔══════════════════════════════════════╗
║          BINDO PROGRAMMING           ║
╚══════════════════════════════════════╝

FUNGSI BAWAAN:

  tulis("Halo")          Menampilkan teks
  masukan("Nama: ")      Meminta input
  bersihkan()            Membersihkan terminal
  bantuan()              Menampilkan bantuan
  keluar()               Keluar dari BINDO

  panjang(data)          Menghitung panjang data
  rentang(1, 10)         Membuat rentang angka
  angka("10")            Mengubah menjadi angka
  teks(100)              Mengubah menjadi teks
  jeda(2)                Memberikan jeda 2 detik
  direktori()            Melihat direktori aktif

PERINTAH TERMINAL:

  bindo                  Mode interaktif
  bindo -i               Mode interaktif
  bindo -c "KODE"        Eksekusi langsung
  bindo --stdin          Membaca kode dari stdin
  bindo jalankan FILE    Menjalankan file
  bindo periksa FILE     Memeriksa sintaks
  bindo terjemahkan FILE Menerjemahkan kode
  bindo info             Informasi BINDO
  bindo --versi          Melihat versi

PERINTAH REPL:

  :help                  Bantuan
  :clear                 Bersihkan terminal
  :history               Riwayat perintah
  :exit                  Keluar
""")


def keluar():
    raise SystemExit


def daftar_file(lokasi="."):
    return [item.name for item in Path(lokasi).iterdir()]


def baca_teks(file):
    return Path(file).read_text(encoding="utf-8")


def simpan_teks(file, isi):
    Path(file).write_text(str(isi), encoding="utf-8")
    return True


def buat_ruang():
    return {
        "__name__": "__console__",
        "__builtins__": __builtins__,
        "tulis": tulis,
        "masukan": masukan,
        "bersihkan": bersihkan,
        "bantuan": bantuan,
        "keluar": keluar,
        "panjang": len,
        "rentang": range,
        "angka": int,
        "teks": str,
        "jeda": time.sleep,
        "direktori": lambda: str(Path.cwd()),
        "daftar_file": daftar_file,
        "baca_teks": baca_teks,
        "simpan_teks": simpan_teks,
    }


def eksekusi(kode, ruang=None, nama="<BINDO>"):
    if ruang is None:
        ruang = buat_ruang()

    hasil = kompilasi(kode, nama)
    exec(hasil, ruang, ruang)


def tampilkan_riwayat():
    if not riwayat:
        print("[BINDO] Belum ada riwayat.")
        return

    print("\nRIWAYAT PERINTAH:")

    for nomor, perintah in enumerate(riwayat, 1):
        print(f"  {nomor}. {perintah}")


def interaktif():
    ruang = buat_ruang()

    print(f"""
╔══════════════════════════════════════╗
║          BINDO INTERACTIVE           ║
║          Versi {__version__:<22}║
╚══════════════════════════════════════╝

Ketik bantuan() atau :help untuk bantuan.
Ketik :exit untuk berhenti.
""")

    while True:
        try:
            baris = input("bindo>>> ").strip()

            if not baris:
                continue

            if baris == ":exit":
                print("[BINDO] Sampai jumpa!")
                break

            if baris == ":help":
                bantuan()
                continue

            if baris == ":clear":
                bersihkan()
                continue

            if baris == ":history":
                tampilkan_riwayat()
                continue

            if baris in ("keluar", "exit", "quit",
                         "keluar()", "exit()", "quit()"):
                print("[BINDO] Sampai jumpa!")
                break

            if baris in ("clear", "cls"):
                bersihkan()
                continue

            riwayat.append(baris)

            mulai = time.perf_counter()
            eksekusi(baris, ruang, "<BINDO-REPL>")
            selesai = time.perf_counter()

        except EOFError:
            print("\n[BINDO] Selesai.")
            break

        except KeyboardInterrupt:
            print("\n[BINDO] Gunakan :exit untuk berhenti.")

        except SystemExit:
            print("[BINDO] Sampai jumpa!")
            break

        except Exception as error:
            print(f"[BINDO ERROR] {error}")


def info():
    print(f"""
╔══════════════════════════════════════╗
║          BINDO PROGRAMMING           ║
╚══════════════════════════════════════╝

Nama         : BINDO
Versi        : {__version__}
Bahasa       : Indonesia
Interpreter  : Python Runtime

FITUR:

  [+] Mode interaktif
  [+] Eksekusi kode langsung
  [+] Menjalankan file
  [+] Pemeriksaan sintaks
  [+] Penerjemah kode
  [+] Fungsi bawaan Indonesia
  [+] Riwayat perintah
  [+] Pembacaan stdin
  [+] Pengukuran waktu
  [+] Manajemen file
  [+] Penanganan error
""")


def main(argv=None):

    parser = argparse.ArgumentParser(
        prog="bindo",
        description="BINDO - Bahasa Pemrograman Indonesia"
    )

    parser.add_argument(
        "--versi", "--version",
        action="version",
        version=f"BINDO {__version__}"
    )

    mode = parser.add_mutually_exclusive_group()

    mode.add_argument(
        "-c", "--kode",
        help="Jalankan kode secara langsung"
    )

    mode.add_argument(
        "--stdin",
        action="store_true",
        help="Jalankan kode dari stdin"
    )

    parser.add_argument(
        "-i", "--interaktif",
        action="store_true",
        help="Masuk mode interaktif"
    )

    parser.add_argument(
        "--ukur",
        action="store_true",
        help="Ukur waktu eksekusi"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Tampilkan traceback lengkap"
    )

    sub = parser.add_subparsers(dest="aksi")

    r = sub.add_parser(
        "jalankan",
        aliases=["run"],
        help="Jalankan file BINDO"
    )
    r.add_argument("file")
    r.add_argument("argumen", nargs=argparse.REMAINDER)
    r.add_argument(
        "--ukur",
        action="store_true",
        default=argparse.SUPPRESS
    )

    c = sub.add_parser(
        "periksa",
        help="Periksa sintaks BINDO"
    )
    c.add_argument("file")

    t = sub.add_parser(
        "terjemahkan",
        aliases=["translate"],
        help="Terjemahkan BINDO ke Python"
    )
    t.add_argument("file")
    t.add_argument("-o", "--keluaran")

    sub.add_parser(
        "interaktif",
        aliases=["repl"],
        help="Buka mode interaktif"
    )

    sub.add_parser(
        "info",
        help="Informasi BINDO"
    )

    args = parser.parse_args(argv)

    try:

        if args.kode is not None:
            mulai = time.perf_counter()
            eksekusi(args.kode)
            selesai = time.perf_counter()

            if args.ukur:
                print(
                    f"\n[BINDO] Waktu: {selesai - mulai:.6f} detik"
                )

            if args.interaktif:
                interaktif()

            return 0

        if args.stdin:
            kode = sys.stdin.read()

            mulai = time.perf_counter()
            eksekusi(kode, nama="<BINDO-STDIN>")
            selesai = time.perf_counter()

            if args.ukur:
                print(
                    f"\n[BINDO] Waktu: {selesai - mulai:.6f} detik"
                )

            return 0

        if args.aksi is None:
            interaktif()
            return 0

        if args.aksi in ("interaktif", "repl"):
            interaktif()
            return 0

        if args.aksi == "info":
            info()
            return 0

        path = Path(args.file).expanduser()

        if not path.is_file():
            print(
                f"[BINDO ERROR] File tidak ditemukan: {path}",
                file=sys.stderr
            )
            return 2

        source = path.read_text(encoding="utf-8")

        if args.aksi == "periksa":
            kompilasi(source, str(path))
            print(f"[BINDO] Sintaks valid: {path}")

        elif args.aksi in ("terjemahkan", "translate"):

            hasil = terjemahkan(source)

            if args.keluaran:
                tujuan = Path(args.keluaran)
                tujuan.parent.mkdir(parents=True, exist_ok=True)
                tujuan.write_text(hasil, encoding="utf-8")
                print(f"[BINDO] Berhasil disimpan: {tujuan}")
            else:
                print(hasil, end="")

        elif args.aksi in ("jalankan", "run"):

            mulai = time.perf_counter()
            jalankan_file(str(path), args.argumen)
            selesai = time.perf_counter()

            if args.ukur:
                print(
                    f"\n[BINDO] Waktu: {selesai - mulai:.6f} detik"
                )

        if args.interaktif:
            interaktif()

        return 0

    except SystemExit:
        raise

    except Exception as error:

        print(
            f"\n[BINDO ERROR] {error}",
            file=sys.stderr
        )

        if args.debug:
            traceback.print_exc()

        return 1


if __name__ == "__main__":
    sys.exit(main())
