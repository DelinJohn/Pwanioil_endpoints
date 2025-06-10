
import json


def json_data_fetcher(product_loction:str):
    """
    Splits the campaign JSON into four parts:
    - output_type: string
    - image_prompt: from 'image_instructions'
    - text_prompt: from 'text_instructions'
    - rest_data: all other keys excluding the above
    
    """
    with open(f"data_bases/{product_loction}", "r", encoding="utf-8") as f:
        payload= json.load(f)
    output_type = payload.get("output_type")
    image_prompt = payload.get("image_instructions")
    text_prompt = payload.get("text_instructions")

    # Create rest_data by excluding the above three keys
    product_info = {
        key: value
        for key, value in payload.items()
        if key not in {"output_type", "image_instructions", "text_instructions"}
    }

    return output_type, image_prompt, text_prompt, product_info