from langchain_core.messages import HumanMessage, SystemMessage
from data_loaders import product_data_fetcher
from llm.model_loader import load_llm
from utils.logger import setup_logger

import time


logger=setup_logger('text_generation')




async def Text_llm(text_prompt,product_data,history,in_time):
    try:
        logger.info("started text generation")
        llm=await load_llm()
        
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
- **Follow briefing instructions exactly**: {text_prompt}
- **Output should be of type**: {product_data.get('content_type')}  
- **Language**: {product_data.get('language')}  
- **Tone**: {product_data.get('tone')}  
- **Platform-optimized**: Aligned with trends effective on **{product_data.get('platform')}**
- **Cultural relevance**: Use local references, humor, or trends that resonate with the target audience.
- **Unique selling proposition**: Highlight what makes Pwani’s product stand out.
- **Call to action**: Encourage immediate engagement or purchase.
- **Brand voice**: Reflect Pwani’s identity and values.
- **Avoid jargon**: Use clear, relatable language.

CONTENT FORMAT:
- **Output must be between 20–30 words max.**

- **This is the history of the conversation**:  
  {history if history else 'No prior campaigns — this is the first iteration.'}

- **Output must follow this format:**

    **Header:**  
    [A catchy, campaign-relevant headline]  

    **Caption:**  
    [A persuasive line with key product benefits, branding and relevance to target audience]  

    **{product_data.get('content_type')}**  
    [If content_type = "hashtag", generate campaign hashtags. If script, give ad-style script. No hashtags unless required.]
""")]


        result = await llm.ainvoke(messages)
        duration = time.time() - in_time
        logger.info(f"/image latency: {duration:.3f} sec")    
        
        return result.content
    

    except Exception as e:
        logger.error(f"Error with producing the output for text generation module{str(e)}")
        raise 