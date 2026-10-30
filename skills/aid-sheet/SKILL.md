---
name: aid-sheet
description: Build a printable test aid sheet / formula sheet / cheat sheet for a course. It fills the allowed size (usually one double-sided letter page) with numbered, color-coded sections in a readable font, holding only the formulas that assignments and past tests actually use. Use when the student asks for an aid sheet, formula sheet, crib sheet or cheat sheet, or what to put on their allowed sheet for a test.
---

# Aid sheet

What works under exam pressure: **only what's actually used, big enough to read, sectioned so you can find things fast, no wasted space.** A first attempt that crammed everything from the notes into 7pt text and 3 columns, with half-empty columns, was hard to use. The version that worked: **2 columns, ~11pt, about 9 numbered color-banded sections, formulas only.**

## 1. Check the rules first
- Find the aid-sheet rule in the course outline and announcements: size (one side / double-sided), **handwritten or printed?**, anything banned.
- If it's unclear, say so plainly and draft a two-line email to the instructor. Default to a **formulas-only** sheet (no past-test questions or worked answers), since that's acceptable under any rule. Only make a "with past answers" version if the student asks and the rules allow it.

## 2. Decide the content (less is more)
- Source of truth: **assignments + past tests + their solutions**, then the notes for exact forms and page numbers. If `bridge-problems` already ran for this test, reuse its pattern-scan table.
- Keep a formula only if a past test, an assignment or a bridge L4 needs it. Drop chapter material that has never been examined. Say what you cut and why.
- Every formula gets a short **bold label** saying when to use it, plus the notes pages in the section header.
- Add quick-lookup tables when the test is calculator-heavy (e.g. H_b(p), log₂n, dB↔ratio). Compute every table value with code; never type them from memory.
- Include **traps** (red text) and a small **test strategy** box (question order, what to write when stuck, assumptions to state).
- Group by **question type**, numbered ①, ②, … across both sides, so the student can say "it's in ⑦". Give side 1 and side 2 each a theme in the header.

## 3. Build
- Start from `templates/aid-sheet-template.html` (letter, 7 mm margins, 2 columns, color-banded `.sec` boxes, ~11pt). Offline: no CDNs, no external fonts.
- Print with the bridge skill's script: `python ../bridge-problems/scripts/print_pdf.py <html> <pdf> asis`.
- **Fit loop:** it must be exactly the allowed number of pages (usually 2). Then look at the PDF and check for: columns clipped at the bottom, tables wider than their column (numbers running together), big empty gaps. Fix by adjusting font size (±1pt steps) or table precision. Don't shrink below ~9.5pt; cut content instead.
- Save to `<course>/tests/`: `aid-sheet-<test>.html` + `<COURSE>-<Test>-formula-sheet.pdf`.

## 4. Hand it over
Give the PDF path, a one-line map of the sections per side, and what was cut. Remind them to **print it** (and that if it must be handwritten, to copy the highest-value sections first, since copying is also review). Point out any blank space they can fill by hand with things they catch themselves looking up while practising.
