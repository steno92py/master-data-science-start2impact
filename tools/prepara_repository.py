"""Esporta la selezione pubblicabile in una nuova cartella, senza eliminare file."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path, help='Cartella nuova o vuota')
    args = parser.parse_args()
    destination = args.destination.resolve()
    if destination.exists() and any(destination.iterdir()):
        parser.error('La destinazione deve essere vuota: nessun file viene sovrascritto.')
    with tempfile.TemporaryDirectory(prefix='s2i-export-') as tmp:
        report = Path(tmp) / 'selection.json'
        subprocess.run([sys.executable, str(ROOT / 'tools/verifica_archivio.py'),
                        '--output', str(report)], check=True)
        paths = json.loads(report.read_text())['paths']
    destination.mkdir(parents=True, exist_ok=True)
    for rel in paths:
        source = ROOT / rel
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        if hashlib.sha256(source.read_bytes()).digest() != hashlib.sha256(target.read_bytes()).digest():
            raise RuntimeError(f'Copia non identica: {rel}')
    print(json.dumps({'copied_files': len(paths), 'destination': str(destination)}))


if __name__ == '__main__':
    main()
