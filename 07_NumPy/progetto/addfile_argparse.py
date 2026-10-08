# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 21:11:03 2025

@author: Steno

addfile.py: tool per spostare file dalla cartella 'files' e aggiornare recap.csv.

Sfrutta argparse per accettare uno o più nomi di file da riga di comando; se nessun file viene passato, entra in modalità interattiva.
All'avvio cerco automaticamente la cartella 'files', preparo recap.csv e carico le voci esistenti.
Per ogni file specificato (o digitato interattivamente) lo sposto nella sottocartella corretta, mostro le informazioni e registro l'entry solo se nuova.
"""
import argparse
import sys
from pathlib import Path
import shutil
import csv

# Mappatura delle estensioni alle cartelle di destinazione
FILE_TYPES: dict[str, list[str]] = {
    "images": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
    "audio":  [".mp3", ".wav", ".ogg", ".flac"],
    "docs":   [".txt", ".doc", ".docx", ".pdf", ".odt"]
}

LOGO = """
███████████████████████████████████████████████████████████████
█                                                             █
█ █████ █████ █     █████                                     █
█ █       █   █     █                                         █
█ ███     █   █     ███                                       █
█ █       █   █     █                                         █
█ █     █████ █████ █████                                     █
█                                                             █
█  ███  ████   ████  ███  █   █ █████ █████ █████ ████        █
█ █   █ █   █ █     █   █ ██  █   █      █  █     █   █       █
█ █   █ ████  █ ███ █████ █ █ █   █     █   ███   ████        █
█ █   █ █ █   █   █ █   █ █  ██   █    █    █     █ █         █
█  ███  █  █   ███  █   █ █   █ █████ █████ █████ █  █        █
█                                                             █
███████████████████████████████████████████████████████████████
█                                                             █
█ █████ █████ ████ █   █  ███    ████  █   █                  █ 
█ █       █   █    ██  █ █   █   █   █ █   █                  █
█ █████   █   ████ █ █ █ █   █   ████  █████                  █
█     █   █   █    █  ██ █   █   █       █                    █
█ █████   █   ████ █   █  ███  █ █       █                    █
█                                                             █
███████████████████████████████████████████████████████████████

"""

def get_category(ext: str) -> str:
    """
    Restituisce la categoria corrispondente all'estensione del file.
    Se non trova corrispondenza, ritorna 'other'.
    """
    ext = ext.lower()
    for category, exts in FILE_TYPES.items():
        if ext in exts:
            return category
    return "other"

def singularize(category: str) -> str:
    """
    Converte un nome di cartella plurale in forma singolare per la stampa.
    """
    return category[:-1] if category.endswith('s') else category

def locate_files_dir() -> Path:
    """
    Cerca ricorsivamente nei parent la cartella 'files'.
    """
    current = Path(__file__).parent.resolve()
    while True:
        candidate = current / "files"
        if candidate.exists() and candidate.is_dir():
            return candidate
        if current.parent == current:
            break
        current = current.parent
    raise FileNotFoundError(f"Directory 'files' non trovata")

def setup_recap(source_dir: Path) -> set[tuple[str, str, int]]:
    """
    Prepara recap.csv e carica le voci esistenti.
    """
    recap_path = source_dir / "recap.csv"
    if not recap_path.exists():
        with open(recap_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["name", "type", "size(B)"])
    existing: set[tuple[str, str, int]] = set()
    with open(recap_path, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            try:
                existing.add((row[0], row[1], int(row[2])))
            except Exception:
                continue
    return existing

def record_entry(source_dir: Path, entry: tuple[str, str, int]) -> None:
    """
    Aggiunge una nuova riga a recap.csv.
    """
    with open(source_dir / "recap.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list(entry))

def move_file(source_dir: Path, filename: str, existing: set[tuple[str, str, int]]) -> None:
    """
    Sposta un singolo file e aggiorna recap.csv se l'entry è nuova.
    """
    file_path = source_dir / filename
    if not file_path.is_file():
        print(f"Errore: il file '{filename}' non esiste in {source_dir}")
        return
    name = file_path.stem
    category = get_category(file_path.suffix)
    size = file_path.stat().st_size
    display_type = singularize(category)
    print(f"{name} type:{display_type} size:{size}B")
    target = source_dir / category
    target.mkdir(exist_ok=True)
    shutil.move(str(file_path), str(target / filename))
    entry = (name, category, size)
    if entry not in existing:
        record_entry(source_dir, entry)
        existing.add(entry)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sposta file da 'files' e aggiorna recap.csv"
    )
    parser.add_argument(
        'filenames', nargs='*', metavar='FILE',
        help="Un elenco di file da spostare (lascia vuoto per modalità interattiva)"
    )
    args = parser.parse_args()

    try:
        source_dir = locate_files_dir()
    except FileNotFoundError as e:
        print(f"Errore: {e}")
        sys.exit(1)
    existing = setup_recap(source_dir)

    if args.filenames:
        for fname in args.filenames:
            move_file(source_dir, fname, existing)
    else:
        print(LOGO)
        print("Modalità interattiva: digita file (es. fileprova.txt) o 'exit' per terminare.")
        while True:
            choice = input("> ").strip()
            if choice.lower() in {"exit", "quit", "q"}:
                print("Chiusura del programma.")
                break
            if choice:
                move_file(source_dir, choice, existing)

if __name__ == "__main__":
    main()
