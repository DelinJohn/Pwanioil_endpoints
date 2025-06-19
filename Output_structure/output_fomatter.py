from llm import Text_llm,image_llm
import json
import asyncio
from utils.logger import setup_logger 

import time


logger=setup_logger('Output_fomatter')


async def real_time_text_generator(text_prompt,product_data,in_time):

    try:
        history = []
        for i in range(3):
            result = await Text_llm(text_prompt,product_data, history,time.time())
            history.append(result)
            yield json.dumps({"text": result}) + "\n"
        duration = time.time() - in_time
        logger.info(f"/image iterator: {duration:.3f} sec")     
    except Exception as e:
        logger.error(f'Real time text generator have malfunctioned{e}')
        raise       
        
        

        
        

async def real_time_image_generator(image_prompt,product_data,image_location,in_time):
    try:
        history = []
        
        for i in range(3):
            result, prompt = await image_llm(image_prompt,product_data,image_location, history,time.time())
            history.append(prompt)
            yield json.dumps({"image": result})+ "\n"
        duration = time.time() - in_time
        logger.info(f"/image iterator: {duration:.3f} sec") 
    except Exception as e:
        logger.error(f'Real time image generator have malfunctioned{e}')
        raise    

        
        

async def real_time_image_text_generator(image_prompt,text_prompt,product_data,image_location,in_time):
    try:
        text_history = []
        prompt_history = []

        

        for i in range(3):
            async with asyncio.TaskGroup() as tg:
                # Create tasks concurrently
                image_task = tg.create_task(
                    image_llm(image_prompt,product_data,image_location,prompt_history,time.time())
                )
                text_task = tg.create_task(

                    Text_llm(text_prompt,product_data, text_history,time.time())
                )
                

                
            # After exiting the task group, both tasks are done.
            text_result =  text_task.result()
            image_result,prompt =  image_task.result()

            text_history.append(text_result)
            prompt_history.append(prompt)
            
        
            yield json.dumps({"text": text_result, "image": image_result})+ "\n"
        duration = time.time() - in_time
        logger.info(f"/image iterator: {duration:.3f} sec")        

    except Exception as e:
        logger.error(f'Real time image and text generator have malfunctioned{e}')
        raise     
