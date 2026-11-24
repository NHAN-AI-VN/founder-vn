# Review checklist

Applies to every change that touches `skills/` or `examples/` (design §5). The machine half is
`python3 scripts/skill_lint.py`; the reviewer checks the rest by reading.

- [ ] No `$`: every amount is VND in Vietnamese format (`35.000 đ`), and no `$` sits next to a digit.
- [ ] No English leaks into Owner-facing output (reports, `examples/`, the simulated-buyer brief);
      the Owner is addressed as "anh/chị".
      Accepted as proper names, not leaks: the tool's verdict labels printed as is
      ("Profitable (có lãi)", "Not yet (chưa lãi)", "Incomplete (chưa đủ số)"), book and
      framework names ("100M Offers"), the board lens names (Offers, Product, Systems) and
      competitor names. The automated check is a stoplist of English function words; a reviewer
      still reads the prose.
- [ ] Every legal or numeric claim carries an official link and a verification date.
- [ ] The disclaimer is present: not financial, tax or legal advice.
- [ ] The simulated-panel caveat is present wherever a panel result is shown:
      "mô phỏng, cận trên, không phải khách hàng thật".

Also checked by `skill_lint.py`: frontmatter has `name` (equal to the folder), `description` with
Vietnamese trigger phrases, `license`, and `metadata.version` equal to the package version. The
shared protocol block of [skill-conventions.md](skill-conventions.md) is present.
