#!/usr/bin/env python3
"""Build and verify Seasonal Letters. MIT License, copyright (c) 2026 aqsa."""
from pathlib import Path
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ['seasonalletters-doc', 'seasonalletters-gallery',
           'seasonalletters-example', 'seasonalletters-print',
           'seasonalletters-standard']

def run(engine, executable, source, dest):
    if engine == 'tectonic':
        cmd = [executable or 'tectonic', '--keep-logs', '--keep-intermediates',
               '--outdir', str(dest), '-Z', 'search-path=' + str(ROOT), str(source)]
        attempts = 1
    else:
        cmd = [executable or engine, '-interaction=nonstopmode',
               '-halt-on-error', '-file-line-error', '-output-directory',
               str(dest), str(source)]
        attempts = 2
    transcript = ''
    for _ in range(attempts):
        result = subprocess.run(cmd, cwd=ROOT, text=True, encoding='utf-8',
                                errors='replace', stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        transcript += result.stdout
        if result.returncode:
            return result.returncode, transcript
    return 0, transcript

def pdf_checks(directory):
    import pdfplumber
    from pypdf import PdfReader
    expected = {'seasonalletters-gallery': (7, 419.53, 595.28),
                'seasonalletters-example': (2, 595.28, 841.89),
                'seasonalletters-print': (1, 612, 792),
                'seasonalletters-standard': (1, 595.28, 841.89),
                'matrix': (28, 419.53, 595.28),
                'lifecycle': (7, 595.28, 841.89)}
    summary = {}
    for name, (count, width, height) in expected.items():
        reader = PdfReader(directory / (name + '.pdf'))
        assert len(reader.pages) == count, (name, len(reader.pages), count)
        for page in reader.pages:
            assert abs(float(page.mediabox.width) - width) < 1, name
            assert abs(float(page.mediabox.height) - height) < 1, name
            assert page.extract_text().strip(), (name, 'empty text')
        summary[name] = count
    # Verify body words stay within the actual class text area. Headings and
    # footer/label decorations are excluded by their y positions.
    for name in ['seasonalletters-gallery', 'seasonalletters-example',
                 'seasonalletters-print']:
        with pdfplumber.open(directory / (name + '.pdf')) as pdf:
            for page_number, page in enumerate(pdf.pages, 1):
                for word in page.extract_words():
                    if 125 <= word['top'] <= page.height - 100:
                        assert word['x0'] >= 84, (name, page_number, word)
                        assert word['x1'] <= page.width - 83, (name, page_number, word)
    flow = PdfReader(directory / 'flow.pdf')
    assert len(flow.pages) >= 3, len(flow.pages)
    assert 'End of flow test' in unicodedata.normalize('NFKC', flow.pages[-1].extract_text())
    summary['flow'] = len(flow.pages)
    artwork = PdfReader(directory / 'artwork.pdf')
    assert len(artwork.pages) == 2
    draws = [page.get_contents().get_data().count(b' Do') for page in artwork.pages]
    assert draws[0] == draws[1] + 1, ('background omission', draws)
    summary['artwork'] = 2
    # Content must survive the continuation-page transition.
    letter = PdfReader(directory / 'seasonalletters-example.pdf')
    assert 'quiet art' in letter.pages[0].extract_text().lower()
    assert 'continuation' in letter.pages[1].extract_text().lower()
    return summary

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--engine', choices=['pdflatex','xelatex','lualatex','tectonic'], default='pdflatex')
    parser.add_argument('--executable', help='Full path to engine executable')
    parser.add_argument('--outdir', type=Path)
    args = parser.parse_args()
    dest = (args.outdir or ROOT / 'build' / args.engine).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    cases = [ROOT / (name + '.tex') for name in SOURCES]
    cases += sorted((ROOT / 'tests').glob('*.tex'))
    report = {'engine': args.engine, 'success': [], 'expected_errors': []}
    for source in cases:
        code, transcript = run(args.engine, args.executable, source, dest)
        (dest / (source.stem + '.build.txt')).write_text(transcript, encoding='utf-8')
        if source.stem.startswith('invalid-'):
            expected = {'invalid-spacing': 'Spacing must be positive',
                        'invalid-theme': "Unknown theme 'missing'",
                        'invalid-option': 'Unknown option'}[source.stem]
            assert code != 0 and re.sub(r'\s+', '', expected) in re.sub(r'\s+', '', transcript), (source.name, transcript[-3000:])
            report['expected_errors'].append(source.stem)
            print('PASS expected rejection:', source.name, flush=True)
            continue
        if code:
            print(transcript, file=sys.stderr)
            raise SystemExit(code)
        log = (dest / (source.stem + '.log')).read_text(encoding='utf-8', errors='replace')
        if 'Overfull' in log:
            lines = log.splitlines()
            details = '\n'.join('\n'.join(lines[i:i+6]) for i, line in enumerate(lines) if 'Overfull' in line)
            raise AssertionError((source.name, details))
        report['success'].append(source.stem)
        print('PASS compilation:', source.name, flush=True)
    # The lifecycle test observes render decisions and per-letter page counts.
    log = (dest / 'lifecycle.log').read_text(encoding='utf-8', errors='replace')
    records = re.findall(r'SLTEST:(\d+):(spring|summer|autumn|winter):(full|light|none|disabled)', log)
    assert records == [('1','spring','full'),('2','spring','light'),
                       ('1','winter','full'),('2','winter','none'),
                       ('2','spring','disabled'),('1','spring','full'),
                       ('2','spring','full')], records
    report['pages'] = pdf_checks(dest)
    for name in SOURCES:
        shutil.copy2(dest / (name + '.pdf'), ROOT / (name + '.pdf'))
    (dest / 'verification.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
