from pathlib import Path
from openai import OpenAI, APIError
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




def get_embedding(text):
    return client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    ).data[0].embedding

def embed_notes(notes):
    embedded_notes = {}
    for name, text in notes.items():
        embedded_notes[name] = get_embedding(text)

    return embedded_notes


def similarity(a, b):
    total = 0
    for x, y in zip(a, b):
        total += x * y
    return total




def get_llm_response(userinput, context):
    return (client.responses.create(
        model="gpt-4o-mini",
        instructions="only respond to the question with the notes provided, If the notes don't cover the question, say your notes dont cover that, rather than using general knowledge. Cite the source note/notes the answer came from",
        input= f"Notes:\n{context}\nQuestion:\n{userinput}"
    ).output_text)


def embedding_search(question, note_embeddings):
    results = []
    embedded_question = get_embedding(question)
    for name, embeddings in note_embeddings.items():
        score = similarity(embeddings, embedded_question)
        results.append((score, name))
    return sorted(results, reverse=True)[:3]



def answer_question(question, notes, embedded_notes):
    top_notes = embedding_search(question, embedded_notes)
    context = ""
    for score, name in top_notes:
        if score > 0.25:
            text = notes[name]
            context += f"Source: {name} \n{text}\n\n"
    if context == "":
        return "My notes don't cover that"
    else:
        return get_llm_response(question, context)




notes = load_notes("notes")

try: 
    note_embeddings = embed_notes(notes)
    question = (input("What would you like to ask our travel support robot?: "))

    if question.strip() == "":
        print("please ask a valid question")
    else:
        print(answer_question(question, notes, note_embeddings))

except APIError:
    print("Sorry we are having an issue with the API")
    


