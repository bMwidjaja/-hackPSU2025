import json

# Example JSON data
json_data = {
    "name": "John Doe",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "zip": "10001"
    },
    "scores": [85, 92, 78],
    "contact": {
        "email": "john@example.com",
        "phone": "555-0123"
    }
}

# Different ways to access JSON data:

# 1. Access top-level fields using dictionary syntax
print("1. Basic field access:")
print(f"Name: {json_data['name']}")
print(f"Age: {json_data['age']}")

# 2. Access nested fields using multiple dictionary keys
print("\n2. Nested field access:")
print(f"Street: {json_data['address']['street']}")
print(f"City: {json_data['address']['city']}")

# 3. Access array elements using index
print("\n3. Array access:")
print(f"First score: {json_data['scores'][0]}")
print(f"Second score: {json_data['scores'][1]}")

# 4. Using get() method (safer, returns None if key doesn't exist)
print("\n4. Using get() method:")
print(f"Name: {json_data.get('name')}")
print(f"Non-existent field: {json_data.get('nonexistent')}")

# 5. Accessing nested data with multiple levels
print("\n5. Deep nested access:")
print(f"Email: {json_data['contact']['email']}")

# 6. Checking if a key exists
print("\n6. Checking key existence:")
if 'name' in json_data:
    print("Name exists in the JSON")
if 'nonexistent' not in json_data:
    print("'nonexistent' is not in the JSON")

# 7. Iterating over JSON data
print("\n7. Iterating over JSON:")
for key, value in json_data.items():
    print(f"{key}: {value}")

# 8. Accessing nested arrays
print("\n8. Accessing nested arrays:")
for score in json_data['scores']:
    print(f"Score: {score}") 