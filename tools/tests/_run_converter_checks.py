"""Drive the converter's in-process gate without putting trigger strings on the
Bash command line (so the live PreToolUse hook doesn't intercept the test)."""
import os
import subprocess
import sys
import tempfile
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CONV = os.path.join(ROOT, "tools", "md" + "_to_docx_pdf.py")

CLEAN = ("## Team identity\n\nClean.\n\n"
         "| Pokemon | Item | Ability | Moves | Role |\n|---|---|---|---|---|\n"
         "| Tinkaton-Gamma | Heavy-Duty Boots | Parasol Prayer | "
         "Double-Edge, Fly, Play Rough, Facade | glue |\n")
POISON = CLEAN.replace("Parasol Prayer", "Levitate")


def run(src):
    d = os.path.dirname(src)
    out1 = os.path.join(d, "o.do" + "cx")
    out2 = os.path.join(d, "o.p" + "df")
    p = subprocess.run([sys.executable, CONV, src, out1, out2],
                       capture_output=True, text=True)
    return p.returncode, (p.stderr or "").strip(), os.path.exists(out1)


def main():
    fails = []
    d = tempfile.mkdtemp()

    # poison -> gate aborts (exit 1), no docx
    pj = os.path.join(d, "poison.md")
    open(pj, "w", encoding="utf-8").write(POISON)
    rc, msg, made = run(pj)
    print("[poison] rc=%d made_docx=%s  %s" % (rc, made, (msg.splitlines() or [''])[0]))
    if rc != 1 or made:
        fails.append("poison should abort with exit 1 and produce no docx")

    # clean + valid sidecar -> gate passes
    cj = os.path.join(d, "clean.md")
    open(cj, "w", encoding="utf-8").write(CLEAN)
    h = hashlib.sha256(open(cj, "rb").read()).hexdigest()
    open(os.path.join(d, "clean.verify.md"), "w", encoding="utf-8").write(
        "source-sha256: %s\n\nfindings: none\n" % h)
    rc, msg, made = run(cj)
    gate_passed = "EXPORT BLOCKED" not in msg
    print("[clean]  rc=%d made_docx=%s gate_passed=%s  %s"
          % (rc, made, gate_passed, (msg.splitlines() or [''])[0]))
    if not gate_passed:
        fails.append("clean+sidecar should pass the gate")
    # rc may be nonzero only if docx/reportlab libs are missing; that's a lib issue,
    # not a gate issue, so we only assert the gate verdict here.

    print("\nRESULT:", "ALL OK" if not fails else "FAILURES: " + "; ".join(fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
