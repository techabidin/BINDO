import unittest
from bindo.translator import terjemahkan

class TestBindo(unittest.TestCase):
    def test_keywords(self):
        py = terjemahkan("jika Benar:\n    cetak('ok')\nselain:\n    cetak('no')\n")
        self.assertIn("if True:", py); self.assertIn("else:", py); compile(py, "<test>", "exec")
    def test_string_comment(self):
        py = terjemahkan('# cetak jika Benar\ncetak("jika cetak Benar")\n')
        self.assertIn('# cetak jika Benar', py); self.assertIn('"jika cetak Benar"', py)
    def test_attribute(self):
        self.assertIn("obj.cetak", terjemahkan("obj.cetak = 1\n"))
    def test_oop(self):
        py = terjemahkan("kelas A:\n    fungsi __init__(diri):\n        diri.x = 1\n")
        compile(py, "<test>", "exec")
    def test_match(self):
        compile(terjemahkan("cocokkan x:\n    kasus 1:\n        cetak('satu')\n"), "<test>", "exec")

if __name__ == "__main__": unittest.main()
