# Review closure ledger — #7 installer (`founder-vn install --host`) and host pages
S1 FIXED — the operator answered (reviews/issue-7/operator-answer.md) and commit 68a9c1d wrote the installer exception into docs/agents/standards.md; code unchanged, it already stays inside install.SKILL_FOLDERS and refuses escapes.
S2 FIXED — red-by-mutation table added to docs/evidence/issue-7-installer.md (commit "docs(evidence): #7 red-by-mutation table"); each CLI test was seen red against a mutated install.py or cli.py, then reverted.
S3 FIXED — the public --skills-dir flag is removed from the CLI (commit "fix(install): drop the public --skills-dir flag"); tests keep the install.run(skills_dir=...) seam and patch install.packaged_skills_dir for CLI runs.
