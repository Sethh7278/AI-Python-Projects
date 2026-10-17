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




def estimate_cost(trip, costs):
    style = trip.style
    prices = costs[style]
    price_per_day = sum(prices.values())
    days = trip.days
    overall_cost = price_per_day * days
    return overall_cost

def budget_check(trip, cost):
    budget = trip.budget
    if budget is None:
        return f"No budget given, Estimated cost: £{cost}"
    elif budget >= cost:
        in_budget = True
        difference = budget - cost
    else:
        in_budget = False
        difference = cost - budget
    if in_budget == True:
        return f"Your trip is in budget by £{difference}"
    else:
        return f"Your trip goes over budget by £{difference}"


costs = load_costs("costs.csv")

prompt = input("""Please enter a description for the holiday you would like to go on containing the length in days, type of travel (hostel, hotel, guesthouse)
    the month you would like to go in and the budget: \n""")

trip = parse_llm_response(prompt)
if trip is None:
    print("Sorry, I couldn't understand that trip. Try describing it again.")
else:
        cost = estimate_cost(trip, costs)
        print(budget_check(trip, cost))
        print(trip)

