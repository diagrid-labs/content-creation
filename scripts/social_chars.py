"""Deterministic character-length counter for social-post variations.

Used by the write-social-post and review-social-post skills.
"""

from __future__ import annotations

import argparse
import json
import re
import sys


LIMITS: dict[str, dict[str, int]] = {
    "X":            {"body":  500},
    "LinkedIn":     {"body":  500},
    "Bluesky":      {"body":  300},
    "Reddit":       {"title": 120, "body": 700},
    "Dapr Discord": {"title": 120, "body": 500},
    "Dev.to":       {"title": 120, "body": 1200},
    "Medium":       {"title": 120, "body": 1200},
}

EXPECTED_VARIATIONS: dict[str, int] = {
    "X": 2, "LinkedIn": 2, "Bluesky": 2, "Reddit": 2, "Dapr Discord": 2, "Dev.to": 1, "Medium": 1,
}

PLATFORM_ORDER: list[str] = ["X", "LinkedIn", "Bluesky", "Reddit", "Dapr Discord", "Dev.to", "Medium"]


def normalize_and_count(text: str) -> int:
    """Return the Unicode code-point length of `text` after normalization.

    Normalization: replace CRLF with LF, then strip leading/trailing whitespace.
    """
    normalized = text.replace("\r\n", "\n").strip()
    return len(normalized)


PLATFORM_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
VARIATION_HEADING_RE = re.compile(r"^###\s+Variation\s+(\d+)\s*$")
TITLE_RE = re.compile(r"^\*\*Title:\*\*\s*(.*)$")
BODY_MARKER = "**Body:**"
CHAR_LINE_RE = re.compile(r"^_(?:Characters|Title characters|Body characters):.*_\s*$")


def parse_social_post(text: str) -> list[dict]:
    """Parse a social-post markdown file into a list of platform dicts.

    Each platform dict has:
      - name: str (e.g. "X", "Dapr Discord")
      - variations: list[dict] with keys "index", "title" (optional), "body"

    Unknown headings, missing sections, and structural problems are not
    raised here — they are surfaced by validate_post() against EXPECTED_VARIATIONS.
    """
    lines = text.replace("\r\n", "\n").split("\n")
    platforms: list[dict] = []
    current_platform: dict | None = None
    current_variation: dict | None = None
    buffer: list[str] = []
    in_body = False  # only meaningful when current_variation has Title/Body markers

    def flush_buffer_into_current() -> None:
        nonlocal buffer
        if current_variation is None:
            buffer = []
            return
        text_block = "\n".join(buffer).strip()
        # Strip the trailing characters-metadata italic line if present.
        cleaned = []
        for ln in text_block.split("\n"):
            if CHAR_LINE_RE.match(ln.strip()):
                continue
            cleaned.append(ln)
        text_block = "\n".join(cleaned).strip()
        if "title" in current_variation and in_body:
            current_variation["body"] = text_block
        elif "title" in current_variation:
            # Buffer collected was content between Title and Body — usually empty.
            pass
        else:
            current_variation["body"] = text_block
        buffer = []

    def close_variation() -> None:
        flush_buffer_into_current()

    def close_platform() -> None:
        nonlocal current_variation, in_body
        if current_variation is not None:
            close_variation()
            current_platform["variations"].append(current_variation)
            current_variation = None
            in_body = False

    for raw in lines:
        line = raw.rstrip()
        m_platform = PLATFORM_HEADING_RE.match(line)
        if m_platform:
            name = m_platform.group(1).strip()
            if name in PLATFORM_ORDER:
                close_platform()
                if current_platform is not None:
                    platforms.append(current_platform)
                current_platform = {"name": name, "variations": []}
                continue
            # Non-platform `## ` headings (none expected): close current platform.
            close_platform()
            if current_platform is not None:
                platforms.append(current_platform)
                current_platform = None
            continue

        if current_platform is None:
            continue

        m_var = VARIATION_HEADING_RE.match(line)
        if m_var:
            close_platform_variation = current_variation is not None
            if close_platform_variation:
                close_variation()
                current_platform["variations"].append(current_variation)
            current_variation = {"index": int(m_var.group(1))}
            in_body = False
            continue

        if current_variation is None:
            # Lines like `**Final link:**` between platform heading and first variation.
            continue

        m_title = TITLE_RE.match(line)
        if m_title:
            current_variation["title"] = m_title.group(1).strip()
            in_body = False
            buffer = []
            continue

        if line.strip() == BODY_MARKER:
            in_body = True
            buffer = []
            continue

        buffer.append(line)

    # End of file: flush.
    if current_platform is not None:
        if current_variation is not None:
            close_variation()
            current_platform["variations"].append(current_variation)
        platforms.append(current_platform)

    return platforms


def validate_post(text: str, source: str) -> dict:
    """Validate a parsed social-post against LIMITS and EXPECTED_VARIATIONS.

    Returns the JSON-serializable report described in the spec.
    """
    parsed = parse_social_post(text)
    found_by_name = {p["name"]: p for p in parsed}

    report_platforms = []
    has_failure = False

    for name in PLATFORM_ORDER:
        limits = LIMITS[name]
        expected_variations = EXPECTED_VARIATIONS[name]
        platform = {"name": name, "structural_errors": [], "variations": []}

        if name not in found_by_name:
            platform["structural_errors"].append("missing platform section")
            has_failure = True
            report_platforms.append(platform)
            continue

        variations = found_by_name[name]["variations"]
        if len(variations) != expected_variations:
            platform["structural_errors"].append(
                f"expected {expected_variations} variation(s), found {len(variations)}"
            )
            has_failure = True

        for v in variations:
            if "title" in limits:
                title_text = v.get("title", "")
                if "title" not in v:
                    platform["structural_errors"].append(
                        f"variation {v['index']} missing **Title:**"
                    )
                    has_failure = True
                count = normalize_and_count(title_text)
                limit = limits["title"]
                over = count > limit
                if over:
                    has_failure = True
                platform["variations"].append({
                    "index": v["index"], "field": "title",
                    "count": count, "limit": limit, "over": over,
                })

            body_text = v.get("body", "")
            if "body" not in v:
                platform["structural_errors"].append(
                    f"variation {v['index']} missing body"
                )
                has_failure = True
            count = normalize_and_count(body_text)
            limit = limits["body"]
            over = count > limit
            if over:
                has_failure = True
            platform["variations"].append({
                "index": v["index"], "field": "body",
                "count": count, "limit": limit, "over": over,
            })

        report_platforms.append(platform)

    return {
        "file": source,
        "verdict": "fail" if has_failure else "pass",
        "platforms": report_platforms,
    }


def cmd_validate(args: argparse.Namespace) -> int:
    from pathlib import Path
    path = Path(args.path)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"error: cannot read {path}: {exc}", file=sys.stderr)
        return 2

    report = validate_post(text, source=str(path))

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        _print_human_report(report)

    return 0 if report["verdict"] == "pass" else 1


def _print_human_report(report: dict) -> None:
    print(f"File: {report['file']}")
    print(f"Verdict: {report['verdict'].upper()}")
    print()
    for p in report["platforms"]:
        print(f"## {p['name']}")
        for err in p["structural_errors"]:
            print(f"  STRUCTURAL: {err}")
        for v in p["variations"]:
            marker = "OVER" if v["over"] else "ok  "
            print(f"  [{marker}] Variation {v['index']} {v['field']}: {v['count']}/{v['limit']}")
        print()


def cmd_count(args: argparse.Namespace) -> int:
    if args.text is not None:
        text = args.text
    else:
        text = sys.stdin.read()
    count = normalize_and_count(text)
    if args.limit is not None:
        print(f"{count}/{args.limit}")
    else:
        print(count)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="social_chars.py")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_count = sub.add_parser("count", help="Count characters in text.")
    p_count.add_argument("--text", help="Text to count. If omitted, reads stdin.")
    p_count.add_argument("--limit", type=int, help="Optional limit. Output becomes N/LIMIT.")
    p_count.set_defaults(func=cmd_count)

    p_validate = sub.add_parser("validate", help="Validate a social-post markdown file.")
    p_validate.add_argument("path", help="Path to the social-post markdown file.")
    p_validate.add_argument("--json", action="store_true", help="Emit JSON report on stdout.")
    p_validate.set_defaults(func=cmd_validate)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        # argparse exits 2 on bad args; preserve that.
        return int(exc.code) if isinstance(exc.code, int) else 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
