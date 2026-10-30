---
name: bridge-problems
description: Build a "bridge" study set for a course topic that takes the student from zero (or lecture level) up to homework/exam level, with a short theory primer per block, leveled problems, hints, code-verified worked solutions, a time-aware study plan ranked by what past exams actually ask, and tablet-ready PDFs. Use when the student asks for practice problems, bridge problems, extra problems, build-up questions, help catching up on lectures, or help getting ready for a test or midterm, or says homework/test questions feel like a big jump from the lecture examples.
---

# Bridge problems

The problem this solves: lecture examples are one step, while homework and test questions are multi-step, and the jump kills confidence. Students are also often behind on lectures. A bridge set fixes both. For each topic block it gives a **short theory primer** ("Learn it"), then a **ladder of small problems** from lecture level to test level, so every skill the real question needs has been learned, practised alone, then combined.

People learn by reps, not lectures. The primer is the minimum theory needed to start the ladder, not a textbook chapter. For first contact with a topic, prefer the `teach-sections` skill (live, one idea at a time) and use the set for reps and reference.

## 0. Inputs (ask only what you can't infer)
- **Course and target.** Read the course's `CLAUDE.md` if there is one (dates, where the student is, notes on the instructor). Target = the next test or assignment.
- **Time budget.** Ask how many hours they have before the target if they haven't said. Everything downstream is ranked against it.
- **Source material**, read in this order of value:
  1. **Past tests** (with solutions if they exist): the best predictor.
  2. Assignments and their solutions (graded work shows what the instructor cares about).
  3. The course outline and announcements (coverage, format, aid-sheet rules).
  4. The lecture notes for the covered sections. Extract text with `pypdf` and read the exact pages, so problems and primers use the **instructor's notation**. Handwritten tablet notes saved as vector ink have no text layer: render them with `scripts/render_ink.py` and read the images.
  If something isn't on disk, ask the student to download it from the course site. Never ask for their password.

## 1. Pattern scan → priorities
- Build a **question-type × source table** (rows: question types; columns: each past test/assignment), e.g. "entropy + Huffman ✓✓✓, channel capacity ✓✓, stationarity checks ✓✓✓". Note how recent each type is: recent tests matter more.
- No past tests? Rank by assignment coverage + outline emphasis + lecture time spent, and say the ranking is a guess.
- Turn the table into **blocks** (one per question type or tight topic cluster) and tag each **Must / Should / Skip-if-short**, using frequency × recency × marks per hour of study. Show the student the table. It also tells them what *not* to study.

## 2. Each block: "Learn it" primer → ladder
**Learn it** (in a box at the top of the block; skippable if they've done the lecture):
1. **Big idea** in 2–4 plain-English sentences: what it is and why anyone cares. A concrete analogy where it helps (use the student's interests if you know them).
2. **The formulas**, each with symbols defined and the notes page.
3. **One fully worked example**, written the way a full-marks test answer looks.
4. **Traps:** the 2–3 mistakes that cost marks (e.g. "dB inside the log", "check the mean too").
5. **Recipe:** numbered steps for this question type.

**Ladder**, about 2 problems per level, fewer for small blocks:
- **L1 Warm-up:** one step, numbers given, lecture-example level.
- **L2 Combine:** two steps chained, or one twist (a tie, a non-power-of-2, a negative answer that's right).
- **L3 Transfer:** set it up yourself, or the same skill in a new context.
- **L4 Test-style:** length, wording and multi-part format of the real test questions.

**Every problem:** level tag, skill trained, notes page, a **hint** (a nudge, not the method), and a **full worked solution** (why this method, each step, units, a sanity check: limiting case, bounds, Kraft sum, dimensions, probabilities sum to 1).

**Never reproduce graded work.** No actual assigned or past-test questions, and no trivially renumbered copies. Bridge problems train the same skill on a different setup, so past tests stay fresh as real timed benchmarks. (Worked solutions *for* past tests that have no official key are fine, as a separate file for the student's own use.)

## 3. Verify every number with code
Write `<course>/practice/verify_NN_<topic>.py`: compute every answer, `assert` identities that must hold, and check expectations independently (numerical integration or simulation, not the same algebra as the solution). Markov chains, queues and reliability models: solve numerically **and** check with a quick Monte Carlo. Have the script also confirm each answer appears in the HTML page, so the page and the code can't drift apart. Run it and fix mismatches. **Never ship an unverified answer.** Use the course's language when the course requires one; otherwise Python.

## 4. Study plan (top of the set)
Split by the time budget, e.g. "Tonight (1 h) / Tomorrow (2 h)" or "Day 1…Day 5":
- Per block: primer → notes pages (exact page numbers) → ladder → the homework/past-test questions it unlocks.
- **Skip rule:** both L2s right without hints ⇒ jump to L4.
- Must blocks first. Name what to skip if time runs short.
- End with a **past test under a timer, then mark it**, and a last "redo what you missed" slot. Leave the night before for sleep, not new material.

## 5. Output
- `<course>/practice/NN-<topic>.html`: one self-contained page per set. Start from `templates/bridge-template.html` (styles, Learn-it box, problem cards, collapsed hints and solutions, light/dark). **Offline:** no CDNs, no external fonts; math in Unicode/HTML.
- PDFs for a tablet, via `scripts/print_pdf.py <html> <pdf> problems|solutions|asis`:
  - `NN-<topic> - PROBLEMS.pdf` (no hints or solutions; they write on it)
  - `NN-<topic> - SOLUTIONS.pdf` (everything expanded)
  Check the page counts it prints, and look at at least one PDF before shipping.
- Only when the student will be offline (travel, commute): a pack folder + zip (`<course>/<name>-pack/`) with `0 - START HERE.txt` holding the plan in plain text.
- If the course has a `CLAUDE.md`, add a line to its notes: set name, what it covers, and the pattern-scan summary.
- If the test allows an aid sheet, offer the **`aid-sheet`** skill at the end.

## 6. Using the set with the student
Match the help they ask for: "stuck" ⇒ a hint for the next step only; "walk me through it" ⇒ full steps. When they finish, ask which problems felt hard and offer a short follow-up set on just those skills. If they're short on time, re-rank the remaining blocks instead of adding more.
