# Claude Study Skills

Three [Claude Code](https://claude.com/claude-code) skills that turn an AI agent into an exam-prep coach. They fix the gap students hit in technical courses: **lecture examples are one step, but homework and test questions are five**.

**Built by:** James Markham, for my own Master of Engineering courses. I used them to get ready for real midterms (digital communications, and computer systems modeling: Markov chains, reliability, queues).

| Skill | What it does |
|---|---|
| [`bridge-problems`](skills/bridge-problems/SKILL.md) | Reads past tests, assignments and notes, ranks what the exam actually asks, then builds a **ladder of problems** from lecture level (L1) to test level (L4) for each topic, with a short theory primer, hints, worked solutions and a time-boxed study plan. **Every answer is checked by code** before you see it. Outputs an offline web page plus tablet-ready PDFs. |
| [`teach-sections`](skills/teach-sections/SKILL.md) | Teaches a topic **live in chat, one idea at a time**: why it matters → the idea → a tiny example → one check question, then waits. Fixes only the step you got wrong. Then runs the ladder problems one by one. |
| [`aid-sheet`](skills/aid-sheet/SKILL.md) | Builds an allowed formula sheet that contains **only what past tests and assignments use**, in numbered, color-banded sections that fit exactly one double-sided page. |

## See an example
[`examples/01-binomial-poisson/`](examples/01-binomial-poisson/) is a complete bridge set for a fictional intro-probability course (all problems original, with baseball-flavoured examples):
- `01-binomial-poisson.html`: open it in a browser. A pattern table of what the "past tests" ask, a 2-hour study plan, two blocks each with a Learn-it primer and an L1→L4 ladder, collapsible hints and solutions, light and dark mode.
- `… - PROBLEMS.pdf` (a clean worksheet to write on) and `… - SOLUTIONS.pdf` (hints and worked solutions).
- `verify_01_binomial_poisson.py`: computes all 20 answers, cross-checks each one with an independent method (direct summation or a seeded Monte Carlo simulation), and confirms every answer string appears in the page, so the page and the math can't drift apart.

```text
$ python verify_01_binomial_poisson.py
check                                                    exact     page  simulated
A1 P(exactly 2 hits in 4), p=.300                       0.2646   0.2646     0.2645
A4 P(at least 3 strikes in 5), p=.62                    0.7165   0.7165     0.7164
B4a exact binomial P(X≤1), n=250, p=.01                 0.2858   0.2858     0.2869
...
All 20 answers verified and found in the page.
```

## How the bridge skill works
1. **Pattern scan.** A question type × past-test table, so you study what gets asked, weighted by how often, how recently and how many marks per hour of study. Each topic block is tagged *Must*, *Should* or *Skip-if-short*.
2. **Learn it, then climb.** Each block opens with the minimum theory (big idea, formulas in the instructor's notation, one full-marks worked example, common traps, a step-by-step recipe), then about 8 problems: L1 one step → L2 two steps or a twist → L3 set it up yourself → L4 test-style. **Skip rule:** both L2s right without hints → jump to L4.
3. **Never reproduce graded work.** Problems train the same skills on new setups, so the real past tests stay fresh for a timed final run.
4. **Verify with code.** A script recomputes every number and checks it a second, independent way (simulation, numerical integration, identities like "probabilities sum to 1").
5. **Ship for real study conditions.** Offline HTML (no CDNs), a problems PDF to write on, a solutions PDF, and an offline pack only when you'll be travelling.

The lesson that shaped `teach-sections`: a polished study page wasn't what got me ready. What worked was being taught one small idea at a time, answering a question, and having only the broken step fixed. The pages and PDFs are for reps and reference.

## Install
Copy the skill folders into a project's `.claude/skills/` (or `~/.claude/skills/` to use them everywhere):
```bash
cp -r skills/* /path/to/your/course-folder/.claude/skills/
```
Then in Claude Code, from your course folder: *"Make me bridge problems for next week's midterm, I have 6 hours"*, *"teach me block C"* or *"build my formula sheet"*.

**Needs:** Python 3.10+ with `pypdf` (and `Pillow` for `render_ink.py`, which renders handwritten tablet notes that have no text layer). PDF printing uses headless **Microsoft Edge or Google Chrome/Chromium**: `python skills/bridge-problems/scripts/print_pdf.py page.html out.pdf problems|solutions|asis`.

## Layout
```
skills/bridge-problems/   SKILL.md, templates/bridge-template.html, scripts/print_pdf.py, scripts/render_ink.py
skills/teach-sections/    SKILL.md
skills/aid-sheet/         SKILL.md, templates/aid-sheet-template.html
examples/01-binomial-poisson/   sample set: HTML, PDFs, verify script
```
