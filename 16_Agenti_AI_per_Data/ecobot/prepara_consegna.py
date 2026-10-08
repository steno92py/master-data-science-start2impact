"""Prepara EcoBot; la chiave locale richiede l'opzione esplicita di consegna."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT.parent / 'consegna/pacchetto_riservato'
PATTERNS = ['*.py', '*.md', '*.txt', '*.ipynb', '.env.example', '.gitignore',
            'streamlit_screenshot.png', 'data/*.csv', 'data/manifest.json',
            'tests/*.py', 'evidenze/*.json', 'evidenze/*.xml', 'evidenze/*.html',
            'evidenze/*.txt', 'grafici/*.png']
SUBMISSION_FILES = ['agent.ipynb', 'requirements.txt', 'streamlit_screenshot.png',
                    'data/solar_production_raw.csv', 'data/household_consumption.csv',
                    'data/manifest.json', 'evidenze/prove_api_reali.json']


def build(include_local_api_key=False):
    files = {}
    if include_local_api_key:
        for name in SUBMISSION_FILES:
            files[name] = (ROOT / name).read_bytes()
        files['README.md'] = (ROOT / 'materiali_consegna/README.md').read_bytes()
    else:
        for pattern in PATTERNS:
            for path in ROOT.glob(pattern):
                if path.is_file():
                    files[path.relative_to(ROOT).as_posix()] = path.read_bytes()
    # Il comportamento predefinito non legge mai la credenziale locale.
    files['.env'] = b'OPENAI_API_KEY=\nOPENAI_MODEL=gpt-4.1-mini\nLANGSMITH_TRACING=false\n'
    if include_local_api_key:
        from dotenv import dotenv_values
        config = dotenv_values(ROOT / '.env', interpolate=False)
        key = config.get('OPENAI_API_KEY')
        if not key or not key.strip() or any(c in key for c in '\r\n\x00'):
            raise ValueError('OPENAI_API_KEY locale assente o non valida; archivio non creato.')
        model = config.get('OPENAI_MODEL') or 'gpt-4.1-mini'
        if any(c in model for c in '\r\n\x00'):
            raise ValueError('OPENAI_MODEL locale non valido; archivio non creato.')
        def quote(value):
            return "'" + value.replace('\\', '\\\\').replace("'", "\\'") + "'"
        files['.env'] = (f'OPENAI_API_KEY={quote(key)}\n'
                         f'OPENAI_MODEL={quote(model)}\nLANGSMITH_TRACING=false\n').encode()
        if any(key.encode() in content for name, content in files.items() if name != '.env'):
            raise ValueError('Credenziale presente fuori da .env; archivio non creato.')
    revision = json.loads((ROOT / 'evidenze/revisione_2026-10-08.json').read_text())
    pending = list(revision['pending'])
    if not include_local_api_key:
        pending.append('Configurazione API del valutatore; .env dello ZIP senza chiave')
    if 'streamlit_screenshot.png' not in files:
        pending.append('Screenshot di una vera interazione Streamlit')
    required = {'agent.ipynb', '.env', 'requirements.txt', 'README.md', 'streamlit_screenshot.png'}
    if include_local_api_key and (pending or not required.issubset(files)):
        raise ValueError('Requisiti di consegna incompleti; archivio finale non creato.')
    state = {
        'status': 'PRONTO_ALLA_CONSEGNA' if include_local_api_key else 'NON_PRONTO_ALLA_CONSEGNA',
        'revision_date': '2026-10-08',
        'pending': pending,
        'contains_api_key': include_local_api_key,
        'distribution': 'Consegna riservata al valutatore' if include_local_api_key else 'Versione senza credenziale',
        'files': {name: hashlib.sha256(content).hexdigest() for name, content in sorted(files.items())},
    }
    if not include_local_api_key:
        files['STATO_CONSEGNA.json'] = json.dumps(state, ensure_ascii=False, indent=2).encode()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    filename = ('StefanoNocco_AgentiAIData.zip' if include_local_api_key
                else 'StefanoNocco_AgentiAIData_REVISIONATO_DA_VALIDARE.zip')
    destination = OUTPUT / filename
    with tempfile.NamedTemporaryFile(dir=OUTPUT, prefix='.ecobot-', suffix='.zip', delete=False) as handle:
        temporary = Path(handle.name)  # Creato con permessi 0600, anche durante la scrittura.
    try:
        with ZipFile(temporary, 'w', ZIP_DEFLATED) as archive:
            for name, content in sorted(files.items()):
                archive.writestr(name, content)
        with ZipFile(temporary) as archive:
            assert archive.testzip() is None
            for name, content in files.items():
                assert archive.read(name) == content
            assert {'agent.ipynb', '.env', 'requirements.txt', 'README.md'}.issubset(archive.namelist())
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    manifest = {'path': str(destination), 'sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
                'files': len(files), 'status': state['status'], 'pending': state['pending'],
                'contains_api_key': include_local_api_key,
                'file_sha256': state['files']}
    manifest_name = ('manifest_ecobot_consegna_2026-10-08.json' if include_local_api_key
                     else 'manifest_ecobot_revisione_2026-10-08.json')
    (OUTPUT / manifest_name).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--include-local-api-key', action='store_true',
                        help='Include la chiave locale nel solo .env dello ZIP finale riservato.')
    args = parser.parse_args()
    print(json.dumps(build(args.include_local_api_key), ensure_ascii=False, indent=2))
