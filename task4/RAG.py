from pathlib import Path

# Loading the files from the notes folder and putting them into a dictionary
def load_notes(folder):
    notes = {}
    for path in Path(folder).glob("*.md"):
        notes[path.stem] = (path.read_text(encoding="utf-8"))
    return notes

notes = load_notes("notes")

# print(len(notes))
# print(notes.keys())



# Searching through the notes for specific words from the given question
def keyword_search(question , notes):
    results = []
    words = set(question.lower().split())
    for name, text in notes.items():
        score = 0
        for word in words:
            if word in text.lower():
                score +=1
        results.append((score,name))
    return(sorted(results, reverse=True)[:3])


print(keyword_search("How much does a scooter cost", notes))