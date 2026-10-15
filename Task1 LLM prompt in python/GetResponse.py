#Importing APIS
import os
from openai import OpenAI

#Connecting to client using client variable
client = OpenAI(
    api_key= os.environ.get("OPENAI_API_KEY")
)

# # Building response
# response = client.responses.create(
#     model="gpt-4o-mini",
#     instructions="Test bot",
#     input ="Test 1"
# )

def print_llm_response(userinput):
    print (client.responses.create(
        model="gpt-3.5-turbo",
        instructions="Test bot that states the prompt",
        input= userinput
    ).output_text)
    
    

#Making sure output is text
print_llm_response("Test function")