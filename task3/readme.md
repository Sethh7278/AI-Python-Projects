# Trip Cost Estimator

## How it works
1. The user describes their trip in plain English.
2. OpenAI's structured outputs extract the details (style, days, month, budget) into a validated `TripRequest` object.
3. `load_costs()` reads `costs.csv` with `csv.DictReader` into a dictionary of daily prices for each accommodation style.
4. `estimate_cost()` adds up the daily costs for the chosen style and multiplies by the number of days.
5. `budget_check()` compares the estimate with the budget, and reports how much is left or how far over budget the trip is.

Prices come from my own data, never from the AI. The AI only handles the messy language, and Python does the maths.

## Example
User enters "I want to go on holiday for 14 days in march on a budget of 820 pounds and I plan on using hostels"

The system responds "Your trip is in budget by £568 costing a total of £252"

## How it works
1. AI extracts trip details (style, days, budget) into a validated `TripRequest`
2. Prices are looked up from `costs.csv`, my own data
3. Python calculates the total and checks it against the budget

## What I learned
1. I learned how to convert data from a CSV file into a python dictionary.
2. Using pydantic classes to store user inputs 
3. "I like pizza" becoming a trip is because the system has to give an output due to the schema forcing the model to invent values. This means the schema decides what the AI can say.

## Test findings
| Input | Expected | Got | Verdict |
|---|---|---|---|
| "10 days in a hostel in March, budget £500" | £180, in budget by £320 | Your trip is in budget by £320 costing a total of £180 | works as expected |
| "2 weeks in a hotel in January with £800" | £980, over budget by £180 | Your trip goes over budget by £180 costing a total of £980 | works as expected converts weeks to days|
| "7 days at a guesthouse in May, £245 budget" | £245, in budget by £0 | Your trip is in budget by £0 costing a total of £245 | working as expected, could add a specific on budget message.|
| "5 days in a guesthouse in April" | £175, no budget message | No budget given, Estimated cost: £175 | Works as expected |
| "a week staying in dorms in June, about 200 quid" | hostel, £126, in budget by £74 | Your trip is in budget by £74 costing a total of £126 | Works even with slang |
| "10 days in February with a £300 budget" | defaults to hostel: £180, in budget by £120 | Your trip is in budget by £74 costing a total of £126 | Automatically goes to hostels |
| "I like pizza" | sorry message |No budget given, Estimated cost: £175 | Gives an estimate does not work |
| "a week in hostels then a week in a hotel" | will assume hostel | No budget given, Estimated cost: £126 | assumed hostel does not know how to switch|

**Summary:**
Passes all simple test cases when giving all the needed information.
Fails when information is not given.
Needs error handling

## Limitations
1. prices are rought estimates.
2. prices do not change based on month taking into account high season, low season etc.
3. budget is not exclusively set in gbp or any currency which could cause a lot of pricing issues.

## How to run
```bash
cd rung3
python main.py
```