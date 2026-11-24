import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Available chat models on your account:
# - "openai/gpt-oss-120b"  (Flagship, fast & capable)
# - "qwen/qwen3.8-27b"     (Strong reasoning & coding)
# - "openai/gpt-oss-20b"   (Lightweight & fast)
# - "allam-2-7b"           (Arabic/English model)

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "Say 'Groq connection successful!' in one sentence.",
        }
    ],
)

# Print the model's response
print(response.choices[0].message.content)