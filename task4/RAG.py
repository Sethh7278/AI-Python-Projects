from pathlib import Path

# Loading the files from the notes folder and putting them into a dictionary
def load_notes(folder):
    notes = {}
    for path in Path(folder).glob("*.md"):
        notes[path.stem] = (path.read_text(encoding="utf-8"))
    return notes

notes = load_notes("notes")

print(len(notes))
print(notes.keys())