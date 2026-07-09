import sys
sys.argv = ["x"]  # keep argparse in the module from grabbing pytest-style args
import kr_manifest_reconcile as R

# The REAL kr/test/manifest.txt content (fetched from the namespace via MCP).
MANIFEST = """# Vantiq Knowledge — Test

Vantiq Test — verifying applications: testing methodology, unit and integration tests, source mocking, event captures, and event generators.

## Context (uri | description)

- vantiq://kr/test/context/E_EDAFound_142_DCL1_L2_2.3_EventGenerator.txt | foundations: captures/event generators
- vantiq://kr/test/context/134_Testing_L1_1.1_Steps.txt | testing methodology
- vantiq://kr/test/context/134_Testing_L1_1.2_Unit.txt | unit testing
- vantiq://kr/test/context/134_Testing_L1_1.3_Mocking.txt | source mocking
- vantiq://kr/test/context/134_Testing_L1_1.4_Integration.txt | integration testing
- vantiq://kr/test/context/tests.md | testing reference
- vantiq://kr/test/context/capture.md | event captures
- vantiq://kr/test/context/eventgenerators.md | event generators
- vantiq://kr/test/context/videos.md | Video index — 6 YouTube links in this subject, with topic + source-transcript mapping. Use this instead of reading full transcripts when a question only needs a video citation.

## See Also

- vantiq://kr/service/manifest.txt — Service Builder Test mode and integration tests against services
- vantiq://kr/vail/manifest.txt — trace/autopsy when a test fails; log statements inside test runs
- vantiq://kr/source/manifest.txt — source mocking — start/stop a source's connection to its real backend
"""

# Simulated namespace: drop capture.md (=> orphan), add a NEW fixtures doc.
ns_names = {
    "kr/test/manifest.txt",
    "kr/test/context/E_EDAFound_142_DCL1_L2_2.3_EventGenerator.txt",
    "kr/test/context/134_Testing_L1_1.1_Steps.txt",
    "kr/test/context/134_Testing_L1_1.2_Unit.txt",
    "kr/test/context/134_Testing_L1_1.3_Mocking.txt",
    "kr/test/context/134_Testing_L1_1.4_Integration.txt",
    "kr/test/context/tests.md",
    # capture.md intentionally MISSING -> orphan
    "kr/test/context/eventgenerators.md",
    "kr/test/context/videos.md",
    "kr/test/context/134_Testing_L1_1.5_Fixtures.txt",   # NEW
}

prefix = R.owned_prefix("kr/test/manifest.txt")
assert prefix == "kr/test/context/", prefix
assert R.owned_prefix("kr/_topics/debugging/manifest.txt") is None
assert R.owned_prefix("kr/_glossary/manifest.txt") is None
print("owned_prefix OK")

# Give one existing entry an [auto] marker to prove it is preserved AND counted.
MANIFEST = MANIFEST.replace(
    "134_Testing_L1_1.2_Unit.txt | unit testing",
    "134_Testing_L1_1.2_Unit.txt | unit testing [auto]")

new_text, new_docs, orphans, uncurated = R.reconcile_manifest(MANIFEST, ns_names, prefix, prune=False)

# 1) curated descriptions preserved verbatim (no marker); [auto] entry kept intact
for kept in ["| source mocking", "| unit testing [auto]",
             "Use this instead of reading full transcripts"]:
    assert kept in new_text, f"LOST description: {kept}"
assert "| source mocking\n" in new_text          # curated line unchanged (no marker added)
print("descriptions preserved OK")

# 2) new doc detected & appended with a filename draft + [auto-draft] marker
assert new_docs == ["kr/test/context/134_Testing_L1_1.5_Fixtures.txt"], new_docs
assert "134_Testing_L1_1.5_Fixtures.txt | testing fixtures [auto-draft]" in new_text
print("new-doc append OK  ->  draft:", repr(R.draft_desc(new_docs[0])))

# 3) orphan detected, NOT pruned by default (line still present)
assert orphans == ["kr/test/context/capture.md"], orphans
assert "capture.md | event captures" in new_text
print("orphan detected & kept OK")

# 4) uncurated worklist = the [auto] entry + the new [auto-draft] entry; curated excluded
unc = dict(uncurated)
assert unc.get("kr/test/context/134_Testing_L1_1.2_Unit.txt") == "auto", uncurated
assert unc.get("kr/test/context/134_Testing_L1_1.5_Fixtures.txt") == "auto-draft", uncurated
assert "kr/test/context/134_Testing_L1_1.3_Mocking.txt" not in unc, "curated line flagged"
assert len(uncurated) == 2, uncurated
print("uncurated worklist OK ->", uncurated)

# 5) See Also preserved
assert "## See Also" in new_text
assert "trace/autopsy when a test fails" in new_text
print("See Also preserved OK")

# 6) new entry inserted INSIDE context list (before ## See Also), not after it
assert new_text.index("1.5_Fixtures") < new_text.index("## See Also")
print("insertion position OK")

# 7) prune mode removes the orphan line
pruned_text, _, orph2, _ = R.reconcile_manifest(MANIFEST, ns_names, prefix, prune=True)
assert "capture.md" not in pruned_text, "orphan not pruned"
assert orph2 == ["kr/test/context/capture.md"]
print("prune OK")

# 8) idempotency: feeding the reconciled text back (new doc now present) => no changes
ns2 = set(ns_names)
again_text, again_new, again_orph, again_unc = R.reconcile_manifest(new_text, ns2, prefix, prune=False)
assert again_new == [], again_new           # nothing new the second time
assert R.norm(again_text) == R.norm(new_text), "not idempotent"
assert len(again_unc) == 2, again_unc       # worklist stable across runs
print("idempotent OK")

# 9) marker_of + draft heuristic spot-checks
assert R.marker_of("plain text") is None
assert R.marker_of("best guess [auto]") == "auto"
assert R.marker_of("rough draft [auto-draft]") == "auto-draft"
assert R.draft_desc("kr/ai/context/132_GenAI_L2_2.7_AgentMemory.txt") == "gen ai agent memory"
assert R.draft_desc("kr/vail-cookbook/context/cookbook_try_catch.vail") == "cookbook try catch"
print("marker_of + draft heuristic OK")

print("\nALL TESTS PASSED")
print("\n--- reconciled Context section (excerpt) ---")
for ln in new_text.splitlines():
    if "1.5_Fixtures" in ln or "capture.md" in ln:
        print(ln)
