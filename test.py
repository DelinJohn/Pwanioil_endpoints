

import streamlit as st
import httpx
import asyncio
import nest_asyncio
from io import BytesIO
import base64
from datetime import datetime
import time


nest_asyncio.apply()






import json


def json_data_fetcher(product_loction:str):
    """
    Splits the campaign JSON into four parts:
    - output_type: string
    - image_prompt: from 'image_instructions'
    - text_prompt: from 'text_instructions'
    - rest_data: all other keys excluding the above
    
    """
    with open(f"{product_loction}", "r", encoding="utf-8") as f:
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




def base64_to_image(img):
    image_data = base64.b64decode(img)
    image = BytesIO(image_data)
    return image



async def main(json_location,image_location):
    output_type, image_prompt, text_prompt, product_data = json_data_fetcher(json_location)
    if image_location is None:
            st.error("it is absent")
            st.stop()
    
    start_time = datetime.now()

    if output_type == "text":
        
        json_payload = {
            "text_prompt": text_prompt,
            "product_data": product_data
           
        }
        async with httpx.AsyncClient(timeout=300.0) as client:
            result= await client.post( "http://127.0.0.1:8000/text_new", json=json_payload)
            result=result.json()
            st.write(result['output_1'])
            
            st.write(result['output_2'])
   
            st.write(result['output_3'])
           
                        



    if output_type=="image":
        if "text_results" not in st.session_state:
                    st.session_state.text_results = []
        
        json_payload={
        "image_prompt":image_prompt,
        "product_data":product_data,
        "image_location":image_location
       
        }
        st.write("Payload being sent:")
        
        async with httpx.AsyncClient(timeout=300.0) as client:
            result= await client.post( "http://127.0.0.1:8000/image_new", json=json_payload)
            result=result.json()
            st.image(base64_to_image(result["result1"]))
            st.image(base64_to_image(result["result2"]))
            st.image(base64_to_image(result["result3"]))
            




    if output_type=="text_and_image":
        json_payload={
        "image_prompt":image_prompt,
        "text_prompt":text_prompt,
        "product_data":product_data,
        "image_location":image_location
        }
       
        async with httpx.AsyncClient(timeout=300.0) as client:
            result= await client.post( "http://127.0.0.1:8000/image_and_text_new", json=json_payload)
            result=result.json()
            st.write(result['text']['output_1'])
            st.image(base64_to_image(result['image_result']["result1"]))
            st.write(result['text']['output_2'])
            st.image(base64_to_image(result['image_result']["result2"]))
            st.write(result['text']['output_3'])
            st.image(base64_to_image(result['image_result']["result3"]))



        
                
                        
    
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds() / 60  # in minutes
    st.success(f"✅ Total time taken: {elapsed:.2f} minutes")                    
                        
                        

                    
st.title("AI Content Generator")

json_location = st.text_input("Enter JSON location path")
image_location = st.text_input("Enter image location path")



# Initialize output

if st.button("Generate"):
    

    # Run the async logic
    asyncio.run(main(json_location, image_location))





