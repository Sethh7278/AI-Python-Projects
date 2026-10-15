from pydantic import BaseModel, PositiveInt
#Importing APIS
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
#Connecting to client using client variable
client = OpenAI(
    api_key= os.environ.get("OPENAI_API_KEY")
)

# Creating the class for a trip request
class TripRequest(BaseModel):
    days: PositiveInt 
    month: str 
    budget: PositiveInt | None


def print_llm_response(userinput):
    print (client.responses.create(
        model="gpt-4o-mini",
        instructions="Simple response bot",
        input= userinput
    ).output_text)

#Parse response
def parse_llm_response(userinput):
    return (client.responses.parse(
        model="gpt-4o-mini",
        instructions="Extract the information and add it to the format",
        input= userinput,
        text_format=TripRequest
    ).output_parsed)
    

prompt = input("""Please enter a description for the holiday you would like to go on containing the length in days,
the month you would like to go in and the budget: \n""")

response = parse_llm_response(prompt)

print(response)

print(type(response))