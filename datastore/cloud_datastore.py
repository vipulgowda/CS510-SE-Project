from google.cloud import datastore
import uuid
import os
from dotenv import load_dotenv

def from_datastore(entity):
    """Translates Datastore results into the format expected by the
    application.

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]
    """
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()
    entity['id'] = entity.key.id
    return [entity['bill_type'],entity['vendor_name'],entity['date'], entity['time'],entity['total_amount'], entity['city'], entity['state'], entity['id']]

class Model():
    def __init__(self):
        load_dotenv() 
        self.client = datastore.Client(os.getenv('DATASTORE_PROJECT_ID'))

    def select(self):
        query = self.client.query(kind = os.getenv('DATASTORE_KIND'))
        query.order = ['-date']
        entities = list(map(from_datastore,query.fetch()))
        return entities

    def insert(self, bill_type, vendor_name, date, time, total_amount, city, state):
        key = self.client.key(os.getenv('DATASTORE_KIND'))
        rev = datastore.Entity(key)
        rev.update({
            'id': str(uuid.uuid4()),
            'bill_type' : bill_type,
            'vendor_name' : vendor_name,
            'date' : date,
            'time': time,
            'total_amount' : total_amount,
            'city': city,
            'state': state
            })
        self.client.put(rev)
        return True
    
    def update(self, id, updated_data):
        key = self.client.key(os.getenv('DATASTORE_KIND'), int(id))
        entity = self.client.get(key)
        
        if not entity:
            print("Entity not found")
            return False
        
        # Update the entity with new values
        for field, value in updated_data.items():
            entity[field] = value
        
        try:
            # Save the updated entity
            self.client.put(entity)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    
    def delete(self, id):
        key = self.client.key(os.getenv('DATASTORE_KIND'), id)
        try:
            self.client.delete(key)
            print("Successfully deleted entity with ID:", key)
            return True
        except Exception as e:
            print("Failed to delete entity:", e)
            return False

# Create an instance of the Model class
model_instance = Model()