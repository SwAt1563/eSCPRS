import json

from core.config import settings
from schemas.documents import Purchase


# Method to seed the collection if it's empty
async def seed_data():

    data_path = settings.ROOT_PATH / "seeds" / "data" / "purchases.json"
  
    print("Seeding data...")
    
    # Open the JSON file and read the data
    with open(data_path, "r") as file:
        # Iterate over each line in the JSON file
        for line in file:
            # Convert each line into a dictionary
            data = json.loads(line)
            
            # Create a Purchase document for the current line
            purchase = Purchase(**data)
            
            # Insert the document into the collection
            await purchase.insert()

    print("Data seeded.")