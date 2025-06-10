from Output_structure import real_time_text_generator,real_time_image_generator,real_time_image_text_generator
from typing import Optional
from fastapi import FastAPI
from typing import Dict, Any
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
from data_loaders import json_data_fetcher



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
        return StreamingResponse(real_time_image_generator(image_prompt,product_data),media_type="text/plain")

    elif output_type=="text_and_image":
        return StreamingResponse(real_time_image_text_generator(image_prompt,text_prompt,product_data,input_data.image_location),media_type="text/plain")
    
    else:
        return {"error": "Invalid or missing output_type"}

    



class TextInputData(BaseModel):
    text_prompt:str
    product_data: Dict[str, Any]






@app.post('/text')
def text_output(input_data:TextInputData):


    return StreamingResponse(real_time_text_generator(input_data.text_prompt,
                                                      input_data.product_data),media_type="text/event-stream")



class ImageInputData(BaseModel):
    image_prompt:str
    product_data: Dict[str, Any]
    image_location:str






@app.post('/image')
def image_output(input_data:ImageInputData):
    return StreamingResponse(real_time_image_generator(input_data.image_prompt,
                                                       input_data.product_data,
                                                       input_data.image_location),media_type="text/event-stream")





class ImageTextData(BaseModel):
    image_prompt:str
    text_prompt:str
    product_data: Dict[str, Any]
    image_location:str


@app.post('/image_and_text')
def image_and_text_output(input_data:ImageTextData):
    return StreamingResponse(real_time_image_text_generator(input_data.image_prompt,
                                                            input_data.text_prompt,
                                                            input_data.product_data,
                                                            input_data.image_location),media_type="text/event-stream")







        







    






        


