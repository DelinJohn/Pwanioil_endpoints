from langchain_core.messages import HumanMessage, SystemMessage
from data_loaders import product_data_fetcher
from utils.logger import setup_logger 
from llm.model_loader import load_llm
from typing import TypedDict, List
import json
logger=setup_logger('text_generation_rethink')



import time

llm=load_llm()



async def text_llm_new(text_prompt,product_data,):
    try:
        
        
        
        product_details = await product_data_fetcher("USHINDI","LAUNDRY BAR")
        # competitor_list = competitor_data_collector(product, competitors, category)
        # location_data, gender_data, locality_data = demographics_data_fetcher(gender, region, urban_or_rural)

        messages =[ SystemMessage(f"""
ROLE:  
You are a **top-tier advertising strategist** specializing in **original, hyper-local campaigns**.

OBJECTIVE:  
Design a standout **{product_data.get('campaign_type')}** campaign for **Pwani** — promoting **{product_data.get('product')}, {product_data.get('category')}, {product_data.get('sku', 'N/A')}**.  
The campaign will target **{product_data.get('channel')}** customers via **{product_data.get('platform')}**.

PRODUCT DETAILS:
product details={product_details}

TONE & STYLE:  
The tone should be **{product_data.get('tone')}**, in line with the platform and target audience behavior.

CAMPAIGN CATEGORY:  
{product_data.get('campaign_category')}

CONTEXT:  
You will receive from the User:
- `product_details`: key benefits, unique selling points, and emotional anchors  
- `target_audience`:  
    - Region: {product_data['demographics'].get('region')}  
    - Gender: {', '.join(product_data['demographics'].get('gender', []))}  
    - Age Range: {product_data['demographics'].get('age_range')}  
    - Income Level: {product_data['demographics'].get('income')}  
    - Demographics Insights: regional, gender-specific, and locality-based behavior

IMPORTANT MUST-HAVES:

- **Output should be of type**: {product_data.get('content_type')}  
- **Language**: {product_data.get('language')}  
- **Tone**: {product_data.get('tone')}  
- **Platform-optimized**: Aligned with trends effective on **{product_data.get('platform')}**
- **Cultural relevance**: Use local references, humor, or trends that resonate with the target audience.
- **Unique selling proposition**: Highlight what makes Pwani’s product stand out.
- **Call to action**: Encourage immediate engagement or purchase.
- **Brand voice**: Reflect Pwani’s identity and values.
- **Avoid jargon**: Use clear, relatable language.
- **content_type**:{product_data.get('content_type')}






"""),
HumanMessage(text_prompt)]
        
       

        class CampaignOutput(TypedDict):
            
           
            content: str
            caption: str
            header: str

        class CampaignResponse(TypedDict):
            output_1: CampaignOutput
            output_2: CampaignOutput
            output_3: CampaignOutput

        structured_llm=llm.with_structured_output(CampaignResponse)
        result = await structured_llm.ainvoke(messages)
        logger.info(result)
        
        return result
    

    except Exception as e:
        logger.error(f"raised and exeption {str(e)}")
        return {"error":f"error in the image generation {str(e)}"}