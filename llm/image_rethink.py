from typing import TypedDict
from langchain_core.messages import HumanMessage, SystemMessage
from data_loaders import product_data_fetcher
from llm.model_loader import load_llm
from config import get_config
import asyncio
from openai import AsyncOpenAI
import time
import aiofiles
from utils.logger import setup_logger 


from pathlib import Path
import json



logger=setup_logger('image_generation_rethink')

config=get_config()
key=config['KEY']
client = AsyncOpenAI(api_key=key)
llm=load_llm()    





async def  image_llm_new(image_prompt,product_info,image_location):
    try:

       
        path=image_location
        image_path = Path(path)
        async with aiofiles.open(image_path, "rb") as f:
            image_bytes = await f.read()

        
        product_details = await product_data_fetcher("USHINDI","LAUNDRY BAR")
        # competitor_list = competitor_data_collector(product, competitors, category)
        # location_data, gender_data, locality_data = demographics_data_fetcher(gender, region, urban_or_rural)
       
        messages = [
    SystemMessage("""
ROLE: You are a top-tier advertising strategist specialized in crafting culturally grounded, emotionally compelling visual prompts for image generation tools.

OBJECTIVE: Generate high-impact, brand-aligned image prompts that reflect authentic product usage scenarios and resonate with the target demographic. The prompts must be optimized for the visual and emotional tone of the target platform.

TONE: Culturally authentic, emotionally resonant, visually clear, and aligned with digital platform trends.
"""),

    HumanMessage(f"""
CAMPAIGN BRIEF:
- Product: {product_info.get('product')}
- Category: {product_info.get('category')}, SKU: {product_info.get('sku')}
- Platform: {product_info.get('platform')} | Channel: {product_info.get('channel')}
- Campaign Type: {product_info.get('campaign_type')} | Category: {product_info.get('campaign_category')}
- Tone: {product_info.get('tone')}

AUDIENCE INSIGHTS:
- Region: {product_info['demographics'].get('region')}
- Age Range: {product_info['demographics'].get('age_range')}
- Gender: {', '.join(product_info['demographics'].get('gender', []))}
- Income Level: {product_info['demographics'].get('income')}
- Urban/Rural: {product_info['demographics'].get('urban_or_rural')}

PRODUCT DETAILS:
{product_details}

TASK:
Create one imaginative and visually striking image prompt that adheres to the following:

✅ CORE REQUIREMENTS:
- The product must be shown in a **realistic and culturally accurate usage scenario**.
  - E.g., laundry soap should appear in actual washing contexts: backyard wash areas, water taps, washing lines — **not in irrelevant places like living rooms or rooftops**.
- Reflect the creative instruction: **{image_prompt}**
- Include **authentic emotional cues** (e.g., pride in cleanliness, joy in daily life, family care).
- Emphasize that the **product itself must not be visually altered** — retain its original appearance.
- Ensure the visual concept is suitable for **{product_info.get('platform')}** trends and aesthetics.

🚫 AVOID:
- Illogical or trendy scenes disconnected from actual product use.
- Generic backdrops (e.g., empty streets, plain rooms) that don’t support the product narrative.
- Overly complicated or abstract imagery.

🎨 VISUAL STYLE GUIDELINES:
- Be concise and visual in your description.
- Use culturally resonant symbols, environments, and emotions.
- Favor clarity and storytelling over detail overload.
- Ensure every visual element supports the product’s purpose and message.

Make sure the image prompt helps users immediately understand **what the product is, how it’s used, and why it matters**, through a meaningful, emotionally resonant visual story.
""")
]
        logger.info(f"input_forPromptgenrerator:{messages}")
        class CampaignResponse(TypedDict):
            prompt_1: str
            prompt_2: str
            prompt_3: str

        
        structured_llm=llm.with_structured_output(CampaignResponse)
        prompt= await  structured_llm.ainvoke(messages)
        logger.info(prompt)

        start_time=time.time()

        async with asyncio.TaskGroup() as tg:
            image1=tg.create_task(client.images.edit(
            model="gpt-image-1",  
            image=("input_image.png", image_bytes),
            prompt=prompt['prompt_1'],
            size="1536x1024"
        ))
            image2=tg.create_task(client.images.edit(
            model="gpt-image-1",  
            image=("input_image.png", image_bytes),
            prompt=prompt['prompt_2'],
            size="1536x1024"
        ))
            image3=tg.create_task(client.images.edit(
            model="gpt-image-1",  
            image=("input_image.png", image_bytes),
            prompt=prompt['prompt_3'],
            size="1536x1024"
        ))
            
        result1=image1.result()
        result2=image2.result()
        result3=image3.result()

        duration = time.time() - start_time
        logger.info(f"/image model only: {duration:.3f} sec")    

        return {"result1":result1.data[0].b64_json,"result2":result2.data[0].b64_json,"result3":result3.data[0].b64_json}



        
      
    
    except Exception as e:

        logger.error(f"Image generation failed: {str(e)}", exc_info=True)
        raise 
        
