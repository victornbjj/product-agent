import os
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, BadRequestError

load_dotenv()

api_key= os.environ["LLM_API_KEY"]
url = os.environ["LLM_BASE_URL"]
model=os.environ["LLM_MODEL"]

client = OpenAI(api_key=api_key, base_url=url)

