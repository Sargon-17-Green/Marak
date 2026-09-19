import unittest

from compiler.normalize.code import normalize_code
from compiler.source.text import SourceText


class SourceMapTests(unittest.TestCase):
    def test_letter_points_include_utf8_byte_offsets(self):
        r = normalize_code(SourceText("א😀ב", "x.md"))
        self.assertEqual(r.text, "אב")
        a = r.source_map.point(0)
        b = r.source_map.point(1)
        self.assertEqual((a.char_offset, a.byte_offset, a.line, a.column), (0, 0, 1, 1))
        self.assertEqual((b.char_offset, b.byte_offset, b.line, b.column), (2, 6, 1, 3))

    def test_span_includes_many_deleted_characters_between_letters(self):
        r = normalize_code(SourceText("א---😀---ב", "x.md"))
        sp = r.source_map.span(0, 2)
        self.assertEqual(sp.start.char_offset, 0)
        self.assertEqual(sp.end.char_offset, len("א---😀---ב"))

    def test_collapsed_space_maps_full_original_run_and_gap(self):
        raw = "אב \t,😀 \n גד"
        r = normalize_code(SourceText(raw, "x.md"))
        self.assertEqual(r.text, "אב גד")
        space = r.source_map.units[2]
        self.assertEqual(space.normalized_char, " ")
        self.assertEqual(raw[space.original.start.char_offset:space.original.end.char_offset], " \t,😀 \n ")

    def test_line_column_after_lf(self):
        r = normalize_code(SourceText("אב\nגד", "x.md"))
        g = r.source_map.units[3]
        self.assertEqual((g.original.start.line, g.original.start.column), (2, 1))

    def test_crlf_counts_once(self):
        r = normalize_code(SourceText("אב\r\nגד", "x.md"))
        g = next(u for u in r.source_map.units if u.normalized_char == "ג")
        self.assertEqual((g.original.start.line, g.original.start.column), (2, 1))

    def test_normalized_eof_points_to_physical_eof_after_transparent_suffix(self):
        raw = "אב!!!😀"
        r = normalize_code(SourceText(raw, "x.md"))
        eof = r.source_map.point(len(r.text))
        self.assertEqual(eof.char_offset, len(raw))
        self.assertEqual(eof.byte_offset, len(raw.encode("utf-8")))
        whole = r.source_map.span(0, len(r.text))
        self.assertEqual(whole.end.char_offset, 2)


if __name__ == "__main__":
    unittest.main()
