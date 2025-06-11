from Output_structure import real_time_text_generator,real_time_image_generator,real_time_image_text_generator
from typing import Optional
from fastapi import FastAPI
from typing import Dict, Any
from fastapi.responses import StreamingResponse,JSONResponse
from pydantic import BaseModel
import json
from data_loaders import json_data_fetcher
from utils.logger import setup_logger
import time


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
    time:float






@app.post('/text')
def text_output(input_data:TextInputData):

    try:
        duration = time.time() - input_data.time
        logger.info(f"/image latency: {duration:.3f} sec")    
        


        return StreamingResponse(real_time_text_generator(input_data.text_prompt,
                                                        input_data.product_data),media_type="text/event-stream")
    except Exception as e:
        logger.error(f"Error in /text: {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Failed to generate image and text"})


class ImageInputData(BaseModel):
    image_prompt:str
    product_data: Dict[str, Any]
    image_location:str
    time:float






@app.post('/image')
def image_output(input_data:ImageInputData):
    try:    
        duration = time.time() - input_data.time
        logger.info(f"/image latency: {duration:.3f} sec")
        return StreamingResponse(real_time_image_generator(input_data.image_prompt,
                                                        input_data.product_data,
                                                        input_data.image_location),media_type="text/event-stream")
    except Exception as e:
        logger.error(f"Error in /image: {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Failed to generate text"})
    





class ImageTextData(BaseModel):
    image_prompt:str
    text_prompt:str
    product_data: Dict[str, Any]
    image_location:str
    time:float


@app.post('/image_and_text')
def image_and_text_output(input_data:ImageTextData):
    try:    
        duration = time.time() - input_data.time
        logger.info(f"/image and text latency: {duration:.3f} sec")
        logger.info(time.time()-input_data.time)
        return StreamingResponse(real_time_image_text_generator(input_data.image_prompt,
                                                            input_data.text_prompt,
                                                            input_data.product_data,
                                                            input_data.image_location,
                                                            time.time()),media_type="text/event-stream")
    except Exception as e:
        logger.error(f"Error in /image and text: {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Failed to generate text"})







        







    






        


