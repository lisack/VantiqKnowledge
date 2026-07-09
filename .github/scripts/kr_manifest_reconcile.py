#!/usr/bin/env python3
"""kr_manifest_reconcile - keep the kr/ manifests in _144_TestKRMCP in step with
the namespace doc set WITHOUT ever clobbering curated descriptions.

Hop (3) of the freshness chain. Runs after kr_sync (hop 2) has refreshed doc
content. This is a MERGE, not a regenerate-from-scratch: the manifest living in
the namespace IS the store of curated descriptions, so we read it, keep every
existing description verbatim, and only fill gaps.

## Provenance markers (curation worklist)

A "## Context" entry is `- <uri> | <description>`. The trailing token records who
wrote the description:

  * no marker        -> CURATED by a human (blessed). Preserved verbatim forever.
  * `[auto]`         -> a content-based best-guess (written by Claude in-session or
                        by an LLM step). Accurate, but not yet blessed.
  * `[auto-draft]`   -> a cheap filename-derived draft written by THIS script when a
                        new doc appeared mid-week and no better source was available.
                        Lowest confidence; describe it properly.

You "bless" an entry by editing its description and removing the trailing marker.
Both `[auto]` and `[auto-draft]` are reported every run as the curation worklist,
drafts first. The set is always exactly recoverable, so nothing slips by.

## What each run does, per SUBJECT manifest (kr/<cat>/manifest.txt)

  * doc already listed              -> line kept verbatim (marker, if any, intact)
  * doc under kr/<cat>/context/ not yet listed (a NEW doc)
        -> appended with a filename draft + `[auto-draft]`
  * listed doc whose namespace document has vanished (orphan)
        -> reported; NOT removed by default (a transient absence must never lose a
           curated line). Pass --prune-orphans to drop them.

CROSS-CUTTING manifests (kr/_topics/*, kr/_glossary/*) reference docs across many
subjects by human curation - they do NOT "own" a prefix, so new docs are never
auto-added to them; their entries are still scanned for the worklist and orphans.

Everything outside the "## Context" list is preserved byte-for-byte. A markdown
drift report is always written (--report PATH) for weekly commit.

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

DRAFT_MARK = "[auto-draft]"   # filename draft written by this script (lowest confidence)
AUTO_MARK = "[auto]"          # content-based best-guess, not yet human-blessed


def marker_of(desc: str):
    """Return 'auto-draft', 'auto', or None (curated) for a description string."""
    d = desc.rstrip()
    if d.endswith(DRAFT_MARK):
        return "auto-draft"
    if d.endswith(AUTO_MARK):
        return "auto"
    return None


def draft_desc(name: str) -> str:
    """Best-effort human-readable draft from a doc's filename."""
    base = name.split("/")[-1]
    base = re.sub(r"\.(txt|md|json|vail)$", "", base, flags=re.I)
    words = []
    for tok in base.split("_"):
        if not tok or LEVEL.match(tok):
            continue
        words.append(re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", tok))   # split CamelCase
    return (" ".join(words).strip().lower()) or base.lower()


def new_entry_line(name: str) -> str:
    return f"- {to_uri(name)} | {draft_desc(name)} {DRAFT_MARK}"


def reconcile_manifest(text, ns_names, owns_prefix, prune):
    """Return (new_text, new_docs, orphans, uncurated).
    new_docs only for prefix owners; uncurated is [(name, marker)] over the result."""
    lines = text.split("\n")

    ctx_i = next((i for i, ln in enumerate(lines) if CTX_HEADER.match(ln)), None)
    if ctx_i is None:
        return text, [], [], []                  # no Context section: leave alone

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

    # classify every resulting Context entry for the worklist
    uncurated = []
    for ln in new_body:
        m = ENTRY.match(ln)
        if m:
            mark = marker_of(m.group(2))
            if mark:
                uncurated.append((to_name(m.group(1)), mark))

    new_text = "\n".join(lines[:ctx_i + 1] + new_body + lines[end:])
    if not new_text.endswith("\n"):
        new_text += "\n"
    return new_text, new_docs, orphans, uncurated


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
    total_unc = sum(len(r["uncurated"]) for r in results)
    total_draft = sum(1 for r in results for _, mk in r["uncurated"] if mk == "auto-draft")
    total_auto = total_unc - total_draft

    drift = total_new or total_orph
    status = (f"DRIFT — {total_new} new doc(s), {total_orph} orphaned entrie(s)"
              if drift else "IN SYNC — no new docs, no orphans")

    L = []
    L.append("# KR Manifest Drift Report")
    L.append("")
    L.append(f"_Generated {generated} · namespace `{NS}` · mode: {mode}_")
    L.append("")
    L.append(f"**Structure: {status}.**")
    L.append(f"**Curation worklist: {total_unc} uncurated entrie(s)** "
             f"({total_draft} `[auto-draft]`, {total_auto} `[auto]`) — "
             "bless one by editing its description in the namespace manifest and "
             "deleting the trailing marker.")
    L.append("")
    L.append("## Summary")
    L.append("")
    L.append("| Manifest | Entries | New | Uncurated | Orphaned |")
    L.append("|---|---:|---:|---:|---:|")
    for r in sorted(results, key=lambda r: r["name"]):
        if r["new"] or r["orphans"] or r["uncurated"]:
            L.append(f"| `{r['name']}` | {r['entries']} | {len(r['new'])} "
                     f"| {len(r['uncurated'])} | {len(r['orphans'])} |")
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

    if total_unc:
        L.append("## Curation worklist (uncurated descriptions)")
        L.append("")
        L.append("`[auto-draft]` = rough filename draft (describe it); `[auto]` = "
                 "content-based best-guess (bless or tweak). Clear a marker to curate.")
        L.append("")
        for r in sorted(results, key=lambda r: r["name"]):
            if r["uncurated"]:
                drafts = [n for n, mk in r["uncurated"] if mk == "auto-draft"]
                autos = [n for n, mk in r["uncurated"] if mk == "auto"]
                L.append(f"### `{r['name']}`")
                for n in drafts:
                    L.append(f"- [ ] `{n}` — `[auto-draft]`")
                for n in autos:
                    L.append(f"- [ ] `{n}` — `[auto]`")
                L.append("")

    text = "\n".join(L).rstrip() + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return status, total_unc


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
        new_text, new_docs, orphans, uncurated = reconcile_manifest(
            text, ns_names, prefix, args.prune_orphans)
        entries = len(re.findall(r"(?m)^-\s+\S+\s*\|", text))
        did_change = norm(new_text) != norm(text)
        if did_change and args.apply:
            api("POST", "/api/v1/resources/documents?upsert=true",
                {"name": name, "fileType": "text/plain", "content": new_text})
            changed += 1
        results.append({"name": name, "entries": entries, "new": new_docs,
                        "orphans": orphans, "uncurated": uncurated,
                        "pruned": args.prune_orphans and bool(orphans),
                        "changed": did_change})

    generated = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    mode = "apply" if args.apply else "dry-run"
    status, worklist = write_report(args.report, mode, results, generated)

    print(f"manifests scanned : {len(manifests)}")
    print(f"  changed         : {changed}" + ("" if args.apply else "  [dry-run; not written]"))
    print(f"  new docs total  : {sum(len(r['new']) for r in results)}")
    print(f"  orphans total   : {sum(len(r['orphans']) for r in results)}")
    print(f"  uncurated total : {worklist}")
    print(f"report            : {args.report}")
    print(f"status            : {status}")


if __name__ == "__main__":
    main()
