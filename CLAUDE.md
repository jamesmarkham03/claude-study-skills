# Claude Study Skills

The global `CLAUDE.md` in `OS/` still applies.

## What this is
Public portfolio repo (github.com/jamesmarkham03/claude-study-skills): generic versions of the `bridge-problems`, `teach-sections` and `aid-sheet` skills James uses in `School/.claude/skills/`, plus one original sample set.

## Rules
- **No real course material, ever:** no lecture notes, past tests, assignments, instructor names or course codes. Examples must be original problems on a fictional course.
- The working copies live in `School/.claude/skills/` and may hold school-specific details. When a skill improves there, port the generic part here by hand (don't copy course details).
- Every number in `examples/` must be checked by its `verify_*.py`, which also checks that the page shows it. Re-run it and reprint the PDFs after any edit.

## Commands
- `python examples/01-binomial-poisson/verify_01_binomial_poisson.py`
- `python skills/bridge-problems/scripts/print_pdf.py <html> <pdf> problems|solutions|asis`
