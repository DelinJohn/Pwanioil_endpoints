from langchain_core.messages import HumanMessage, SystemMessage
from data_loaders import product_data_fetcher,demographics_data_fetcher
from llm.model_loader import load_llm
from config import get_config
from utils import base64_to_image
from openai import OpenAI
import logging

from pathlib import Path

import base64



llm=load_llm()

async def  image_llm(image_prompt,product_info,image_location,history):
    try:    

        image_path = Path(f"image_data/{image_location}")
        with image_path.open("rb") as f:
            image_bytes = f.read()

        
        
        
        config=get_config()
        key=config['KEY']
        
        product_details = product_data_fetcher("USHINDI","LAUNDRY BAR")
        # competitor_list = competitor_data_collector(product, competitors, category)
        # location_data, gender_data, locality_data = demographics_data_fetcher(gender, region, urban_or_rural)

        messages = [
        SystemMessage("""
ROLE: You are a top-tier advertising strategist creating culturally resonant visual prompts.
OBJECTIVE: Help generate creative image prompts for marketing campaigns.
TONE: Your output must be simple, visual, emotionally appealing, and aligned with platform-specific trends.
""")
,

    HumanMessage(f"""
CAMPAIGN DATA:
- Product: {product_info.get('product')}, Category: {product_info.get('category')}, SKU: {product_info.get('sku')}
- Product_details: {product_details}
- Platform: {product_info.get('platform')}, Channel: {product_info.get('channel')}
- Campaign Type: {product_info.get('campaign_type')}, Category: {product_info.get('campaign_category')}
- Tone: {product_info.get('tone')}
- Region: {product_info['demographics'].get('region')}
- Target Audience:
    - Age Range: {product_info['demographics'].get('age_range')}
    - Gender: {', '.join(product_info['demographics'].get('gender', []))}
    - Income Level: {product_info['demographics'].get('income')}
    - Urban/Rural: {product_info['demographics'].get('urban_or_rural')}

PROMPT INSTRUCTIONS:
{image_prompt}


HISTORY:
{history if history else 'No prior prompts.'}

REQUIREMENTS:
- The product image must **not be altered**.
- The image must be culturally relevant and optimized for **{product_info.get('platform')}** trends.
- Keep the prompt **visually imaginative** but **not overly detailed** to avoid confusing the image generation model.
- Make the image and caption concept **distinct** from past versions and aligned with the campaign direction.
""")


    ]
        logging.info(f"Image LLM:Prompt: {messages}")
        
        prompt= llm.invoke(messages).content
        logging.info(f"Image LLM Response prompt: {prompt}")

        client = OpenAI(api_key=key)
        img = client.images.edit(
            model="gpt-image-1",  
            image=("input_image.png", image_bytes),
            prompt=prompt,
            size="1536x1024"
        )

        

        return img.data[0].b64_json,prompt
    
    except Exception as e:
        raise Exception(f"An Error with image generation module {e}")
