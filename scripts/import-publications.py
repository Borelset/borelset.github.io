#!/usr/bin/env python3
"""Import the legacy About page's bibliography into Jekyll data.

Usage: python3 scripts/import-publications.py --output /tmp/legacy-publications.json

This is a migration utility. After migration, edit _data/publications.json
directly. It preserves the source bibliography's wording and dates apart from
display markers for author roles and venue grades. The default source is the
archived docs/legacy-about.html. An explicit output is required so re-importing
the old 47-paper list does not silently overwrite the researched bibliography.
"""

import argparse
from collections import Counter
from hashlib import sha1
from html.parser import HTMLParser
import json
from pathlib import Path
import re


def compact(value):
    return re.sub(r"\s+", " ", value).strip()


def title_key(value):
    return re.sub(r"[^a-z0-9]", "", value.lower())


class BibliographyParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ol_depth = 0
        self.current = None
        self.year = None
        self.records = []
        self.anchor = None
        self.strong = None

    def handle_starttag(self, tag, attrs):
        if tag == "ol":
            self.ol_depth += 1
        elif tag == "li":
            self.current = {
                "text": [], "anchors": [], "strong": [],
                "publication": self.ol_depth > 0,
            }
        elif self.current is not None and tag == "a":
            self.anchor = {"url": dict(attrs).get("href", ""), "text": []}
        elif self.current is not None and tag == "strong":
            self.strong = []

    def handle_data(self, data):
        if self.current is not None:
            self.current["text"].append(data)
            if self.anchor is not None:
                self.anchor["text"].append(data)
            if self.strong is not None:
                self.strong.append(data)

    def handle_endtag(self, tag):
        if tag == "ol":
            self.ol_depth -= 1
        elif tag == "a" and self.anchor is not None:
            self.anchor["text"] = compact("".join(self.anchor["text"]))
            self.current["anchors"].append(self.anchor)
            self.anchor = None
        elif tag == "strong" and self.strong is not None:
            self.current["strong"].append(compact("".join(self.strong)))
            self.strong = None
        elif tag == "li" and self.current is not None:
            record = self.current
            text = compact("".join(record["text"]))
            if record["publication"]:
                if self.year is None:
                    raise ValueError("Publication appears before a year heading")
                match = re.fullmatch(r'(.*?)"(.*?)"(.*)', text)
                if match is None:
                    raise ValueError(f"Cannot separate publication title: {text}")
                authors, title, citation = match.groups()
                title = title.rstrip(", ")
                venues = [s for s in record["strong"] if "CCF-" in s or "HotEdge" in s]
                if len(venues) != 1:
                    raise ValueError(f"Ambiguous venue for {title}: {venues}")
                venue = re.sub(r"\s*['’]\s*\d{2}", "", venues[0].split(",")[0]).strip()
                citation = re.sub(r",\s+CCF-[ABC](?=\))", "", citation.lstrip(", "))
                title_links = [a for a in record["anchors"] if title_key(a["text"]) == title_key(title)]
                url = title_links[0]["url"] if title_links else ""
                self.records.append({
                    "id": f"pub-{self.year}-{sha1(title.encode()).hexdigest()[:10]}",
                    "year": self.year,
                    "title": title,
                    "authors": authors.replace("*", "").rstrip(",. "),
                    "venue": venue,
                    "citation": citation,
                    "url": url,
                    "links": [
                        {"label": "Paper" if a in title_links else a["text"], "url": a["url"]}
                        for a in record["anchors"]
                    ],
                    "bibtex": "",
                })
            elif re.fullmatch(r"20\d{2}", text):
                self.year = int(text)
            self.current = None


def attach_bibtex(records, root):
    lookup = {title_key(record["title"]): record for record in records}
    for path in sorted((root / "bibtex").glob("*.bib")):
        content = path.read_text(encoding="utf-8")
        title = re.search(r"^\s*title\s*=\s*\{(.*?)\}\s*,?\s*$", content, re.M)
        if title is None:
            raise ValueError(f"Cannot parse title in {path}")
        record = lookup.get(title_key(title.group(1)))
        if record is None:
            raise ValueError(f"Unmatched BibTeX resource: {path}")
        record["bibtex"] = content
        record["links"].append({"label": "BibTeX", "url": "/" + path.relative_to(root).as_posix()})


def main():
    root = Path(__file__).resolve().parents[1]
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--source", type=Path, default=root / "docs/legacy-about.html", help="Original legacy About HTML")
    cli.add_argument("--output", required=True, type=Path, help="Explicit destination for the legacy-only export")
    args = cli.parse_args()
    source = args.source.read_text(encoding="utf-8")
    parser = BibliographyParser()
    parser.feed(source)
    records = parser.records
    expected_count = sum(len(re.findall(r"<li(?:\s[^>]*)?>", group)) for group in re.findall(r"<ol>(.*?)</ol>", source, re.S))
    if not records or len(records) != expected_count:
        raise ValueError(f"Expected {expected_count} publications, parsed {len(records)}")
    keys = [title_key(record["title"]) for record in records]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate publication titles")
    attach_bibtex(records, root)
    for record in records:
        for link in record["links"]:
            if link["url"].startswith("/") and not (root / link["url"].lstrip("/")).is_file():
                raise ValueError(f"Missing local resource: {link['url']}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "publications": len(records),
        "years": dict(sorted(Counter(record["year"] for record in records).items(), reverse=True)),
        "bibtex_files": sum(bool(record["bibtex"]) for record in records),
        "output": str(args.output),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
