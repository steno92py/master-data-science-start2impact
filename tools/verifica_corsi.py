"""Verifica l'indice dei corsi, le collocazioni uniche e gli elaborati originali."""
import hashlib
import json
from pathlib import Path

from verifica_archivio import candidate_paths

ROOT = Path(__file__).resolve().parents[1]


def main():
    courses = json.loads((ROOT / 'docs/indice_corsi.json').read_text())
    projects = json.loads((ROOT / 'docs/catalogo_progetti.json').read_text())
    selected = set(candidate_paths())
    errors = []
    course_by_slug = {course['slug']: course for course in courses}
    project_by_slug = {project['slug']: project for project in projects}
    if len(course_by_slug) != len(courses):
        errors.append('Slug di corso duplicati')
    if len(project_by_slug) != len(projects):
        errors.append('Slug di elaborato duplicati')
    folders = [course['folder'] for course in courses if course['folder']]
    if len(folders) != len(set(folders)):
        errors.append('La stessa cartella è assegnata a corsi distinti')
    approved = 0
    for course in courses:
        expected_projects = {p['slug'] for p in projects if p['course_slug'] == course['slug']}
        if set(course['projects']) != expected_projects or len(course['projects']) != len(expected_projects):
            errors.append(f"Elaborati non coerenti nell'indice: {course['slug']}")
        if bool(course['folder']) != bool(expected_projects):
            errors.append(f"Cartella senza elaborati o elaborati senza cartella: {course['slug']}")
        if course['folder'] and not (ROOT / course['folder'] / 'README.md').is_file():
            errors.append(f"README del corso mancante: {course['folder']}")
        if course['folder'] and course['folder'] + '/README.md' not in selected:
            errors.append(f"README del corso escluso dalla pubblicazione: {course['folder']}")
    for project in projects:
        slug = project['slug']
        course = course_by_slug.get(project['course_slug'])
        if not course:
            errors.append(f'Corso non censito: {slug}')
            continue
        if project['course_folder'] != course['folder']:
            errors.append(f'Collocazione del corso incoerente: {slug}')
        if project['official_course_url'] != course['official_course_url']:
            errors.append(f'Pagina ufficiale incoerente: {slug}')
        for field in ['folder', 'artifact_path']:
            path = (ROOT / project[field]).resolve()
            if not path.is_relative_to((ROOT / course['folder']).resolve()):
                errors.append(f'Percorso esterno al corso: {slug}, {field}')
        path = ROOT / project['artifact_path']
        if project['artifact_path'] not in selected:
            errors.append(f'Elaborato escluso dalla pubblicazione: {slug}')
        if not path.is_file():
            errors.append(f"Elaborato mancante: {project['artifact_path']}")
            continue
        expected = project.get('artifact_sha256')
        if project.get('status') == 'Superato' and not expected:
            errors.append(f'Hash della consegna approvata mancante: {slug}')
        if expected:
            if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                errors.append(f'Hash diverso: {slug}')
            else:
                approved += 1
    physical = {name.split('/')[0] for name in selected
                if '/' in name and name[:2].isdigit()}
    if physical != set(folders):
        errors.append(f'Cartelle di corso non coerenti con indice: {sorted(physical ^ set(folders))}')
    print(json.dumps({'courses': len(courses), 'course_folders': len(folders),
                      'activities_without_local_projects': len(courses) - len(folders),
                      'projects': len(projects), 'verified_artifacts': approved,
                      'errors': errors}, ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
