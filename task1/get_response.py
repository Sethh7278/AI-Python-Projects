#Importing APIS
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
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
        model="gpt-4o-mini",
        instructions="Simple response bot",
        input= userinput
    ).output_text)


user_prompt = input("Please enter the prompt you would like to ask: ")    

#Making sure output is text
print_llm_response(user_prompt)