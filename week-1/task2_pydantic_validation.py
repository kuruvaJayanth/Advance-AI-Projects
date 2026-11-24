import re
from pydantic import BaseModel, EmailStr, Field, ValidationError, field_validator


class UserProfile(BaseModel):
    name: str
    age: int = Field(..., ge=18, le=120)
    email: EmailStr
    pan: str

    @field_validator("pan")
    @classmethod
    def validate_pan(cls, value: str) -> str:
        cleaned = value.strip().upper()
        if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]$", cleaned):
            raise ValueError("PAN must match format AAAAA9999A (5 letters, 4 digits, 1 letter)")
        return cleaned


if __name__ == "__main__":
    # 1. Valid input (including string-to-int age coercion and lowercase PAN normalization)
    print("--- Testing Valid Input ---")
    valid_user = UserProfile(
        name="K. Jayanth",
        age="25",  # Coerced from str to int
        email="jayanth@example.com",
        pan="abcde1234f",
    )
    print("Validated User:", valid_user.model_dump())

    # 2. Invalid input (underage, invalid email, malformed PAN)
    print("\n--- Testing Invalid Input ---")
    try:
        UserProfile(
            name="Invalid User",
            age=15,
            email="not-an-email",
            pan="12345ABCDE",
        )
    except ValidationError as exc:
        print("Caught expected ValidationError:")
        for err in exc.errors():
            print(f"  - Field '{err['loc'][0]}': {err['msg']}")