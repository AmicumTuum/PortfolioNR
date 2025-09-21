import json

with open('five.json') as file:
    data = json.load(file)

age_filter = 25
filtered_data_by_age = [x for x in data if x['age'] == age_filter]

city_filter = "Saratov"
filtered_data_by_city = [x for x in data if x["city"] == city_filter]

print("Filtered by age:")
print(json.dumps(filtered_data_by_age, indent=4))

print("Filtered by city:")
print(json.dumps(filtered_data_by_city, indent=4))