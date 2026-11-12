"""Penerjemah token BINDO ke Python."""
import io
import tokenize

KAMUS = {
"jika":"if", "jika_lain":"elif", "selain":"else", "untuk":"for",
"selama":"while", "dalam":"in", "dan":"and", "atau":"or", "bukan":"not",
"adalah":"is", "fungsi":"def", "kembalikan":"return", "kelas":"class",
"coba":"try", "kecuali":"except", "akhirnya":"finally", "dengan":"with",
"sebagai":"as", "naikkan":"raise", "lulus":"pass", "hentikan":"break",
"lanjutkan":"continue", "hapus":"del", "global":"global", "nonlokal":"nonlocal",
"asinkron":"async", "tunggu":"await", "hasilkan":"yield", "dari":"from",
"impor":"import", "cocokkan":"match", "kasus":"case",
"Benar":"True", "Salah":"False", "Kosong":"None",
"cetak":"print", "masukan":"input", "rentang":"range", "panjang":"len",
"jenis":"type", "teks":"str", "bilangan":"int", "desimal":"float",
"logika":"bool", "daftar":"list", "kamus":"dict", "himpunan":"set",
"pasangan":"tuple", "buka":"open", "enumerasi":"enumerate", "gabungkan":"zip",
"jumlah":"sum", "minimum":"min", "maksimum":"max", "urutkan":"sorted",
"terbalik":"reversed", "mutlak":"abs", "semua":"all", "ada":"any",
"peta":"map", "saring":"filter", "bulatkan":"round", "bantuan":"help",
"objek":"object", "superkelas":"super", "properti":"property",
"statis":"staticmethod", "metode_kelas":"classmethod",
}

def terjemahkan(kode: str) -> str:
    hasil = []
    sebelumnya = None
    try:
        for tok in tokenize.generate_tokens(io.StringIO(kode).readline):
            setelah_titik = sebelumnya is not None and sebelumnya.type == tokenize.OP and sebelumnya.string == "."
            if tok.type == tokenize.NAME and tok.string in KAMUS and not setelah_titik:
                tok = tok._replace(string=KAMUS[tok.string])
            hasil.append(tok)
            if tok.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
                                tokenize.DEDENT, tokenize.COMMENT, tokenize.ENCODING):
                sebelumnya = tok
        return tokenize.untokenize(hasil)
    except (tokenize.TokenError, IndentationError) as exc:
        raise SyntaxError(f"Sintaks BINDO tidak dapat diterjemahkan: {exc}") from exc
