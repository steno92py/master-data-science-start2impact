"""Verifica i file pubblicati rispetto agli hash delle consegne recuperate."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    catalog = json.loads((ROOT / 'docs/catalogo_progetti.json').read_text())
    checked = 0
    failures = []
    for item in catalog:
        expected = item.get('artifact_sha256')
        if not expected:
            continue
        path = ROOT / item['artifact_path']
        if not path.is_file():
            failures.append(f"Manca: {item['artifact_path']}")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            failures.append(f"Hash diverso: {item['artifact_path']}")
        else:
            checked += 1
    print(json.dumps({'verified_artifacts': checked, 'errors': failures}, indent=2))
    return bool(failures)


if __name__ == '__main__':
    raise SystemExit(main())
