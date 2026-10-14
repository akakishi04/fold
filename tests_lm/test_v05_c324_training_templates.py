"""Synthetic authoring checks for the C324 TRAIN-template selection component."""
import copy
from dataclasses import FrozenInstanceError
import itertools
import unittest

from fold_lm.v05_benchmarks import c324_training_templates as b


def fixture():
    rows = []
    for lang, order, query in itertools.product(("en", "ja"), ((0, 1), (1, 0)), (0, 1)):
        rows.append(dict(id=f"{lang}-{order}-{query}", language=lang, entities=[0, 1],
                         values=[0, 3], permutation=list(order), query=query, target=(48, 51)[query]))

    def record(row, text):
        return dict(source_id=row["id"], target=row["target"],
                    views=dict(normal=text, evidence_blind="masked evidence", query_blind="masked query"))

    original = {str(n): {p: [record(r, f"old/{n}/{p}/{r['id']}") for r in rows]
                        for p in b.OLD_PROFILES} for n in b.LENGTHS}
    # Exact normal C321 pattern semantics, used only as synthetic writer-shaped input.
    patterns = (("uuvu", "uvuu"), ("uuvv", "uvuv"), ("vuvv", "vvuv"))
    interior = {}
    for profile, pair in zip(b.INTERIOR_PROFILES, patterns, strict=True):
        out = []
        for row in rows:
            chars = "ab" if row["language"] == "en" else "\u7532\u4e59"
            names = [s.translate(str.maketrans({"u": chars[0], "v": chars[1]})) for s in pair]
            text = ";".join(names[i] + "=" + str(row["values"][i]) for i in row["permutation"])
            out.append(record(row, text + ";" + names[row["query"]] + "="))
        interior[profile] = out
    return rows, original, interior


class C324TrainingTemplateTests(unittest.TestCase):
    def setUp(self):
        self.rows, self.original, self.interior = fixture()

    def build(self, arm="interior4"):
        return b.build_training_views(self.rows, self.original, self.interior, arm=arm)

    def test_01_original_all_nine_tables_unchanged(self):
        got = self.build("original")
        self.assertEqual(len(got.tables), 9)
        for n, p in got.tables:
            self.assertEqual(got.tables[n, p], tuple(r["views"]["normal"] for r in self.original[str(n)][p]))

    def test_02_candidate_changes_only_length_four(self):
        a, c = self.build("original"), self.build()
        self.assertEqual({k for k in a.tables if a.tables[k] != c.tables[k]}, {(4, p) for p in b.OLD_PROFILES})

    def test_03_profile_slot_mapping_exact(self):
        got = self.build()
        for old, new in zip(b.OLD_PROFILES, b.INTERIOR_PROFILES, strict=True):
            self.assertEqual(got.tables[4, old], tuple(r["views"]["normal"] for r in self.interior[new]))

    def test_04_labels_ids_counts_unchanged(self):
        a, c = self.build("original"), self.build()
        self.assertEqual(a.targets, c.targets)
        self.assertEqual(a.source_ids, c.source_ids)
        self.assertEqual(a.targets, tuple(r["target"] for r in self.rows))
        self.assertTrue(all(len(t) == len(self.rows) for t in c.tables.values()))

    def test_05_inputs_preserved(self):
        before = copy.deepcopy((self.rows, self.original, self.interior))
        self.build()
        self.assertEqual(before, (self.rows, self.original, self.interior))

    def test_06_result_immutable(self):
        got = self.build()
        with self.assertRaises(TypeError):
            got.tables[4, "repeat"] = ()
        with self.assertRaises(FrozenInstanceError):
            got.targets = ()

    def test_07_original_never_reads_interior(self):
        got = b.build_training_views(self.rows, self.original, object(), arm="original")
        self.assertEqual(got.tables, self.build("original").tables)

    def test_08_missing_extra_lengths_rejected(self):
        for keys in (("2", "3"), ("2", "3", "4", "5")):
            with self.subTest(keys=keys), self.assertRaises(ValueError):
                b.build_training_views(self.rows, {k: self.original.get(k, {}) for k in keys}, self.interior, arm="original")

    def test_09_profiles_rejected(self):
        self.original["2"]["HOLDOUT"] = []
        with self.assertRaisesRegex(ValueError, "profile"):
            self.build()

    def test_10_interior_profiles_rejected(self):
        self.interior.pop("balanced")
        with self.assertRaisesRegex(ValueError, "interior profile"):
            self.build()

    def test_11_reordered_records_rejected(self):
        self.interior["balanced"].reverse()
        with self.assertRaisesRegex(ValueError, "source alignment"):
            self.build()

    def test_12_prompt_target_change_rejected(self):
        self.interior["balanced"][0]["target"] = 51
        with self.assertRaisesRegex(ValueError, "target alignment"):
            self.build()

    def test_13_logical_target_change_rejected(self):
        self.rows[0]["target"] = 51
        with self.assertRaisesRegex(ValueError, "target binding"):
            self.build()

    def test_14_duplicate_ids_rejected(self):
        self.rows[1]["id"] = self.rows[0]["id"]
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.build()

    def test_15_masked_views_never_used(self):
        for records in self.interior.values():
            for record in records:
                record["views"]["evidence_blind"] = object()
                record["views"]["query_blind"] = object()
        got = self.build()
        self.assertTrue(all(isinstance(s, str) and "masked" not in s for t in got.tables.values() for s in t))

    def test_16_utf8_fact_order_and_query_preserved(self):
        got = self.build()
        self.assertEqual(got.tables[4, "repeat"][0], "aaba=0;abaa=3;aaba=")
        self.assertEqual(got.tables[4, "repeat"][3], "abaa=3;aaba=0;abaa=")
        text = "\u7532\u7532\u4e59\u7532=0;\u7532\u4e59\u7532\u7532=3;\u7532\u7532\u4e59\u7532="
        self.assertEqual(got.tables[4, "repeat"][4].encode("utf-8"), text.encode("utf-8"))

    def test_17_invalid_arm_and_empty_rows_rejected(self):
        for arm in ("last_only", None, True):
            with self.subTest(arm=arm), self.assertRaises(ValueError):
                self.build(arm)
        with self.assertRaises(ValueError):
            b.build_training_views([], self.original, self.interior, arm="original")

    def test_18_invalid_source_row_fields_rejected(self):
        for key, value in (("query", True), ("entities", [0, 0]), ("values", [0, 0]),
                           ("permutation", [0, 2]), ("target", True), ("language", "xx")):
            rows = copy.deepcopy(self.rows)
            rows[0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                b.build_training_views(rows, self.original, self.interior, arm="original")

    def test_19_missing_or_invalid_normal_rejected(self):
        for value in (None, "", "bad\x00text", "\ud800"):
            interior = copy.deepcopy(self.interior)
            interior["balanced"][0]["views"]["normal"] = value
            with self.subTest(value=repr(value)), self.assertRaises(ValueError):
                b.build_training_views(self.rows, self.original, interior, arm="interior4")

    def test_20_row_count_and_full_split_container_rejected(self):
        self.interior["balanced"].pop()
        with self.assertRaisesRegex(ValueError, "row count"):
            self.build()
        with self.assertRaisesRegex(ValueError, "length inventory"):
            b.build_training_views(self.rows, {"TRAIN": self.original}, None, arm="original")


if __name__ == "__main__":
    unittest.main()
