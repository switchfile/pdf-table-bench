#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Regression tests for number tokens and cell keys (standard library only): `python3 -I -m unittest discover eval`.
The notation of a number must not decide a match, its signed value must."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mdparse import cell_key, is_number_cell, selfcheck, tokens  # noqa: E402
from score import score_one, table_numbers  # noqa: E402


class NumberTokens(unittest.TestCase):
    def same(self, a: str, b: str, mark: str = ".") -> None:
        self.assertEqual(tokens(a, mark), tokens(b, mark), f"{a!r} vs {b!r}, mark {mark!r}")

    def differ(self, a: str, b: str, mark: str = ".") -> None:
        self.assertNotEqual(tokens(a, mark), tokens(b, mark), f"{a!r} vs {b!r}, mark {mark!r}")

    def test_decimal_point_counts(self):
        self.differ("1.20", "120")
        self.differ("1,20", "120", ",")
        self.differ("£176.84", "£17684")
        self.differ("1,6", "16", ",")

    def test_sign_counts(self):
        self.differ("-1.20", "1.20")
        self.differ("−0.279", "0.279")
        self.differ("total –5", "total 5")

    def test_minus_variants(self):
        for m in ("-", "−", "–"):
            self.same(f"{m}1.20", "-1.20")
            self.same(f"a {m}7 b", "a -7 b")
        self.same("£-1.20", "-£1.20")
        self.same("-£ 1.20", "-1.20 £")

    def test_hyphen_is_not_a_minus(self):
        self.assertEqual(tokens("2019-2020"), ["2019", "2020"])
        self.assertEqual(tokens("2019 – 2020"), tokens("2019 2020"))
        self.assertEqual(tokens("CaCl2 x-5"), ["cacl2", "x", "5"])

    def test_thousands_notation_is_free(self):
        for mark in (".", ","):
            for v in ("1 268 082", "1.268.082", "1,268,082", "1268082", "1 268 082"):
                self.same(v, "1268082", mark)

    def test_decimal_mark_notation_is_free(self):
        for mark in (".", ","):
            self.same("2,1", "2.1", mark)
            self.same("1.20", "1.2", mark)
            self.same("-0,50", "-0.5", mark)
        self.same("1.268,50", "1268.5", ",")
        self.same("1 268,5", "1268,5", ",")
        self.same("1,268.5", "1268.50")

    def test_ambiguous_group_follows_document_mark(self):
        self.same("1.268", "1268", ",")
        self.differ("1.268", "1268", ".")
        self.same("1,268", "1268", ".")
        self.differ("1,268", "1268", ",")

    def test_detached_minus(self):
        self.assertEqual(tokens("| - 0.472 |"), ["-0.472"])
        self.assertEqual(tokens("2019 - 2020"), ["2019", "2020"])
        self.assertEqual(tokens("a - 5"), ["a", "5"])
        self.assertEqual(tokens("£ - £ 122.00 £ -"), ["122"])
        self.assertEqual(tokens("343.00 £ - 45.89"), ["343", "45.89"])
        self.assertEqual(tokens("36 000      33 000"), ["36000", "33000"])

    def test_glued_numbers_stay_one_word(self):
        self.assertEqual(tokens("15,956.23GB742484426"), ["1595623gb742484426"])
        self.assertEqual(tokens("end.5"), ["end", "5"])

    def test_separate_numbers_stay_separate(self):
        self.assertEqual(tokens("2022-03 123,760.00"), ["2022", "03", "123760"])
        self.assertEqual(tokens("31 102,600"), ["31", "102600"])
        self.assertEqual(tokens("92 991,00 €", ","), ["92991"])
        self.assertEqual(len(tokens("201.343 201.343")), 2)
        self.assertEqual(len(tokens("201.343 201.343", ",")), 2)
        self.assertEqual(tokens("8 208 | 597 752"), ["8208", "597752"])

    def test_cell_keys(self):
        self.assertEqual(cell_key("(1.20)"), cell_key("-1.20"))
        self.assertEqual(cell_key("( £1.20 )"), cell_key("-1.20"))
        self.assertEqual(cell_key("- 0.472"), cell_key("−0.472"))
        self.assertEqual(cell_key("£ - 1.20"), cell_key("-1.20"))
        self.assertNotEqual(cell_key("0.472 -"), cell_key("−0.472"))
        self.assertNotEqual(cell_key("1.20"), cell_key("-1.20"))
        self.assertNotEqual(cell_key("1.20"), cell_key("120"))
        self.assertEqual(cell_key("1.268,5", ","), cell_key("1 268,50", ","))
        for c in ("-1.20", "(1.20)", "1 268 082", "2,1", "−7"):
            self.assertTrue(is_number_cell(c), c)
        self.assertFalse(is_number_cell("CaCl2"))

    def test_selfcheck(self):
        selfcheck()


class CellScoring(unittest.TestCase):
    TRUTH = [{"rows": [["Item", "Change", "Count"], ["Alpha", "-1.20", "1 268"], ["Beta", "0.75", "42"]],
              "numeric": [[False, False, False], [False, True, True], [False, True, True]]}]

    def hits(self, pred_rows):
        total, hit, _ = table_numbers(self.TRUTH, [pred_rows])
        return total, hit

    def test_exact_copy(self):
        self.assertEqual(self.hits([["Item", "Change", "Count"], ["Alpha", "-1.20", "1268"], ["Beta", "0.75", "42"]]), (4, 4))

    def test_other_notation_same_value(self):
        self.assertEqual(self.hits([["Item", "Change", "Count"], ["Alpha", "−1.2", "1,268"], ["Beta", "0,75", "42"]]), (4, 4))
        self.assertEqual(self.hits([["Item", "Change", "Count"], ["Alpha", "(1.20)", "1,268"], ["Beta", "0.750", "42"]]), (4, 4))

    def test_lost_sign_or_point_is_a_miss(self):
        self.assertEqual(self.hits([["Item", "Change", "Count"], ["Alpha", "1.20", "1268"], ["Beta", "075", "42"]]), (4, 2))

    def test_mark_by_language_without_decimals(self):
        truth = [{"rows": [["Road", "2019"], ["A1", "49.000"]], "numeric": [[False, False], [False, True]]}]
        self.assertEqual(table_numbers(truth, [[["Road", "2019"], ["A1", "49000"]]], ",")[1], 1)
        self.assertEqual(score_one({"text": "A1 | 49.000", "layer": "A1 49.000", "tables": truth}, "| Road | 2019 |\n|---|---|\n"
                                   "| A1 | 49000 |", "de")["cells_hit"], 1)

    def test_corrupted_number_with_lost_point(self):
        truth = {"text": "Rate 1.20 and 7", "layer": "Rate 1.20 and 7", "tables": []}
        self.assertEqual(score_one(truth, "Rate 1.20 and 7")["nums_false"], 0)
        self.assertEqual(score_one(truth, "Rate 120 and 7")["nums_false"], 1)
        self.assertEqual(score_one(truth, "Rate -1.20 and 7")["nums_false"], 1)


if __name__ == "__main__":
    unittest.main()
