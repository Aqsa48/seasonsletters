#!/usr/bin/env python3
"""Create clean source and CTAN release archives. MIT License, (c) 2026 aqsa."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = '0.1.0'
CTAN = ['README.md','preview.png','LICENSE','CHANGELOG.md','MANIFEST.md','VALIDATION.md',
        'seasonalletters.sty','seasonalletter.cls',
        'seasonalletters-doc.tex','seasonalletters-doc.pdf',
        'seasonalletters-gallery.tex','seasonalletters-gallery.pdf',
        'seasonalletters-example.tex','seasonalletters-example.pdf',
        'seasonalletters-print.tex','seasonalletters-print.pdf',
        'seasonalletters-standard.tex','seasonalletters-standard.pdf']

def main():
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    for name in CTAN:
        if not (ROOT / name).is_file():
            raise SystemExit('Missing release file: ' + name)
    source = [p for p in ROOT.rglob('*') if p.is_file()
              and not set(p.relative_to(ROOT).parts) &
              {'.git','build','dist','__pycache__'}]
    manifest = {}
    for kind, paths in [('ctan',[ROOT / n for n in CTAN]),('source',source)]:
        archive = dist / ('seasonalletters-' + VERSION + '-' + kind + '.zip')
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
            for p in sorted(paths):
                rel = p.relative_to(ROOT).as_posix()
                info = zipfile.ZipInfo('seasonalletters/' + rel, (2026,11,5,0,0,0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                z.writestr(info, p.read_bytes())
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            assert all(n.startswith('seasonalletters/') for n in z.namelist())
            assert not any(n.endswith(('.aux','.log','.toc','.out','.xdv','.exe')) for n in z.namelist())
        manifest[archive.name] = {'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
                                 'files':len(paths),'bytes':archive.stat().st_size}
    (dist / 'SHA256SUMS').write_text(''.join(v['sha256']+'  '+k+'\n' for k,v in manifest.items()), encoding='utf-8')
    print(json.dumps(manifest, indent=2))

if __name__ == '__main__':
    main()
