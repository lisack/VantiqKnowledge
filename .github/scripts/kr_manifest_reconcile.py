#!/usr/bin/env python3
"""kr_manifest_reconcile - keep the kr/ manifests in _144_TestKRMCP in step with
the namespace doc set WITHOUT ever clobbering curated descriptions.

Hop (3) of the freshness chain. Runs after kr_sync (hop 2) has refreshed doc
content. This is a MERGE, not a regenerate-from-scratch: the manifest living in
the namespace IS the store of curated descriptions, so we read it, keep every
existing description verbatim, and only fill gaps.

For each SUBJECT manifest (kr/<cat>/manifest.txt) it reconciles the "## Context"
list against the namespace docs under that manifest's kr/<cat>/context/ prefix:

  * doc already listed              -> description kept verbatim (preserved)
  * doc present under the prefix but NOT listed (a genuinely NEW doc)
        -> appended as a new entry carrying a "NEEDS DESCRIPTION" sentinel plus a
           filename-derived draft, so you know exactly which entries to describe
  * listed doc whose namespace document has vanished (orphan)
        -> reported; NOT removed by default (a transient absence must never lose
           a curated line). Pass --prune-orphans to drop them.

CROSS-CUTTING manifests (kr/_topics/*, kr/_glossary/*) reference docs across many
subjects by human curation - they do NOT "own" a prefix, so new docs are never
auto-added to them; only orphaned entries are reported.

Everything outside the "## Context" list (H1 title, subject blurb, "## See Also",
blank lines, entry ordering) is preserved byte-for-byte.

A markdown drift report is always written (--report PATH) for weekly commit.

Modes:
  (default)        dry-run: compute + write report. No writes to Vantiq.
  --apply          upsert changed manifests into the namespace.
  --prune-orphans  also drop manifest entries whose namespace doc is gone.

Env:
  KR_TOKEN   token with read (dry-run) / write (--apply) on _144_TestKRMCP
"""
from __future__ import annotations
import argparse, datetime, json, os, re, ssl, sys, urllib.parse, urllib.request

NS = "_144_TestKRMCP"
BASE = "https://test.vantiq.com"
TOKEN = os.environ.get("KR_TOKEN", "")

try:
    import certifi
    CTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    CTX = ssl.create_default_context()   # system CA bundle (fine on CI runners)


def api(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None)
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("X-Target-Namespace", NS)
    if body is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, context=CTX) as r:
        return r.status, r.read().decode("utf-8", "replace")


def norm(s: str) -> str:
    return s.replace("\r\n", "\n").rstrip() + "\n"


def to_name(uri: str) -> str:
    return uri[len("vantiq://"):] if uri.startswith("vantiq://") else uri


def to_uri(name: str) -> str:
    return name if name.startswith("vantiq://") else "vantiq://" + name


# ---- pure text logic (unit-testable without a token) ------------------------

CTX_HEADER = re.compile(r"^##\s+Context\b", re.I)
SECTION = re.compile(r"^##\s+")
ENTRY = re.compile(r"^-\s+(\S+)\s*\|\s*(.*)$")   # "- <uri> | <description>"
# version/level/course-code tokens carry no descriptive value in a filename
LEVEL = re.compile(r"^(L\d+|v\d+|\d+(\.\d+)*)$", re.I)
SENTINEL = "⚠ NEEDS DESCRIPTION"            # "WARNING SIGN + text"


def draft_desc(name: str) -> str:
    """Best-effort human-readable draft from a doc's filename."""
    base = name.split("/")[-1]
    base = re.sub(r"\.(txt|md|json)$", "", base, flags=re.I)
    words = []
    for tok in base.split("_"):
        if not tok or LEVEL.match(tok):
            continue
        words.append(re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", tok))   # split CamelCase
    return (" ".join(words).strip().lower()) or base.lower()


def new_entry_line(name: str) -> str:
    return f'- {to_uri(name)} | {SENTINEL} — draft: "{draft_desc(name)}"'


def reconcile_manifest(text, ns_names, owns_prefix, prune):
    """Return (new_text, new_docs, orphans). new_docs only for prefix owners."""
    lines = text.split("\n")

    ctx_i = next((i for i, ln in enumerate(lines) if CTX_HEADER.match(ln)), None)
    if ctx_i is None:
        return text, [], []                      # no Context section: leave alone

    end = len(lines)
    for j in range(ctx_i + 1, len(lines)):
        if SECTION.match(lines[j]):
            end = j
            break
    body = lines[ctx_i + 1:end]

    referenced, entry_pos = [], []
    for k, ln in enumerate(body):
        m = ENTRY.match(ln)
        if m:
            referenced.append(to_name(m.group(1)))
            entry_pos.append(k)
    ref_set = set(referenced)

    orphans = [n for n in referenced if n not in ns_names]

    new_docs = []
    if owns_prefix:
        for n in sorted(ns_names):
            if n.startswith(owns_prefix) and not n.endswith("/manifest.txt") and n not in ref_set:
                new_docs.append(n)

    last_entry = entry_pos[-1] if entry_pos else len(body) - 1
    new_body = []
    for k, ln in enumerate(body):
        m = ENTRY.match(ln)
        if m and prune and to_name(m.group(1)) in orphans:
            continue                             # drop orphan line
        new_body.append(ln)
        if k == last_entry and new_docs:
            new_body.extend(new_entry_line(n) for n in new_docs)
    if not entry_pos and new_docs:               # empty Context list
        new_body.extend(new_entry_line(n) for n in new_docs)

    new_text = "\n".join(lines[:ctx_i + 1] + new_body + lines[end:])
    if not new_text.endswith("\n"):
        new_text += "\n"
    return new_text, new_docs, orphans


def owned_prefix(manifest_name):
    """Subject manifest kr/<cat>/manifest.txt owns kr/<cat>/context/.
    Cross-cutting (_topics/*, _glossary, any '_'-prefixed cat) owns nothing."""
    m = re.match(r"^kr/([^/]+)/manifest\.txt$", manifest_name)
    if m and not m.group(1).startswith("_"):
        return f"kr/{m.group(1)}/context/"
    return None


# ---- report -----------------------------------------------------------------

def write_report(path, mode, results, generated):
    total_new = sum(len(r["new"]) for r in results)
    total_orph = sum(len(r["orphans"]) for r in results)
    status = ("CLEAN— manifests in sync with the namespace"
              if total_new == 0 and total_orph == 0
              else f"DRIFT — {total_new} new doc(s) need descriptions, "
                   f"{total_orph} orphaned entrie(s)")

    L = []
    L.append("# KR Manifest Drift Report")
    L.append("")
    L.append(f"_Generated {generated} · namespace `{NS}` · mode: {mode}_")
    L.append("")
    L.append(f"**Status: {status}.**")
    L.append("")
    L.append("## Summary")
    L.append("")
    L.append("| Manifest | Entries | New (added) | Orphaned |")
    L.append("|---|---:|---:|---:|")
    for r in sorted(results, key=lambda r: r["name"]):
        if r["new"] or r["orphans"]:
            L.append(f"| `{r['name']}` | {r['entries']} | {len(r['new'])} | {len(r['orphans'])} |")
    if total_new == 0 and total_orph == 0:
        L.append("| _(all manifests in sync)_ | | 0 | 0 |")
    L.append("")

    if total_new:
        L.append("## New docs needing descriptions")
        L.append("")
        L.append("Each was appended to its manifest with a `⚠ NEEDS DESCRIPTION` "
                 "sentinel and a filename-derived draft. Edit the description in the "
                 "namespace manifest to replace the draft — that clears the sentinel "
                 "and the line is preserved verbatim on every future run.")
        L.append("")
        for r in sorted(results, key=lambda r: r["name"]):
            if r["new"]:
                L.append(f"### `{r['name']}`")
                for n in r["new"]:
                    L.append(f'- [ ] `{n}` — draft: "{draft_desc(n)}"')
                L.append("")

    if total_orph:
        L.append("## Orphaned entries (source doc missing)")
        L.append("")
        note = ("Removed this run (`--prune-orphans`)." if any(r["pruned"] for r in results)
                else "Kept in place so the curated description is not lost. Investigate, "
                     "then remove by hand or re-run with `--prune-orphans`.")
        L.append(note)
        L.append("")
        for r in sorted(results, key=lambda r: r["name"]):
            if r["orphans"]:
                L.append(f"### `{r['name']}`")
                for n in r["orphans"]:
                    L.append(f"- `{to_uri(n)}`")
                L.append("")

    text = "\n".join(L).rstrip() + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return status


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="upsert changed manifests to the namespace")
    ap.add_argument("--prune-orphans", action="store_true", help="also drop entries whose doc is gone")
    ap.add_argument("--report", default="manifest-drift-report.md", help="markdown report output path")
    args = ap.parse_args()

    if not TOKEN:
        sys.exit("set KR_TOKEN")

    _, raw = api("GET", "/api/v1/resources/documents?limit=2000")
    ns_names = {d["name"] for d in json.loads(raw) if d["name"].startswith("kr/")}
    manifests = sorted(n for n in ns_names if n.endswith("/manifest.txt"))

    results, changed = [], 0
    for name in manifests:
        _, text = api("GET", "/docs/" + urllib.parse.quote(name, safe="/"))
        prefix = owned_prefix(name)
        new_text, new_docs, orphans = reconcile_manifest(text, ns_names, prefix, args.prune_orphans)
        entries = len(re.findall(r"(?m)^-\s+\S+\s*\|", text))
        did_change = norm(new_text) != norm(text)
        if did_change and args.apply:
            api("POST", "/api/v1/resources/documents?upsert=true",
                {"name": name, "fileType": "text/plain", "content": new_text})
            changed += 1
        results.append({"name": name, "entries": entries, "new": new_docs,
                        "orphans": orphans, "pruned": args.prune_orphans and bool(orphans),
                        "changed": did_change})

    generated = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    mode = "apply" if args.apply else "dry-run"
    status = write_report(args.report, mode, results, generated)

    print(f"manifests scanned : {len(manifests)}")
    print(f"  changed         : {changed}" + ("" if args.apply else "  [dry-run; not written]"))
    print(f"  new docs total  : {sum(len(r['new']) for r in results)}")
    print(f"  orphans total   : {sum(len(r['orphans']) for r in results)}")
    print(f"report            : {args.report}")
    print(f"status            : {status}")


if __name__ == "__main__":
    main()
