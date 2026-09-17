#!/usr/bin/env python3
"""Validate every book against books-vocabulary.json.

Books are written here by the Apps Script behind the Google Form, so no human
reviews the commit before it lands. This runs the same checks the website's
build runs (src/content.config.ts there), but here, where the file arrives —
so a bad entry is caught in this repo instead of breaking the site's build.

    python3 check-books.py
"""

import json
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).parent
VOCAB = json.loads((ROOT / "books-vocabulary.json").read_text(encoding="utf-8"))

values = lambda key: {e["value"] for e in VOCAB[key]}

SCALARS = {"category": "category", "form": "form", "format": "format", "reviewer_role": "reviewer_role"}
LISTS = {"domain": "domain", "use": "use", "appeal": "appeal"}
REQUIRED = ("title", "author", "category", "domain", "form", "review", "reviewer_role")
OPTIONAL_STR = ("isbn", "series", "reviewer_role_other", "reviewed_by", "libby_url")

problems = []


def check(path, data):
    say = lambda msg: problems.append(f"{path.name}: {msg}")

    if not isinstance(data, dict):
        return say("front matter is not a mapping")

    for field in REQUIRED:
        if data.get(field) in (None, "", []):
            say(f"missing {field}")

    for field, key in SCALARS.items():
        v = data.get(field)
        if v is None:
            continue
        if not isinstance(v, str):
            say(f"{field} must be a single value, got {type(v).__name__}")
        elif v not in values(key):
            say(f"{field}: {v!r} is not in books-vocabulary.json")

    for field, key in LISTS.items():
        v = data.get(field)
        if v is None:
            continue
        if not isinstance(v, list):
            say(f"{field} must be a list")
            continue
        for item in v:
            if item not in values(key):
                say(f"{field}: {item!r} is not in books-vocabulary.json")

    if isinstance(data.get("domain"), list) and not data["domain"]:
        say("domain must name at least one subject")

    if data.get("reviewer_role") == "other" and not data.get("reviewer_role_other"):
        say("reviewer_role is 'other' but reviewer_role_other is empty")

    for field in ("title", "author", "review") + OPTIONAL_STR:
        if field in data and data[field] is not None and not isinstance(data[field], str):
            say(f"{field} must be text")

    if "year" in data and data["year"] is not None and not isinstance(data["year"], int):
        say("year must be a number")

    for field in ("draft", "placeholder"):
        if field in data and not isinstance(data[field], bool):
            say(f"{field} must be true or false")

    url = data.get("amazon_url")
    if url:
        if not re.match(r"^https://(www\.)?amazon\.com/", url):
            say("amazon_url must be an amazon.com link")
        tag = VOCAB.get("amazon_tag")
        if tag and f"tag={tag}" not in url:
            say(f"amazon_url must carry CEP's Associates tag ({tag})")


def main():
    files = sorted((ROOT / "books").glob("*.md"))
    if not files:
        print("No book files found in books/.", file=sys.stderr)
        return 1

    for path in files:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            problems.append(f"{path.name}: no front matter")
            continue
        parts = text.split("---", 2)
        try:
            check(path, yaml.safe_load(parts[1]))
        except yaml.YAMLError as err:
            problems.append(f"{path.name}: front matter is not valid YAML - {err}")

    slugs = {}
    for path in files:
        slugs.setdefault(path.stem, []).append(path.name)

    for problem in problems:
        print(problem, file=sys.stderr)

    if problems:
        print(f"\n{len(problems)} problem(s) in {len(files)} books.", file=sys.stderr)
        return 1

    print(f"{len(files)} books, all valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
