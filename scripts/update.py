#!/usr/bin/env python3
"""Refresh this repository from the public CSV files served on worldmoneyroadmap.com.

The site regenerates its CSV datasets at every build and serves them at
https://worldmoneyroadmap.com/data/csv/en/<file>.csv, with column metadata in
datasets.json. This script copies the six files that are mirrored here (the
same six as the Hugging Face dataset), checks them, and rewrites the
generated parts of README.md.

Standard library only. Nothing is written unless every check passes.

  python3 scripts/update.py                  # fetch from the live site
  python3 scripts/update.py --from-dir DIR   # use a local build (DIR/<file>.csv, DIR/datasets.json)
  python3 scripts/update.py --check          # validate the files already in data/
"""
import argparse
import csv
import datetime as dt
import io
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
README = os.path.join(ROOT, "README.md")
BASE_URL = "https://worldmoneyroadmap.com/data/csv/en/"
UA = "wmr-market-datasets-mirror/1.0 (+https://github.com/worldmoneyroadmap/wmr-market-datasets)"

# Mirrored files (same set as huggingface.co/datasets/worldmoneyroadmap/wmr-market-datasets).
# Each one is either WMR's own calculation or a public-domain / official public record.
FILES = [
    "fed-rate-history",
    "market-dates",
    "trading-days",
    "us-financials-sec",
    "ai-lab-nav",
    "ai-lab-metrics",
]

PAPER_ACCOUNTS = {"kr", "us", "etf", "fund", "crypto", "futures", "multi"}  # AI-lab paper accounts only
MAX_FILE = 50 * 1024 * 1024   # GitHub warns above 50 MB
MAX_TOTAL = 100 * 1024 * 1024
MAX_SHRINK = 0.30             # refuse an update that drops more than 30% of a file's rows
HANGUL = re.compile("[\u1100-\u11ff\u3130-\u318f\uac00-\ud7a3]")
# Sources that must never appear in this repository (terms do not allow redistribution).
FORBIDDEN = re.compile(r"yahoo\.|naver\.|finra\.org|openapi\.krx|data\.krx\.co\.kr|fred\.stlouisfed\.org|stooq\.", re.I)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        if r.status != 200:
            raise RuntimeError(f"{url}: HTTP {r.status}")
        return r.read()


def load(src_dir, name):
    if src_dir:
        with open(os.path.join(src_dir, name), "rb") as f:
            return f.read()
    return fetch(BASE_URL + name)


def parse_csv(raw, label):
    text = raw.decode("utf-8-sig")  # site files carry a UTF-8 BOM
    rows = list(csv.reader(io.StringIO(text, newline="")))
    if not rows:
        raise ValueError(f"{label}: empty file")
    return text, rows[0], rows[1:]


def count_rows(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return len(parse_csv(f.read(), path)[2])


def check_file(stem, raw, meta):
    label = f"{stem}.csv"
    if len(raw) > MAX_FILE:
        raise ValueError(f"{label}: {len(raw)} bytes is over the 50 MB limit")
    text, header, body = parse_csv(raw, label)
    want = [c["name"] for c in meta.get("columns", [])]
    if want and header != want:
        raise ValueError(f"{label}: header {header} does not match datasets.json {want}")
    if not body:
        raise ValueError(f"{label}: no data rows")
    bad = [i for i, r in enumerate(body, 2) if len(r) != len(header)]
    if bad:
        raise ValueError(f"{label}: rows with the wrong number of fields at lines {bad[:5]}")
    if HANGUL.search(text):
        raise ValueError(f"{label}: Korean text found in the English edition")
    m = FORBIDDEN.search(text)
    if m:
        raise ValueError(f"{label}: forbidden source reference '{m.group(0)}'")
    if "account" in header:
        # Only the AI paper accounts may appear; a real-money or any other account must never be published.
        i = header.index("account")
        extra = sorted({r[i] for r in body} - PAPER_ACCOUNTS)
        if extra:
            raise ValueError(f"{label}: unexpected account codes {extra}")
    if meta.get("rows") is not None and int(meta["rows"]) != len(body):
        raise ValueError(f"{label}: {len(body)} rows but datasets.json says {meta['rows']}")
    old = count_rows(os.path.join(DATA, label))
    if old and len(body) < old * (1 - MAX_SHRINK):
        raise ValueError(f"{label}: rows fell from {old} to {len(body)} (more than {int(MAX_SHRINK*100)}%)")
    return header, body


def md_escape(s):
    return str(s).replace("|", "\\|").replace("\n", " ").strip()


def render_files(metas, sizes):
    out = ["| File | What it contains | Rows | As of | Size | Source |", "|---|---|---:|---|---:|---|"]
    for stem in FILES:
        m = metas[stem]
        src = md_escape(m.get("source", ""))
        if m.get("source_url"):
            src = f"[{src}]({m['source_url']})"
        kb = sizes[stem] / 1024
        size = f"{kb/1024:.1f} MB" if kb >= 1024 else f"{kb:.1f} KB"
        out.append(f"| [`{stem}.csv`](data/{stem}.csv) | {md_escape(m.get('description', ''))} | {int(m['rows']):,} | {m.get('as_of', '')} | {size} | {src} |")
    return "\n".join(out)


def render_schema(metas):
    out = []
    for stem in FILES:
        m = metas[stem]
        out.append(f"### `{stem}.csv`\n")
        fq = md_escape(m.get("update_frequency", ""))
        if fq[1:2].islower():
            fq = fq[0].lower() + fq[1:]
        out.append(f"{md_escape(m.get('title', ''))}. Updated: {fq}.\n")
        out.append("| Column | Description |")
        out.append("|---|---|")
        for c in m.get("columns", []):
            out.append(f"| `{c['name']}` | {md_escape(c.get('description', ''))} |")
        out.append("")
    return "\n".join(out).rstrip()


def replace_block(text, key, body):
    pat = re.compile(rf"(<!-- BEGIN:{key} -->\n)(?:.*?\n)?(<!-- END:{key} -->)", re.S)
    if not pat.search(text):
        raise ValueError(f"README.md: marker {key} not found")
    return pat.sub(lambda m: m.group(1) + body + "\n" + m.group(2), text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-dir", help="read files from a local site build instead of the live site")
    ap.add_argument("--check", action="store_true", help="validate data/ only; write nothing")
    ap.add_argument("--force", action="store_true", help="rewrite README.md even if no data changed")
    a = ap.parse_args()

    src_dir = DATA if a.check else a.from_dir
    meta_raw = load(src_dir, "datasets.json")
    meta_all = json.loads(meta_raw.decode("utf-8-sig"))
    by_file = {d.get("file", "").removesuffix(".csv"): d for d in meta_all.get("datasets", [])}
    missing = [s for s in FILES if s not in by_file]
    if missing:
        raise SystemExit(f"datasets.json lacks: {missing}")

    raws, sizes = {}, {}
    for stem in FILES:
        raw = load(src_dir, f"{stem}.csv")
        check_file(stem, raw, by_file[stem])  # in --check mode the shrink test compares the file with itself
        raws[stem], sizes[stem] = raw, len(raw)
    if sum(sizes.values()) > MAX_TOTAL:
        raise SystemExit("total size over 100 MB")
    if a.check:
        print("check OK:", ", ".join(f"{s} {by_file[s]['rows']} rows" for s in FILES))
        return

    keep = {k: v for k, v in meta_all.items() if k != "datasets"}
    keep["datasets"] = [by_file[s] for s in FILES]
    meta_out = (json.dumps(keep, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    mp = os.path.join(DATA, "datasets.json")
    old_meta = open(mp, "rb").read() if os.path.exists(mp) else None
    changed = [s for s in FILES
               if not os.path.exists(os.path.join(DATA, f"{s}.csv"))
               or open(os.path.join(DATA, f"{s}.csv"), "rb").read() != raws[s]]
    if not changed and old_meta == meta_out and not a.force:
        print("no changes")
        return

    # Build the new README first, so a README problem stops the run before any file is written.
    text = open(README, encoding="utf-8").read()
    text = replace_block(text, "files", render_files(by_file, sizes))
    text = replace_block(text, "schema", render_schema(by_file))
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    text = replace_block(text, "stamp", f"**Last refreshed: {stamp} (UTC).** Row counts below match the files in `data/`.")

    os.makedirs(DATA, exist_ok=True)
    for stem in changed:
        with open(os.path.join(DATA, f"{stem}.csv"), "wb") as f:
            f.write(raws[stem])  # byte-for-byte copy of the site file
        print(f"updated {stem}.csv ({by_file[stem]['rows']} rows)")
    with open(mp, "wb") as f:
        f.write(meta_out)
    with open(README, "w", encoding="utf-8") as f:
        f.write(text)
    print("README.md and data/datasets.json refreshed")

if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
