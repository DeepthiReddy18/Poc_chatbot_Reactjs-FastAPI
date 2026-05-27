from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = AzureOpenAI(
    api_key = os.getenv("subscription_key"),
    api_version = os.getenv("api_version"),
    azure_endpoint = os.getenv("endpoint")

)

deployment = os.getenv("deployment")

def generate_response(query, chunks):
    context = "\n\n".join(chunks)

    prompt = f"""
                you are an HR assistant chatbot.

                Answer ONLY from the provided context.

                If answer not available say:
                "I could not find that information in company policies."

                Context:
                {context}

                Question:
                {query}
                """
    
    response = client.chat.completions.create(
            model = deployment,
            messages=[
                    {
                        "role": "system",
                        "content": "you are a helpful HR assistant"    
                    },
                    {
                            "role": "user",
                            "content":prompt
                    }
            ],
            temperature = 1 
        )
    
    return response.choices[0].message.content