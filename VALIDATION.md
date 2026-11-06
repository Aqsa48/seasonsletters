# Release validation

Version 0.1.0, checked on 2026-11-05.

## Checks actually run locally

Engine: Tectonic 0.17.0 (XeTeX backend), Windows. Its downloaded bundle reports
LaTeX2e 2021-11-15 patch level 1, exercising the package against an older
format than current TeX distributions. The compiler ZIP was verified against
the SHA-256 digest published in the upstream GitHub release metadata.

The build script completed with a zero exit status.

- Nine valid documents compiled: manual, gallery, two-page example, print
  example, standard-letter example, artwork, natural-flow, lifecycle and matrix.
- All 28 season/weekday combinations compiled on A5 paper.
- Three invalid inputs were rejected with the expected errors: unknown key,
  zero rule spacing, and unknown named theme.
- Per-letter page counts, local theme restoration, disabled pages, and light,
  full and absent continuation decoration matched the recorded lifecycle.
- The natural-flow test produced three pages and retained its final signature.
- Custom background and corner images plus a custom TikZ layer compiled.
  PDF image-draw counts confirmed that print mode omits the background image.
- PDF page counts and paper sizes were checked: A4, A5 and US Letter.
- Extracted body-word boundaries in the gallery, letter and print example
  stayed within the intended horizontal writing area.
- No overfull boxes were reported in successful final builds.

## Visual review

Poppler rendered all six manual pages, all seven gallery designs, both pages
of the letter, the print example, the standard-letter example, and all three
natural-flow pages. These were inspected for clipping, overlap, readability,
page numbering and continuation behaviour. The preview image is composed
from the actual gallery renders.

## GitHub Actions

The full build and verification suite passed with pdfLaTeX, XeLaTeX, and
LuaLaTeX on Linux. See the [successful workflow run](https://github.com/Aqsa48/seasonsletters/actions/runs/42068058256).
Physical printer testing and tagged PDF validation remain outside these checks.

## Name and publication status

An exact CTAN package-JSON lookup returned HTTP 404 on 2026-11-05, and a
GitHub repository-name search returned no matching repository. These checks do
not reserve the name or establish novelty. CTAN remains responsible for its
acceptance and catalogue naming decisions.

The source is published at https://github.com/Aqsa48/seasonsletters.
No CTAN submission has been sent. The submission metadata is in CTAN-SUBMISSION.md.
