from pymongo import MongoClient
from config import get_config





def Mongodb_insert(collection,Values):
    try:
        config=get_config()
        uri=config['MONGO_URI']
        mongo_client=MongoClient(uri)
        db=mongo_client['Pwani_llm_Output']
        db[collection].insert_one(Values)
    except Exception as e:
        raise Exception(f"Error with the Mongo insertion{e}")    
