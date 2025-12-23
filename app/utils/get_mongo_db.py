from settings import settings

import json

if __name__ == "__main__":
    # Get the database object
    dbname = settings.get_database()
    
    if dbname is not None:
        # You can now use the dbname object to interact with collections and data
        print(f"Database object: {dbname}")
        collection = dbname['movies']

        print(collection)

        with open("movies_data.json", 'r') as file:
            data = json.load(file)
            collection.insert_many(data)
        
        file.close()