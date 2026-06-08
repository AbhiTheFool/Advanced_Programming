products = [
    {"name": "Pen", "stock": 5},
    {"name": "Notebook", "stock": 25},
    {"name": "Pencil", "stock": 8},
    {"name": "Eraser", "stock": 3},
    {"name": "Marker", "stock": 15}
]

print("Products with stock less than 10:")

for item in products:
    if item["stock"] < 10:
        print(item["name"], "-", item["stock"])


# output 
# Products with stock less than 10:
# Pen - 5
# Pencil - 8
# Eraser - 3
