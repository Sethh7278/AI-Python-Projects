from pydantic import BaseModel, PositiveInt
#Importing APIS
import os
from openai import OpenAI
from dotenv import load_dotenv
import csv
from typing import Literal


load_dotenv()
#Connecting to client using client variable
client = OpenAI(
    api_key= os.environ.get("OPENAI_API_KEY")
)


# Creating the class for a trip request
class TripRequest(BaseModel):
    style : Literal["hostel", "hotel", "guesthouse"]
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
        instructions="Extract the information and add it to the format style being hostel, guesthouse or hotel",
        input= userinput,
        text_format=TripRequest
    ).output_parsed)
    
def load_costs(path):
    costs = {}
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            costs[row["style"]] = {
                "accommodation_per_night" : int(row["accommodation_per_night"]),
                "food_per_day" : int(row["food_per_day"]),
                "transport_per_day" : int(row["transport_per_day"])
            }
    return costs

costs = load_costs("costs.csv")


def estimate_cost(trip, costs):
    # finding out what style the user wants
    style = trip.style
    # get the price for that style
    prices = costs[style]
    price_per_day = sum(prices.values())
    #  find out amount of days user wants to go for
    days = trip.days
    # multiple daily cost by number of days
    overall_cost = price_per_day * days
    # return overall cost 
    return  overall_cost




# prompt = input("""Please enter a description for the holiday you would like to go on containing the length in days, type of travel (hostel, hotel, guesthouse)
# the month you would like to go in and the budget: \n""")

#response = parse_llm_response(prompt)
trip1 = TripRequest(days=7, month="march", budget=1000, style = "hostel")
print(estimate_cost(trip1, costs))

