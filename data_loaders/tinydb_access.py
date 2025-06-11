from tinydb import TinyDB, Query
import logging




async def product_data_fetcher(brand, category):

    try:    
        db = TinyDB("data_bases/product_database.json")
        results = db.search((Query().Brand == brand) & (Query().Category == category))
        logging.info(f"Product data from data base new_product.json{results}")
        return results
    except Exception as e:
        
        raise Exception(f"Error fetching product data: {e}")



def demographics_data_fetcher(gender, region, urban_or_rural):

    try:
        result = TinyDB("data_bases/demographics.json").table("demographics").all()[-1]
        gender_data = [{g: result[g]} for g in gender] if gender != ["All Genders"] else {i:result[i] for i in ["Female", "Male", "Non_binary"]}
        locality_data = {urban_or_rural: result[urban_or_rural]} if urban_or_rural != "No Preference" else ""
        location_data = {region: result[region]} if region != "No Preference" else "Kenya"
        logging.info(f"Dmographics_data: Location data{location_data}, Gender data{gender_data}, locality data{locality_data}")
        return location_data, gender_data, locality_data
        
    except Exception as e:
        raise Exception(f"Error fetching product data: {e}")
    




# Data Fetching Functions
# @st.cache_data(show_spinner="Fetching competitor data...")
# def get_companies(prompt: str) -> str:
#     messages = [
#     {
#         "role": "system",
#         "content": (
#             """You are a market analyst specializing in the Kenyan FMCG market. 
#             When provided with a product from Pwani Oils and a list of competitors, your role is to analyze and provide:
#             - The advertisement strategies
#             - Types of advertisements
#             - Types of promotions

#             **Specifically for the competitors** provided in the prompt, not Pwani Oils itself.
#             If Pwani Oils is mentioned, it is only for context and benchmarking.
#             Your focus is on understanding what **the competitors** are doing in the Kenyan market."""
#         ),
#     },
#     {   
#         "role": "user",
#         "content": (
#             prompt
#         ),
#     },
#     ]
#     client = OpenAI(api_key=perplexity_key, base_url="https://api.perplexity.ai")
#     response = client.chat.completions.create(model="sonar", messages=messages)
#     logging.info(f"Response: {response.choices[0].message.content}")
#     return response.choices[0].message.content

# Save structured competitor data
# def json_db_creator(data, product, category):
#     class AdvertisementTechniques(TypedDict):
#         name: str= Field(description="Name of the company")
#         Advertisement_strategy:str=Field(description="overall strategy are they using to position their product in the market")
#         Type_of_advertisement:str=Field(description="channels or formats are being used? (e.g., TV, radio, social media, print, influencer marketing)")
#         Type_of_Promotion:str=Field(description="promotional tactics are they using? (e.g., discounts, free samples, bundled offers, loyalty programs)")

#     class ExtractSchema(TypedDict):
#         companies: List[AdvertisementTechniques]

#     structured_llm = llm.with_structured_output(ExtractSchema)
#     result = structured_llm.invoke(data)

#     db = TinyDB("db.json")
#     ProductCategory = Query()
#     result.update({"date": str(datetime.today().date()), "Product": product, "category": category})
#     existing_record = db.search((ProductCategory.Product == product) & (ProductCategory.category == category))
#     if existing_record:
#         # If the product and category exist, update the record
#         db.update(result, (ProductCategory.Product == product) & (ProductCategory.category == category))
#         print(f"Product '{product}' in category '{category}' updated.") 
#     else:
#         # If the product and category don't exist, insert a new record
#         db.insert(result)
#         print(f"Product '{product}' in category '{category}' inserted.")    

#     result.update({"date": str(datetime.today().date()), "Product": product, "category": category})
#     TinyDB("db.json").table("products").insert(result)

# Wrapper for prompt + saving
# def data_collector_json_getter(competitors, category, product):
#     prompt = f"""
#         You are provided with a list of competitors for the Pwani Oil company in Kenya.

#         **Product of focus**: {product}  
#         **category**: {category}  
#         **Competitors**: {competitors}

#         Your task is to analyze the **advertising and promotional strategies** used by these competitors in the Kenyan market.

#         Please provide insights under the following sections for each competitor:

#         1. **Advertisement Strategy** – What overall strategy are they using to position their product in the market?
#         2. **Type of Advertisement** – What channels or formats are being used? (e.g., TV, radio, social media, print, influencer marketing)
#         3. **Type of Promotion** – What promotional tactics are they using? (e.g., discounts, free samples, bundled offers, loyalty programs)

#         Focus only on the competitors listed. Do not provide details for Pwani Oil itself.
# """
#     data = get_companies(prompt)
#     json_db_creator(data, product, category)
#     return data

# Load competitor info
# def competitor_data_collector(product, competitors, category):
#     db = TinyDB("db.json").table("products")
#     q = Query()
#     result = db.search((q.date == str(datetime.today().date())) & (q.Product == product) & (q.category == category))
#     logging.info(f"Competitor data from data base db.json{result}")
#     return result if result else data_collector_json_getter(competitors, category, product)

