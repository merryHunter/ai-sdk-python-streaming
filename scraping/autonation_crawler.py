from crawl4ai.extraction_strategy import *
from crawl4ai.crawler_strategy import *
import asyncio
from pydantic import BaseModel, Field

url = r'https://www.autonation.com/cars-for-sale'

class CarModel(BaseModel):
    model_name: str = Field(..., description="Car model name.")
    price: str = Field(..., description="MSRP Price.")
    condition: str = Field(..., description="Used or New")
    year: int = Field(..., description="Year of the car.")
    mileage: str = Field(..., description="Mileage of the car.")
    distance: int = Field(..., description="Away distance to the car.")

from crawl4ai import AsyncWebCrawler

async def main():
    # Use AsyncWebCrawler
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            word_count_threshold=1,
            extraction_strategy= LLMExtractionStrategy(
                provider= "openai/gpt-4o", api_token = os.getenv('OPENAI_API_KEY'),
                # provider= "groq/llama-3.1-70b-versatile", api_token = os.getenv('GROQ_API_KEY'),
                schema=CarModel.model_json_schema(),
                extraction_type="schema",
                instruction="From the crawled content, extract all vehicle names along with their " \
                            "features and description attributes. Make sure not to miss anything in the entire content. " \
                            'One extracted model JSON format should look like this: ' \
                            '{ "model_name": "2022 Ford Mustang Coupe", "price": "US$16,00000", "condition": "new", "Year": 2017, "mileage": "95000 Miles", "distance": "5 Miles Away" }' 
            ),

        )
        print("Success:", result.success)
        model_fees = json.loads(result.extracted_content)
        print(len(model_fees))

        with open("data/data.json", "w", encoding="utf-8") as f:
            f.write(result.extracted_content)

asyncio.run(main())