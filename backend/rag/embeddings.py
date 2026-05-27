from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = AzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),
    api_version = os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

)

deployment = os.getenv("EMBEDDING_DEPLOYMENT")

def generate_embedding(text):
    response = client.embeddings.create(
        input = text,
        model = deployment,
    )

    return list(response.data[0].embedding)
