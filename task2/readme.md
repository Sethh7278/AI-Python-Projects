
## Task Aim
For task 2 I am going to use the AI prompt to turn a user input into a python object with fields.

## Example

Here is a working example:
Please enter a description for the holiday you would like to go on containing the length in days,
the month you would like to go in and the budget: 

    I would like to go away for 12 days in March on a budget of £1000
Returns:
days=12 month='March' budget=1000
<class '__main__.TripRequest'>

## How it works
1. User describes their trip in plain English
2. OpenAI's structured outputs extract the details into a schema
3. Pydantic validates the result (e.g. days must be positive)

## What I learned
1. I learned how to use pydantic classes for data validation and structure.
2. Parsing using OpenAI client
3. Passing a format for the response to be in using text_format.


## Test findings
| Input | Expected | Got | Verdict |
|---|---|---|---|
| No budget given | `budget=None` | `days=12, month='February', budget=None` | Optional works |
| Trip length given in months | Months converted to days | `days=60, month='January', budget=2000` | Converted correctly (slower response) |
| Month given as "Frog" | Month is `None` or rejected | `days=11, month='Frog', budget=400` |  `str` accepts any text |
| Budget given in lira | Currency flagged or converted to GBP | `days=10, month='April', budget=225` | Number extracted, but currency lost and treated as £ |
| No number of days given | `days=None` or user asked | `days=5, month='March', budget=500` | Invents days, varies between runs, seems based on budget |

**Summary:** 2 passed, 1 partial, 2 failed.
## Limitations
1. The system doesn't know the current date.
2. The system doesn't know the currency making the system very unaccurate.
3. Does not pick a destination different destinations need a different budget.
## Next
estimate trip cost from my own price data.