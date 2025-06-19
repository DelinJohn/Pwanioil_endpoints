import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env", override=True)



def get_config():
    try:
        return {
            "KEY": os.getenv("OPENAI_API_KEY"),
            "model_provider": os.getenv("GPT_model_provider"),
            "model": os.getenv("GPT_model"),
            "MONGO_URI": os.getenv("uri")
        }
    except KeyError as e:
        
        raise KeyError(f"Missing Streamlit Secret:{e}")
    
 
