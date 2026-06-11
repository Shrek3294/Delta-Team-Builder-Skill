#!/usr/bin/env python3
"""PreToolUse(Bash) hook: the breadth/early layer of the export gate.

Two jobs:
  1. Block ANY Bash command that produces a .docx/.pdf unless it goes through the
     single canonical exporter tools/md_to_docx_pdf.py. This catches the legacy
     one-off teams/build_*.py|js scripts and ad-hoc evasions (python -c, node -e,
     renamed scripts, copied output paths).
  2. When the canonical exporter IS used, run lint_team.lint_for_export on the
     source .md and block on any HARD FAIL (before the slow conversion starts).

The converter itself re-lints fail-closed (tools/md_to_docx_pdf.py), so this hook
is defense-in-depth, not the sole guarantee. Blocking = exit code 2 with the
reason on stderr (Claude Code surfaces stderr to the model on a blocked PreToolUse).
Anything not docx/pdf-related is allowed (exit 0).
"""
import sys
import os
import re
import json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CANONICAL = "md_to_docx_pdf.py"


def _deny(reason):
    sys.stderr.write(reason + "\n")
    sys.exit(2)


def _allow():
    sys.exit(0)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        _allow()  # can't parse -> don't interfere with unrelated commands
    cmd = (payload.get("tool_input") or {}).get("command") or ""
    low = cmd.lower()

    canonical = CANONICAL in low
    produces_doc = (".docx" in low) or (".pdf" in low)
    if not (canonical or produces_doc):
        _allow()

    if produces_doc and not canonical:
        _deny(
            "EXPORT BLOCKED: deliverable docx/pdf must be produced via the single "
            "canonical exporter `tools/md_to_docx_pdf.py` (which runs the factual "
            "lint gate). This command produces a .docx/.pdf another way "
            "(legacy teams/build_* script, python -c, node -e, etc.) and is denied. "
            "Re-run as: python tools/md_to_docx_pdf.py <draft.md> <out.docx> <out.pdf>")

    # Canonical exporter invoked: find the source .md and lint (fail CLOSED if we can't).
    md = re.findall(r'"([^"]+\.md)"|\'([^\']+\.md)\'|(\S+\.md)', cmd)
    srcs = [a or b or c for (a, b, c) in md]
    if not srcs:
        _deny("EXPORT BLOCKED: could not identify the source .md argument in the "
              "export command. Pass the draft path explicitly: "
              "python tools/md_to_docx_pdf.py <draft.md> <out.docx> <out.pdf>")
    src = srcs[0]
    if not os.path.isabs(src):
        src = os.path.join(ROOT, src)
    if not os.path.exists(src):
        _deny("EXPORT BLOCKED: source markdown not found: %s" % src)

    sys.path.insert(0, HERE)
    try:
        import lint_team
        res = lint_team.lint_for_export(src)
    except Exception as e:
        _deny("EXPORT BLOCKED: lint gate failed to run (%s). Fix the linter or data "
              "files before exporting." % e)

    if not res.ok:
        lint_team._log_denial(src, res)
        _deny("EXPORT BLOCKED by the factual gate:\n\n" + res.report() +
              "\n\nFix these, or add confirmed data gaps to data/lint_allowlists.json.")
    _allow()


if __name__ == "__main__":
    main()
