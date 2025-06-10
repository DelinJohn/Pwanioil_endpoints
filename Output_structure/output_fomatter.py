from llm import Text_llm,image_llm
from utils import base64_to_image
import json
import asyncio


async def real_time_text_generator(text_prompt,product_data):
    history = []
    for i in range(3):
        result = await Text_llm(text_prompt,product_data, history)
        history.append(result)
        yield json.dumps({"text": result}) + "\n"
        await asyncio.sleep(1)
        

        
        

async def real_time_image_generator(image_prompt,product_data,image_location):
    history = []
    
    for i in range(3):
        result, prompt = await image_llm(image_prompt,product_data,image_location, history)
        history.append(prompt)
        yield json.dumps({"image": result})+ "\n"

        
        

async def real_time_image_text_generator(image_prompt,text_prompt,product_data,image_location):
    text_history = []
    prompt_history = []
    

    for i in range(3):
        async with asyncio.TaskGroup() as tg:
            # Create tasks concurrently
            text_task = tg.create_task(
                Text_llm(text_prompt,product_data, text_history)
            )
            image_task = tg.create_task(
                image_llm(image_prompt,product_data, image_location,prompt_history)
            )

            

        # After exiting the task group, both tasks are done.
        text_result =  text_task.result()
        image_result,prompt =  image_task.result()

        text_history.append(text_result)
        prompt_history.append(prompt)
        yield json.dumps({"text": text_result, "image": image_result})+ "\n"

       
        
