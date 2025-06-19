from Output_structure import real_time_text_generator,real_time_image_generator,real_time_image_text_generator
from llm import text_llm_new,image_llm_new
from typing import Optional
from fastapi import FastAPI
from typing import Dict, Any
from fastapi.responses import StreamingResponse,JSONResponse
from pydantic import BaseModel
import json
from data_loaders import json_data_fetcher
from utils.logger import setup_logger
import time
import asyncio
import traceback

logger=setup_logger('routes')



app=FastAPI()


@app.get('/')
async def status_report():
    return json.dumps({"Status":"Working"})


class InputData(BaseModel):
    image_location:Optional[str]
    json_location:str




@app.post('/Output')
async def complete_output(input_data:InputData):
    output_type, image_prompt, text_prompt, product_data = json_data_fetcher(input_data.json_location)

    if output_type=="text":
        return StreamingResponse(real_time_text_generator(text_prompt,product_data),media_type="text/event-stream")

    elif output_type=="image":
        return StreamingResponse(real_time_image_generator(image_prompt,product_data),media_type="text/event-stream")

    elif output_type=="text_and_image":
        return StreamingResponse(real_time_image_text_generator(image_prompt,text_prompt,product_data,input_data.image_location),media_type="text/plain")
    
    else:
        return {"error": "Invalid or missing output_type"}

    



class TextInputData(BaseModel):
    text_prompt:str
    product_data: Dict[str, Any]
    






@app.post('/text')
async def text_output(input_data:TextInputData):

    try:
        return StreamingResponse(real_time_text_generator(input_data.text_prompt,
                                                        input_data.product_data,time.time()),media_type="text/event-stream")
    except Exception as e:
        logger.error(f"Error in /text: {str(e)}")
        return JSONResponse(status_code=500, content={"error": f"Failed to generate output {str(e)}"})
    



@app.post('/text_new')
async def text_output(input_data:TextInputData):

    try:
        return JSONResponse(content=await text_llm_new(input_data.text_prompt,input_data.product_data))
    except Exception as e:
        logger.error(f"Error in /text: {str(e)}")
        return JSONResponse(status_code=500, content={"error": f"Failed to generate output {str(e)}"})    


class ImageInputData(BaseModel):
    image_prompt:str
    product_data: Dict[str, Any]
    image_location:str
    






@app.post('/image')
async def image_output(input_data:ImageInputData):
    try:    
        return StreamingResponse(real_time_image_generator(input_data.image_prompt,
                                                        input_data.product_data,
                                                        input_data.image_location,time.time()),media_type="text/event-stream")
    except Exception as e:
        logger.error(f"Error in /image: {str(e)}")
        return JSONResponse(status_code=500, content={"error":f"Failed to generate output {str(e)}"})
    




@app.post('/image_new')
async def image_output(input_data:ImageInputData):
    try:    
        return JSONResponse(content=await image_llm_new(input_data.image_prompt, input_data.product_data, input_data.image_location))
    except Exception as e:
        logger.error(f"Error in /image: {str(e)}")
        return JSONResponse(status_code=500, content={"error":f"Failed to generate output {str(e)}"})    





class ImageTextData(BaseModel):
    image_prompt:str
    text_prompt:str
    product_data: Dict[str, Any]
    image_location:str
    


@app.post('/image_and_text')
async def image_and_text_output(input_data:ImageTextData):
    try:    
        
        return StreamingResponse(real_time_image_text_generator(input_data.image_prompt,
                                                            input_data.text_prompt,
                                                            input_data.product_data,
                                                            input_data.image_location,
                                                            time.time()),media_type="text/event-stream")
    except Exception as e:
        logger.error(f"Error in /image and text: {str(e)}")
        return JSONResponse(status_code=500, content={"error": f"Failed to generate output {str(e)}"})




@app.post('/image_and_text_new')
async def image_and_text_output(input_data: ImageTextData):
    try:
        image_result = None
        text_result = None

        async with asyncio.TaskGroup() as tg:
            image_task = tg.create_task(
                image_llm_new(input_data.image_prompt, input_data.product_data, input_data.image_location)
            )
            text_task = tg.create_task(
                text_llm_new(input_data.text_prompt, input_data.product_data)
            )

        # If either task failed, .result() will raise
        try:
            image_result = image_task.result()
        except Exception as e:
            logger.error(f"❌ Image generation failed: {str(e)}")
            traceback.print_exc()
            image_result = {"error": f"Image generation failed: {str(e)}"}

        try:
            text_result = text_task.result()
        except Exception as e:
            logger.error(f"❌ Text generation failed: {str(e)}")
            traceback.print_exc()
            text_result = {"error": f"Text generation failed: {str(e)}"}

        return JSONResponse(content={
            "text": text_result,
            "image_result": image_result
        })

    except Exception as e:
        logger.error(f"🔥 UNCAUGHT ERROR in /image_and_text_new: {str(e)}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": f"Server error: {str(e)}"})


        







    






        


