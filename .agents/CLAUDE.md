# Miscellaneous Notes
In any given directory, AGENTS.md may be a symlink to CLAUDE.md (or vice-versa).
This is by design so that both files contain the same content.
If tasked with updating one of these files, just edit one of them and expect the other to stay in sync by virtue of the symlink.

# Next steps
1) Run `find .` (or equivalent) to orient yourself to the project structure
2) Read the README.md and pyproject.toml
3) Find unimplemented features (and bugs) and create an implementation (and fix) plan in .agents/PLAN.md
4) Any architectural or security concerns that arise during development should be documented in .agents/REVIEW.md
5) Create a TODO list for the first phase of development in .agents/TODO-001.md
