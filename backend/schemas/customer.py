from pydantic import BaseModel, Field, field_validator


class CustomerInput(BaseModel):
    CreditScore: int = Field(..., ge=300, le=900)
    Geography: str
    Gender: str
    Age: int = Field(..., ge=18, le=100)
    Tenure: int = Field(..., ge=0, le=20)
    Balance: float = Field(..., ge=0)
    NumOfProducts: int = Field(..., ge=1, le=4)
    HasCrCard: int = Field(..., ge=0, le=1)
    IsActiveMember: int = Field(..., ge=0, le=1)
    EstimatedSalary: float = Field(..., ge=0)

    @field_validator('Geography')
    @classmethod
    def validate_geography(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError('Geography cannot be empty')
        return cleaned

    @field_validator('Gender')
    @classmethod
    def validate_gender(cls, value: str) -> str:
        cleaned = value.strip().capitalize()
        if cleaned not in {'Male', 'Female'}:
            raise ValueError('Gender must be Male or Female')
        return cleaned