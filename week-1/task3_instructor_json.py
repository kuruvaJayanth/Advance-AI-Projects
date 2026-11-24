import os
from typing import List
from dotenv import load_dotenv
from groq import Groq
import instructor
from pydantic import BaseModel, Field

load_dotenv()

# Patch the Groq client with Instructor
client = instructor.from_groq(
    Groq(api_key=os.getenv("GROQ_API_KEY")),
    mode=instructor.Mode.JSON,
)


class ExtractedUser(BaseModel):
    full_name: str = Field(..., description="The full name of the user")
    role: str = Field(..., description="Job title or role")
    company: str = Field(..., description="Company or organization name")
    skills: List[str] = Field(default_factory=list, description="Technical skills mentioned")
    years_experience: int = Field(..., description="Total years of experience")


if __name__ == "__main__":
    sample_text = (
        "Hi, I'm Ananya Sharma, working as a Senior Backend Engineer at FinCore Systems "
        "for the past 6 years. I specialize in Python, FastAPI, PostgreSQL, and Docker."
    )

    user_data = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        response_model=ExtractedUser,
        messages=[
            {
                "role": "system",
                "content": "Extract structured user profile data accurately from the text.",
            },
            {
                "role": "user",
                "content": sample_text,
            },
        ],
    )

    print(user_data.model_dump_json(indent=2))