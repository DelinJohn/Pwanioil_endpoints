from langchain_core.messages import HumanMessage, SystemMessage
from data_loaders import product_data_fetcher
from llm.model_loader import load_llm
from config import get_config
from utils import log_execution_time
from openai import AsyncOpenAI
from utils.logger import setup_logger 
import time
import aiofiles



from pathlib import Path
import json


logger=setup_logger('image_generation')




async def  image_llm(image_prompt,product_info,image_location,history,in_time):
    try:
        logger.info('Started Image geenration')
        llm=await load_llm()    
        path=image_location
        image_path = Path(path)
        async with aiofiles.open(image_path, "rb") as f:
            image_bytes = await f.read()


        
        
        
        config=get_config()
        key=config['KEY']
        
        product_details = await product_data_fetcher("USHINDI","LAUNDRY BAR")
        # competitor_list = competitor_data_collector(product, competitors, category)
        # location_data, gender_data, locality_data = demographics_data_fetcher(gender, region, urban_or_rural)
        prompt_creator_time=time.time()
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
        
        
        prompt= await  llm.ainvoke(messages)
        prompt=prompt.content
        
        duration = time.time() - prompt_creator_time
        logger.info(f"/prompt_generator_llm: {duration:.3f} sec")


        duration = time.time() - in_time
        logger.info(f"/prompt_generator complete: {duration:.3f} sec")   
        
        start_time=time.time()
        client = AsyncOpenAI(api_key=key)
        img = await client.images.edit(
            model="gpt-image-1",  
            image=("input_image.png", image_bytes),
            prompt=prompt,
            size="1536x1024"
        )
        duration = time.time() - start_time
        logger.info(f"/image model only: {duration:.3f} sec")    
        
        

        return img.data[0].b64_json,prompt
    
    except Exception as e:
        logger.error(f"Image generation failed: {str(e)}", exc_info=True)
        raise
