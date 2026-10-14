#Importing APIS
import os
from openai import OpenAI

#Connecting to client using client variable
client = OpenAI(
    api_key= os.environ.get("OPENAI_API_KEY")
)

# Building response
get_llm_response = client.responses.create(
    model="gpt-4o-mini",
    instructions="Test bot",
    input ="Test 1"
)

#Making sure output is text
print(get_llm_response.output_text)