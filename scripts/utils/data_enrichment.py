import random

def generate_random_address():
    street_names = [
        "Main", "Maple", "Oak", "Pine", "Cedar", "Elm", "Washington", "Lake",
        "Hill", "Sunset", "Park", "Ridge", "Spring", "View", "First", "Second", "Third",
        "Broadway", "Highland", "Center", "Market", "River", "Grove", "Forest", "Meadow",
        "King", "Queen", "Prince", "Princess", "Lincoln", "Franklin", "Jefferson", "Jackson",
        "Adams", "Wilson", "Madison", "Grant", "Roosevelt", "Garfield", "Baker", "Church",
        "Garden", "Bay", "Harbor", "Shore", "Valley", "Vista", "Wood", "Meadow", "Creek",
        "Farm", "Field", "Court", "Parkway", "Terrace", "Circle", "Heights", "Square",
        "Mill", "Bridge", "South", "North", "East", "West"
    ]
    street_types = ["St", "Ave", "Blvd", "Ln", "Rd", "Dr", "Pl", "Ct"]

    number = random.randint(1, 999)
    street_name = random.choice(street_names)
    street_type = random.choice(street_types)

    address = f"{number} {street_name} {street_type}"
    return address