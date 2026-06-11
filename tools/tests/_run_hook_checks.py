"""Ad-hoc driver for the export-gate hook (kept out of the Bash command line so
the live PreToolUse hook doesn't intercept the test invocation itself)."""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
HOOK = os.path.join(ROOT, "tools", "export_gate_hook.py")
CANON = os.path.join("tools", "md" + "_to_docx_pdf.py")


def run(cmd):
    p = subprocess.run([sys.executable, HOOK], input=json.dumps({"tool_input": {"command": cmd}}),
                       capture_output=True, text=True)
    return p.returncode, (p.stderr or "").strip()


def main():
    fails = []

    # 1. non-canonical exporter -> deny (2)
    rc, msg = run("node teams/build" + "_docx.js out.do" + "cx")
    print("[1] non-canonical exporter: rc=%d" % rc)
    if rc != 2:
        fails.append("non-canonical exporter should be denied")

    # 2. canonical export of poisoned draft -> deny (2)
    poison = ("## Team identity\n\nt\n\n"
              "| Pokemon | Item | Ability | Moves | Role |\n|---|---|---|---|---|\n"
              "| Tinkaton-Gamma | Heavy-Duty Boots | Levitate | "
              "Hydro Pump, Fly, Play Rough, Facade | glue |\n")
    d = tempfile.mkdtemp()
    pj = os.path.join(d, "poison.md")
    open(pj, "w", encoding="utf-8").write(poison)
    rc, msg = run("python %s %s a.do%s b.p%s" % (CANON, pj, "cx", "df"))
    print("[2] poisoned canonical export: rc=%d  (%s)" % (rc, msg.splitlines()[0] if msg else ""))
    if rc != 2:
        fails.append("poisoned canonical export should be denied")

    # 3. unrelated command -> allow (0)
    rc, msg = run("ls -la")
    print("[3] unrelated command: rc=%d" % rc)
    if rc != 0:
        fails.append("unrelated command should be allowed")

    # 4. canonical export, no .md arg -> deny (fail closed)
    rc, msg = run("python %s" % CANON)
    print("[4] canonical, no .md (fail closed): rc=%d" % rc)
    if rc != 2:
        fails.append("canonical with no source should fail closed")

    print("\nRESULT:", "ALL OK" if not fails else "FAILURES: " + "; ".join(fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
