import unittest
from scripts.social_chars import normalize_and_count


class NormalizeAndCountTests(unittest.TestCase):
    def test_basic_ascii(self):
        self.assertEqual(normalize_and_count("hello"), 5)

    def test_strips_leading_and_trailing_whitespace(self):
        self.assertEqual(normalize_and_count("  hello  \n"), 5)

    def test_crlf_and_lf_match(self):
        crlf = "line one\r\nline two"
        lf = "line one\nline two"
        self.assertEqual(normalize_and_count(crlf), normalize_and_count(lf))

    def test_single_emoji_is_one_codepoint(self):
        self.assertEqual(normalize_and_count("🚀"), 1)

    def test_zwj_family_is_five_codepoints(self):
        # 👨‍👩‍👧 = man + ZWJ + woman + ZWJ + girl = 5 code points.
        # Documents that we count code points, not grapheme clusters.
        self.assertEqual(normalize_and_count("👨‍👩‍👧"), 5)

    def test_empty_string_is_zero(self):
        self.assertEqual(normalize_and_count(""), 0)
        self.assertEqual(normalize_and_count("   \n\n"), 0)


import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "social_chars.py"


def run(*args, stdin: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        input=stdin,
        capture_output=True,
        text=True,
    )


class CountSubcommandTests(unittest.TestCase):
    def test_count_with_text_flag(self):
        result = run("count", "--text", "hello world")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "11")

    def test_count_from_stdin(self):
        result = run("count", stdin="hello world")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "11")

    def test_count_with_limit_under(self):
        result = run("count", "--limit", "500", "--text", "hello")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "5/500")

    def test_count_with_limit_over(self):
        text = "x" * 600
        result = run("count", "--limit", "500", "--text", text)
        # Over-limit still exits 0 — see plan / spec.
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "600/500")

    def test_count_invalid_args_exits_two(self):
        result = run("count", "--limit", "not-a-number", "--text", "x")
        self.assertEqual(result.returncode, 2)


from scripts.social_chars import parse_social_post

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class ParseSocialPostTests(unittest.TestCase):
    def test_parses_all_platforms(self):
        text = (FIXTURES / "good.md").read_text(encoding="utf-8")
        platforms = parse_social_post(text)
        self.assertEqual(
            [p["name"] for p in platforms],
            ["X", "LinkedIn", "Bluesky", "Reddit", "Dapr Discord", "Dev.to", "Medium"],
        )

    def test_x_has_two_variations_each_with_body_only(self):
        text = (FIXTURES / "good.md").read_text(encoding="utf-8")
        platforms = parse_social_post(text)
        x = next(p for p in platforms if p["name"] == "X")
        self.assertEqual(len(x["variations"]), 2)
        for v in x["variations"]:
            self.assertIn("body", v)
            self.assertNotIn("title", v)
            self.assertTrue(v["body"].startswith("Sample X"))

    def test_reddit_variations_have_title_and_body(self):
        text = (FIXTURES / "good.md").read_text(encoding="utf-8")
        platforms = parse_social_post(text)
        reddit = next(p for p in platforms if p["name"] == "Reddit")
        self.assertEqual(len(reddit["variations"]), 2)
        for v in reddit["variations"]:
            self.assertTrue(v["title"].startswith("Reddit fixture title"))
            self.assertTrue(v["body"].startswith("Reddit body"))

    def test_strips_characters_metadata_line(self):
        text = (FIXTURES / "good.md").read_text(encoding="utf-8")
        platforms = parse_social_post(text)
        x = next(p for p in platforms if p["name"] == "X")
        for v in x["variations"]:
            self.assertNotIn("_Characters:", v["body"])

    def test_devto_has_one_variation(self):
        text = (FIXTURES / "good.md").read_text(encoding="utf-8")
        platforms = parse_social_post(text)
        devto = next(p for p in platforms if p["name"] == "Dev.to")
        self.assertEqual(len(devto["variations"]), 1)

    def test_medium_has_one_variation(self):
        text = (FIXTURES / "good.md").read_text(encoding="utf-8")
        platforms = parse_social_post(text)
        medium = next(p for p in platforms if p["name"] == "Medium")
        self.assertEqual(len(medium["variations"]), 1)


import json

from scripts.social_chars import validate_post


class ValidatePostTests(unittest.TestCase):
    def test_good_fixture_passes(self):
        text = (FIXTURES / "good.md").read_text(encoding="utf-8")
        report = validate_post(text, source="good.md")
        self.assertEqual(report["verdict"], "pass")
        for p in report["platforms"]:
            self.assertEqual(p["structural_errors"], [])
            for v in p["variations"]:
                self.assertFalse(v["over"])

    def test_over_limit_x_fails(self):
        text = (FIXTURES / "over_limit_x.md").read_text(encoding="utf-8")
        report = validate_post(text, source="over_limit_x.md")
        self.assertEqual(report["verdict"], "fail")
        x = next(p for p in report["platforms"] if p["name"] == "X")
        over = [v for v in x["variations"] if v["over"]]
        self.assertEqual(len(over), 1)
        self.assertEqual(over[0]["index"], 2)

    def test_missing_linkedin_is_structural_error(self):
        text = (FIXTURES / "missing_linkedin.md").read_text(encoding="utf-8")
        report = validate_post(text, source="missing_linkedin.md")
        self.assertEqual(report["verdict"], "fail")
        names = [p["name"] for p in report["platforms"]]
        # LinkedIn entry must still appear, with a structural error.
        self.assertIn("LinkedIn", names)
        linkedin = next(p for p in report["platforms"] if p["name"] == "LinkedIn")
        self.assertTrue(any("missing" in e.lower() for e in linkedin["structural_errors"]))

    def test_reddit_with_one_variation_is_structural_error(self):
        text = (FIXTURES / "one_reddit_variation.md").read_text(encoding="utf-8")
        report = validate_post(text, source="one_reddit_variation.md")
        self.assertEqual(report["verdict"], "fail")
        reddit = next(p for p in report["platforms"] if p["name"] == "Reddit")
        self.assertTrue(any("variation" in e.lower() for e in reddit["structural_errors"]))


class ValidateCLITests(unittest.TestCase):
    def test_validate_good_exits_zero(self):
        result = run("validate", str(FIXTURES / "good.md"))
        self.assertEqual(result.returncode, 0)

    def test_validate_over_limit_exits_one(self):
        result = run("validate", str(FIXTURES / "over_limit_x.md"))
        self.assertEqual(result.returncode, 1)

    def test_validate_unreadable_exits_two(self):
        result = run("validate", str(FIXTURES / "does_not_exist.md"))
        self.assertEqual(result.returncode, 2)

    def test_validate_json_schema(self):
        result = run("validate", str(FIXTURES / "good.md"), "--json")
        payload = json.loads(result.stdout)
        self.assertIn("file", payload)
        self.assertIn("verdict", payload)
        self.assertIn("platforms", payload)
        self.assertEqual(payload["verdict"], "pass")
        self.assertTrue(all("name" in p and "variations" in p for p in payload["platforms"]))

    def test_validate_malformed_reports_structural_errors(self):
        result = run("validate", str(FIXTURES / "malformed.md"), "--json")
        # Returncode is 1 (structural blocker), not 2 (parse crash).
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["verdict"], "fail")


if __name__ == "__main__":
    unittest.main()
