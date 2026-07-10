#!/usr/bin/env python3
"""kr_doc_census - reconcile the repo's source files against the kr/ context docs
in _144_TestKRMCP, in BOTH directions. Hop (4) of the freshness chain; run after
kr_sync (hop 2).

Why this exists: the namespace is a *curated subset* of the repo, hand-assigned to
subjects (kr/<subject>/context/...). Nothing in the repo encodes which subject a
file belongs to, or whether a file should be published at all (the repo also holds
the KB's own prompts, licenses, build READMEs, raw transcripts). So this tool
REPORTS discrepancies rather than blindly mirroring:

  A. ORPHANED namespace docs — a kr/.../context/* doc whose repo source file is gone.
     Excludes intentionally "native" docs (glossary, videos.md, cookbook, course_map,
     quick_start, PDF-derived guide) that have no repo source by design. These are
     candidates to remove; `--prune-missing` deletes them (opt-in, destructive).
     CAVEAT: a doc may be legitimately hand-authored in the namespace with no repo
     source (e.g. brokerShort.md) — verify before pruning.

  B. UNPUBLISHED repo files — doc files in the repo with no namespace counterpart.
     REPORT ONLY: publishing requires a subject-assignment judgment CI can't make.
     Split into "content candidates" vs "likely tooling/meta" (prompts, licenses,
     index) so the list is actionable, not noise.

Resolution reuses kr_sync.py's basename + rename rules so "used" matches what the
content-sync considers a source. Writes a markdown report (--report).

Modes:
  (default)         report only. No writes to Vantiq.
  --prune-missing   delete the ORPHANED namespace docs (section A). Destructive; opt-in.

Env:
  KR_TOKEN   token with read (report) / write (--prune-missing) on _144_TestKRMCP
  KR_REPO    path to the VantiqKnowledge checkout (default: cwd)
"""
from __future__ import annotations
import argparse, collections, datetime, json, os, re, ssl, sys, urllib.parse, urllib.request

NS = "_144_TestKRMCP"
BASE = "https://test.vantiq.com"
TOKEN = os.environ.get("KR_TOKEN", "")
REPO = os.environ.get("KR_REPO") or os.getcwd()
DOC_DIRS = ["blog", "class", "docs", "extra", "extSrc", "guide",
            "k8sdeploy_tools", "lab", "miniVid", "prompts", "sdk"]

try:
    import certifi
    CTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    CTX = ssl.create_default_context()


def api(method, path):
    req = urllib.request.Request(BASE + path, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("X-Target-Namespace", NS)
    with urllib.request.urlopen(req, context=CTX) as r:
        return r.status, r.read().decode("utf-8", "replace")


def norm(s: str) -> str:
    return s.replace("\r\n", "\n").rstrip() + "\n"


# Docs authored/transformed in the namespace with no repo source, by design.
NATIVE = (lambda n: n.startswith("kr/_glossary/") or "/cookbook_" in n
          or n.endswith("/videos.md") or n.endswith("/course_map.md")
          or n.endswith("/quick_start.md")
          or (n.startswith("kr/guide/context/") and n.endswith(".txt")))

# Repo files that are the KB's own tooling / repo meta, not Vantiq knowledge.
def is_tooling(path: str) -> bool:
    base = path.split("/")[-1]
    return (path.startswith("prompts/")
            or base in ("LICENSE.md", "AGENTS.md", "CLAUDE.md", "index.md"))


def build_index():
    by_base = collections.defaultdict(list)
    all_files = []
    for d in DOC_DIRS:
        for root, _, files in os.walk(os.path.join(REPO, d)):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), REPO)
                by_base[f].append(rel)
                all_files.append(rel)
    return by_base, all_files


def repo_text(rel):
    try:
        return open(os.path.join(REPO, rel), encoding="utf-8", errors="replace").read()
    except Exception:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prune-missing", action="store_true",
                    help="delete orphaned namespace docs (section A). Destructive.")
    ap.add_argument("--report", default="doc-census-report.md")
    args = ap.parse_args()
    if not TOKEN:
        sys.exit("set KR_TOKEN")

    by_base, all_files = build_index()
    _, raw = api("GET", "/api/v1/resources/documents?limit=2000")
    docs = [d["name"] for d in json.loads(raw)
            if d["name"].startswith("kr/") and "/context/" in d["name"]]

    bodycache = {}
    def ns_body(name):
        if name not in bodycache:
            try:
                bodycache[name] = api("GET", "/docs/" + urllib.parse.quote(name, safe="/"))[1]
            except Exception:
                bodycache[name] = None
        return bodycache[name]

    def resolve(name):
        """Return list of repo paths this namespace doc maps to ([] if none)."""
        base = name.split("/")[-1]
        hits = by_base.get(base, [])
        if len(hits) == 1:
            return [hits[0]]
        if "_" in base:
            if base.endswith("_README.md"):
                dd = base[:-len("_README.md")]
                c = [h for h in by_base.get("README.md", [])
                     if h.endswith(f"/{dd}/README.md") or h == f"{dd}/README.md"]
                if len(c) == 1:
                    return c
            P, R = base.split("_", 1)
            c = [h for h in by_base.get(R, [])
                 if h.endswith(f"/{P}/{R}") or h == f"{P}/{R}"]
            if len(c) == 1:
                return c
        dis = [p for bn, ps in by_base.items() if bn.endswith("_" + base) for p in ps]
        if dis:
            b = ns_body(name)
            if b is not None:
                for h in dis:
                    if norm(repo_text(h)) == norm(b):
                        return [h]
        if len(hits) > 1:
            b = ns_body(name)
            if b is not None:
                for h in hits:
                    if norm(repo_text(h)) == norm(b):
                        return [h]
            return hits            # ambiguous -> conservatively treat all as used
        return []

    used, native, orphaned = set(), [], []
    for name in docs:
        r = resolve(name)
        if r:
            used.update(r)
        elif NATIVE(name):
            native.append(name)
        else:
            orphaned.append(name)

    unpublished = sorted(set(all_files) - used)
    candidates = [p for p in unpublished if not is_tooling(p)]
    tooling = [p for p in unpublished if is_tooling(p)]

    pruned = []
    if args.prune_missing:
        for name in orphaned:
            api("DELETE", "/api/v1/resources/documents/" + urllib.parse.quote(name, safe=""))
            pruned.append(name)

    write_report(args.report, docs, native, orphaned, used, all_files,
                 candidates, tooling, pruned)

    print(f"repo doc files      : {len(all_files)}")
    print(f"namespace ctx docs  : {len(docs)}  (native {len(native)}, orphaned {len(orphaned)})")
    print(f"unpublished         : {len(unpublished)}  (candidates {len(candidates)}, tooling/meta {len(tooling)})")
    print(f"orphaned {'PRUNED' if args.prune_missing else 'reported'} : {len(pruned) if args.prune_missing else len(orphaned)}")
    print(f"report              : {args.report}")


def write_report(path, docs, native, orphaned, used, all_files, candidates, tooling, pruned):
    gen = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    L = ["# KR Doc Census (repo ↔ namespace)", "",
         f"_Generated {gen} · namespace `{NS}`_", "",
         f"- Repo doc files: **{len(all_files)}** · namespace context docs: **{len(docs)}** "
         f"(native/no-source {len(native)})",
         f"- **Orphaned** namespace docs (repo source gone): **{len(orphaned)}**"
         + (f" — **{len(pruned)} PRUNED this run**" if pruned else ""),
         f"- **Unpublished** repo files: **{len(candidates) + len(tooling)}** "
         f"({len(candidates)} content candidates, {len(tooling)} tooling/meta)", ""]

    L += ["## A. Orphaned namespace docs (repo source gone)", ""]
    if orphaned:
        L.append("Candidates to remove. **Caveat:** a doc may be intentionally "
                 "hand-authored in the namespace (no repo source) — verify before pruning. "
                 "Run with `--prune-missing` to delete these.")
        L.append("")
        for n in sorted(orphaned):
            L.append(f"- [ ] `{n}`" + ("  — **pruned**" if n in pruned else ""))
    else:
        L.append("_None._")
    L.append("")

    L += ["## B. Unpublished repo files — content candidates", "",
          "Repo doc files with no namespace doc. Publishing each is a curation call "
          "(which subject? should it be published at all?), so this is report-only. "
          "Tell me which to publish and I'll categorize + add them in-session.", ""]
    if candidates:
        bydir = collections.defaultdict(list)
        for p in candidates:
            bydir[p.split("/")[0]].append(p)
        for d in sorted(bydir):
            L.append(f"### `{d}/` ({len(bydir[d])})")
            for p in sorted(bydir[d]):
                L.append(f"- [ ] `{p}`")
            L.append("")
    else:
        L.append("_None._\n")

    L += ["## C. Unpublished — likely tooling / meta (probably ignore)", "",
          "The KB's own prompts, licenses, and index files — not Vantiq knowledge. "
          "Listed for completeness.", ""]
    L.append(f"{len(tooling)} file(s): " + ", ".join(f"`{p}`" for p in sorted(tooling)) if tooling else "_None._")
    L.append("")

    text = "\n".join(L).rstrip() + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    main()
