#!/usr/bin/env python3
"""C177: write labs/lab-NN-<slug>/README.md from the single source (course_data + data_domainN).

The Learner Guide reads these READMEs' "## Steps" back, so the prompts in the LG, the lab READMEs
and the deck always come from the same data.
"""
import glob
import importlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import course_data as C

REPO = os.environ.get("COURSE_REPO") or os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
LABS = os.path.join(REPO, "labs")


def activities():
    acts = []
    for path in sorted(glob.glob(os.path.join(HERE, "data_domain[0-9]*.py"))):
        name = os.path.basename(path)[:-3]
        if re.fullmatch(r"data_domain\d+", name):
            n = re.search(r"\d+", name).group()
            acts += getattr(importlib.import_module(name), f"DOMAIN{n}")
    return sorted(acts, key=lambda a: a["num"])


def minutes(num):
    rows = C.SCHEDULE(lambda ns: ", ".join(f"Lab {n}" for n in ns))[1][1]
    return next((m for _s, _e, m, k, t in rows if k == "lab" and f"Lab {num}" in t.split(":")[0] + t), None)


def main():
    topics = {t["num"]: t for t in C.TOPICS}
    acts = activities()
    index = [f"# Labs - {C.TITLE}", "",
             "Eight labs build one project from scratch with AI vibe coding. Each lab: read the concepts, paste the "
             "prompts into Claude Code or Codex, review the code, run the lab's check, commit.", "",
             "| Lab | Title | Time | Check |", "|---|---|---|---|"]
    for a in acts:
        slug = C.LAB_SLUGS[a["num"]]
        folder = os.path.join(LABS, f"lab-{a['num']:02d}-{slug}")
        os.makedirs(folder, exist_ok=True)
        t = topics[a["topic"]]
        mins = minutes(a["num"])
        lines = [f"# Lab {a['num']} - {a['title']}", "",
                 f"**Course:** {C.TITLE}  |  **Topic {t['code']}:** {t['title']}" + (f"  |  **Time:** {mins} min" if mins else ""), "",
                 f"**Learning outcome:** {a['objective']}.", "", a["desc"], "",
                 "## Key concepts", ""]
        lines += [f"- **{c[0]}** - {c[1]}" for c in a.get("concepts", [])]
        lines += ["", "## What you'll build", "", a["build"], "", f"**Tools:** {a['services']}", "", "## Steps", ""]
        for i, (instr, cmd) in enumerate(a["steps"], 1):
            lines.append(f"{i}. **{instr}**")
            if cmd:
                body = cmd[len("PROMPT:"):].strip() if cmd.startswith("PROMPT:") else cmd
                kind = "text" if cmd.startswith("PROMPT:") else "bash"
                if cmd.startswith("PROMPT:"):
                    lines.append("   Paste into your AI coding assistant:")
                lines += ["", f"   ```{kind}"] + [f"   {x}" for x in body.splitlines()] + ["   ```", ""]
        lines += ["## Verify", "", a["test"], "",
                  "## Reference solution", "",
                  "If you are stuck, compare with the trainer's reference project in "
                  "[`labs/solution/`](../solution/) - the same files, contracts and checks (`labs/solution/tests/`).", "",
                  "> " + C.LAB_NOTE, ""]
        open(os.path.join(folder, "README.md"), "w").write("\n".join(lines))
        index.append(f"| {a['num']} | [{a['title']}](lab-{a['num']:02d}-{slug}/README.md) | {mins} min | "
                     f"`tests/test_lab{a['num']}.py` |")
    index += ["", "## Reference solution", "",
              "[`solution/`](solution/) holds the complete working project (all eight agents, the dashboard and the "
              "acceptance checks). It runs offline: `cd labs/solution && pip install -e .[dev] && OFFLINE=true python run.py`.", "",
              "> " + C.LAB_NOTE, ""]
    open(os.path.join(LABS, "README.md"), "w").write("\n".join(index))
    print("wrote", len(acts), "lab READMEs")


if __name__ == "__main__":
    main()
