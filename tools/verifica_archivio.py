"""Controlla la selezione Git senza modificare il repository o inviare dati."""
from pathlib import Path
import argparse
import json
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
LIMIT = 50 * 1024 * 1024
PATTERNS = {
    'openai_key': re.compile(rb'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{25,}'),
    'telegram_token': re.compile(rb'\b[0-9]{8,12}:[A-Za-z0-9_-]{30,50}\b'),
    'aws_access_key': re.compile(rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    'private_key': re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'github_token': re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})'),
    'google_api_key': re.compile(rb'\bAIza[0-9A-Za-z_-]{30,}'),
    'huggingface_token': re.compile(rb'\bhf_[A-Za-z0-9]{30,}'),
    'airtable_token': re.compile(rb'\bpat[A-Za-z0-9]{14}\.[A-Za-z0-9]{50,}'),
}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='s2i-git-check-') as tmp:
        gitdir = Path(tmp)/'repo.git'
        subprocess.run(['git','init','--bare','-q',str(gitdir)],check=True)
        cmd = ['git','-c','core.excludesFile=/dev/null',f'--git-dir={gitdir}',
               f'--work-tree={ROOT}','ls-files','--others','--exclude-standard','-z']
        paths = [p for p in subprocess.check_output(cmd,cwd=ROOT).decode().split('\0') if p]
    large=[];secrets=[];forbidden=[];total=0
    for rel in paths:
        p=ROOT/rel
        if not p.is_file():continue
        size=p.stat().st_size;total+=size
        if size>LIMIT:large.append({'path':rel,'bytes':size})
        archive_guide = rel in {'98_ARCHIVIO_ORIGINALI/README.md',
                               '98_ARCHIVIO_ORIGINALI/SOLO_COPIA_STORICA.txt'}
        if (p.name.startswith('.env') and p.name!='.env.example') or any(
            part in {'config_locale','node_modules','.venv','feedback_riservato'} for part in p.parts) or (
            '98_ARCHIVIO_ORIGINALI' in p.parts and not archive_guide):
            forbidden.append(rel)
        if p.suffix.lower() in {'.pdf','.png','.jpg','.jpeg','.xlsx','.twbx','.gif'}:continue
        data=p.read_bytes()
        for kind,pattern in PATTERNS.items():
            if pattern.search(data):secrets.append({'path':rel,'type':kind})
    result={'candidate_files':len(paths),'candidate_bytes':total,'large_files':large,
            'credential_patterns':secrets,'forbidden_paths':forbidden,
            'network_calls':False,'remote_repository_created_by_check':False,
            'paths':paths}
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='paths'},ensure_ascii=False,indent=2))
    return bool(large or secrets or forbidden)

if __name__=='__main__':raise SystemExit(main())
