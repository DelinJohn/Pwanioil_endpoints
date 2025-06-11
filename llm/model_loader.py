import os
from config import get_config
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
load_dotenv()






        

async def load_llm():

    try:
        config=get_config()


        key=config["KEY"]
        model_provider=config["model_provider"]
        model_name=config['model']
        os.environ["API_KEY"] = key
        
        return init_chat_model(model_name, model_provider=model_provider)
    
    except KeyError as ke:
        raise KeyError(f"Missing key in config: {ke}") from ke

    except Exception as e:
        raise RuntimeError(f"Unexpected error while loading LLM: {e}") from e
    


    



