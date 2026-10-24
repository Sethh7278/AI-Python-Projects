from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
#Connecting to client using client variable
client = OpenAI(
    api_key= os.environ.get("OPENAI_API_KEY")
)


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


def get_llm_response(userinput, context):
    return (client.responses.create(
        model="gpt-4o-mini",
        instructions="only respond to the question with the notes provided, If the notes don't cover the question, say you don't know, rather than using general knowledge. Site the source note/notes the answer came from",
        input= f"Here is the user's question {userinput} and the context you can use {context}"
    ).output_text)


def answer_question(question, notes):
    keywords = keyword_search(question, notes)
    context = ""
    for score, name in keywords:
        if score > 0:
            source = name
            text = notes[source]
            context += f"Source: {source} \n Text: {text}"

        else:
            continue
    return get_llm_response(question, context)

question = str(input("What would you like to ask our travel support robot?: "))

print(answer_question(question, notes))