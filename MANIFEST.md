# File manifest

## Runtime
- seasonalletters.sty: package and original TikZ motifs
- seasonalletter.cls: optional personal-letter document class

## Documentation
- seasonalletters-doc.tex and .pdf: manual and its editable source
- preview.png: overview image rendered from the gallery documentation
- README.md: overview, installation, dependencies, contact and licence
- LICENSE: MIT licence
- CHANGELOG.md: version history
- MANIFEST.md: this inventory

## Documented examples
Each example has a .tex source and a compiled .pdf supplied as documentation.
- seasonalletters-example: first and continuation pages (A4)
- seasonalletters-gallery: seven season/day combinations (A5)
- seasonalletters-print: white-paper output (US Letter)
- seasonalletters-standard: standard letter-class integration (A4)

## Repository development files (not required at runtime)
- tools/build.py: engine builds, regression checks and PDF checks
- tools/package.py: clean source and CTAN ZIP creation
- tests/: matrix, pagination, state, image and invalid-input fixtures
- .github/workflows/compile.yml: three-engine CI configuration
- .gitignore: excludes generated build intermediates
- VALIDATION.md: actual local verification results
- CTAN-UPLOAD-GUIDE.md: step-by-step submission guide
- CTAN-SUBMISSION.md: proposed submission fields and release status

The CTAN archive contains runtime files, documentation and documented examples.
The source archive additionally contains development files. Neither includes
TeX binaries, caches, machine-specific paths, or build intermediates.
