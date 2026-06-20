#!/usr/bin/env python3
"""kr_sync - refresh the manifested kr/ corpus in _144_TestKRMCP from the repo.

Hop (2) of the freshness chain. For each kr/<cat>/context/<doc> already in the
namespace, resolve its source file in the VantiqKnowledge checkout and refresh
the namespace document's CONTENT when it has drifted upstream.

It does NOT touch manifests, invent categories, or delete docs - structure and
manifest guidance are human-curated. Docs that are authored directly in the
namespace (glossary, VAIL cookbook snippets, per-subject video indexes) have no
repo source and are recognised as "native" and left untouched.

Modes:
  (default)   dry-run: resolve mapping, report drift. No writes to Vantiq.
  --publish   upsert drifted docs into the namespace (idempotent).

Env:
  KR_TOKEN    token with read (dry-run) / write (--publish) on _144_TestKRMCP
  KR_REPO     path to the VantiqKnowledge checkout (default: current dir)
"""
from __future__ import annotations
import json, os, re, ssl, sys, tempfile, urllib.request, urllib.parse, collections

REPO = os.environ.get("KR_REPO") or os.getcwd()
NS = "_144_TestKRMCP"
BASE = "https://test.vantiq.com"
TOKEN = os.environ.get("KR_TOKEN", "")
PUBLISH = "--publish" in sys.argv

# Docs not produced by file-copy from the repo - authored in the namespace, or
# transformed (PDF->text). No repo source by design; the content sync never touches them.
NATIVE = (
    lambda n: n.startswith("kr/_glossary/")
    or "/cookbook_" in n
    or n.endswith("/videos.md")
    or n.endswith("/course_map.md")
    or n.endswith("/quick_start.md")
    or (n.startswith("kr/guide/context/") and n.endswith(".txt"))   # PDF-derived; refreshed by extraction, not copy
)

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


def main():
    if not TOKEN:
        sys.exit("set KR_TOKEN")

    _, raw = api("GET", "/api/v1/resources/documents?limit=2000")
    docs = [d for d in json.loads(raw) if d["name"].startswith("kr/") and "/context/" in d["name"]]

    by_base = collections.defaultdict(list)
    for root, _, files in os.walk(REPO):
        if "/.git" in root:
            continue
        for f in files:
            by_base[f].append(os.path.relpath(os.path.join(root, f), REPO))

    def repo_text(rel):
        return open(os.path.join(REPO, rel), encoding="utf-8", errors="replace").read()

    def resolve(name, ns_body_getter):
        """Return repo-relative source path, or None."""
        base = name.split("/")[-1]
        hits = by_base.get(base, [])
        if len(hits) == 1:
            return hits[0]
        # rename rules (the namespace flattens a subdir into the basename):
        if "_" in base:
            # suffix form: "<dir>_README.md" <- ".../<dir>/README.md"  (dir may contain '_')
            if base.endswith("_README.md"):
                d = base[: -len("_README.md")]
                cands = [h for h in by_base.get("README.md", []) if h.endswith(f"/{d}/README.md") or h == f"{d}/README.md"]
                if len(cands) == 1:
                    return cands[0]
            # prefix form: "<P>_<R>" <- ".../<P>/<R>"  (disambiguating prefixes like GAB_, AIinEDA_)
            P, R = base.split("_", 1)
            cands = [h for h in by_base.get(R, []) if h.endswith(f"/{P}/{R}") or h == f"{P}/{R}"]
            if len(cands) == 1:
                return cands[0]
        # ambiguous basename: pick the candidate whose content matches the namespace doc
        if len(hits) > 1:
            body = ns_body_getter()
            if body is not None:
                for h in hits:
                    if norm(repo_text(h)) == norm(body):
                        return h
        return None

    mapping, drift, insync, native, orphaned = {}, [], [], [], []
    for d in docs:
        name = d["name"]
        _cache = {}

        def ns_body():
            if "v" not in _cache:
                try:
                    _cache["v"] = api("GET", "/docs/" + urllib.parse.quote(name, safe="/"))[1]
                except Exception:
                    _cache["v"] = None
            return _cache["v"]

        src = resolve(name, ns_body)
        if src is None:
            (native if NATIVE(name) else orphaned).append(name)
            continue
        mapping[name] = src
        body = ns_body()
        if body is not None and norm(repo_text(src)) != norm(body):
            drift.append((name, src))
            if PUBLISH:
                ft = "text/markdown" if name.endswith(".md") else \
                     "application/json" if name.endswith(".json") else "text/plain"
                api("POST", "/api/v1/resources/documents?upsert=true",
                    {"name": name, "fileType": ft, "content": repo_text(src)})
        else:
            insync.append(name)

    print(f"namespace kr/ context docs : {len(docs)}")
    print(f"  resolved to a repo source: {len(mapping)}")
    print(f"  in sync                  : {len(insync)}")
    print(f"  drifted (refreshed)      : {len(drift)}" + ("  [PUBLISHED]" if PUBLISH else "  [dry-run]"))
    print(f"  native (left untouched)  : {len(native)}")
    print(f"  ORPHANED (source gone)   : {len(orphaned)}")
    for n, s in drift[:40]:
        print("    drift:", n, "<-", s)
    for n in orphaned:
        print("    orphaned:", n)

    out = os.path.join(tempfile.gettempdir(), "kr_mapping.json")
    json.dump({"mapping": mapping, "drift": [n for n, _ in drift],
               "native": native, "orphaned": orphaned}, open(out, "w"), indent=2)
    print("\nwrote", out)
    # Orphans are informational (e.g. a source pending re-sync); don't fail the run.


if __name__ == "__main__":
    main()
