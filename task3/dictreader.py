import csv

def load_costs(path):
    costs = {}
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            costs[row ["style"]] = {
                "accommodation_per_night" : int(row["accommodation_per_night"]),
                "food_per_day" : int(row["food_per_day"]),
                "transport_per_day" : int(row["transport_per_day"])
            }
    return costs

print(load_costs("costs.csv"))