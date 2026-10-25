from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
#Connecting to client using client variable
client = OpenAI(
    api_key= os.environ.get("OPENAI_API_KEY")
)




def get_llm_response(userinput, context):
    return (client.responses.create(
        model="gpt-4o-mini",
        instructions="only respond to the question with the notes provided, If the notes don't cover the question, say you don't know, rather than using general knowledge. Site the source note/notes the answer came from",
        input= f"Here is the user's question {userinput} and the context you can use {context}"
    ).output_text)

def get_embedding(text):
    return client.embeddings.create(
        model=("text-embedding-3-small"),
        input=text
    ).data[0].embedding


def similarity(a, b):
    total = 0
    for x, y in zip(a, b):
        total += x * y
    return total


scooter = get_embedding("scooter")
elephant = get_embedding("elephant")
motorbike = get_embedding("motorbike")


print(similarity(scooter, motorbike))
print(similarity(scooter, elephant))

print(type(scooter))
print(type(scooter[0]))
