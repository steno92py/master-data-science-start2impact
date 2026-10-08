# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 21:11:03 2025

@author: Steno


addfile.py: 

Script interattivo che sposta file dalla cartella 'files' nelle sottocartelle di competenza
e aggiorna il file recap.csv evitando duplicati.
"""
from pathlib import Path
import shutil
import csv
import sys

# Mappatura delle estensioni alle cartelle di destinazione\
FILE_TYPES: dict[str, list[str]] = {
    "image": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
    "audio":  [".mp3", ".wav", ".ogg", ".flac"],
    "docs":   [".txt", ".odt", ".doc", ".docx", ".pdf"]
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

def locate_files_dir() -> Path:
    """
    Cerca ricorsivamente nei parent directories la cartella 'files'.
    Ritorna il Path se trovato, altrimenti solleva FileNotFoundError.
    """
    current = Path(__file__).parent.resolve()
    while True:
        candidate = current / "files"
        if candidate.exists() and candidate.is_dir():
            return candidate
        if current.parent == current:
            break
        current = current.parent
    raise FileNotFoundError(f"Directory 'files' non trovata nei parent di {Path(__file__)}")

def setup_recap(source_dir: Path) -> set[tuple[str, str, int]]:
    """
    Prepara il file recap.csv: crea header se serve e carica le voci esistenti.
    Ritorna un set di tuple (name, type, size) già registrate.
    """
    recap_path = source_dir / "recap.csv"
    # Creazione header se non esiste
    if not recap_path.exists():
        with open(recap_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["name", "type", "size(B)"])

    # Caricamento delle entries esistenti
    existing_entries: set[tuple[str, str, int]] = set()
    with open(recap_path, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # salto header
        for row in reader:
            try:
                name, cat, size_str = row
                existing_entries.add((name, cat, int(size_str)))
            except ValueError:
                continue
    return existing_entries

def record_entry(source_dir: Path, entry: tuple[str, str, int]) -> None:
    """
    Aggiunge una nuova riga al file recap.csv.
    """
    recap_path = source_dir / "recap.csv"
    with open(recap_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list(entry))

def move_file(source_dir: Path, filename: str, existing: set[tuple[str, str, int]]) -> None:
    """
    Sposta un singolo file e aggiorna recap.csv se non è già registrato.
    """
    file_path = source_dir / filename
    if not file_path.exists() or not file_path.is_file():
        print(f"Errore: il file '{filename}' non esiste in {source_dir}")
        return

    name = file_path.stem
    category = get_category(file_path.suffix)
    size = file_path.stat().st_size
    print(f"{name} type:{category} size:{size}B")

    target_dir = source_dir / category
    target_dir.mkdir(exist_ok=True)

    dest = target_dir / filename
    shutil.move(str(file_path), str(dest))
    print(str(filename) + " è stato aggiunto alla cartella " + str(target_dir))
    entry = (name, category, size)
    if entry not in existing:
        record_entry(source_dir, entry)
        existing.add(entry)

def main() -> None:
    """
    Loop interattivo: chiede all'utente il nome del file da spostare o 'exit' per uscire.
    """
    try:
        source_dir = locate_files_dir()
    except FileNotFoundError as e:
        print(f"Errore: {e}")
        sys.exit(1)

    existing_entries = setup_recap(source_dir)

    print(LOGO)
    print("""
╔══════════════════════════════════════════════════════════════╗
║  Benvenuto in FileOrganizer interactive mode!                ║
║  Digita il nome del file da spostare (es. fileprova.txt)     ║   
║  Digita 'exit' per terminare.                                ║
╚══════════════════════════════════════════════════════════════╝
          """)

    while True:
        choice = input("> ").strip()
        if choice.lower() in {"exit", "quit", "q"}:
            print("""
╔══════════════════════════════════════════════════════════════╗
║  Uscita dal programma. Arrivederci!                          ║
╚══════════════════════════════════════════════════════════════╝
                  """)
            break
        if not choice:
            continue
        move_file(source_dir, choice, existing_entries)

if __name__ == "__main__":
    main()