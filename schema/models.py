import uuid
from enum import Enum
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field, computed_field, computed_field, field_validator


class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class Patient(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., title="The name of the patient")
    email: str = Field(..., title="The email of the patient")
    gender: Gender = Field(..., title="The gender of the patient")
    age: int = Field(..., title="The age of the patient", gt=0, lt=120)
    weight: float = Field(..., title="The weight of the patient in kg")
    height: float = Field(..., title="The height of the patient in m", gt=0, lt=3)
    smoker: bool = Field(..., title="Whether the patient is a smoker")
    income_lpa: float = Field(..., title="The income of the patient in lakhs per annum")
    occupation: Literal['retired','freelancer','student','government_job','business_owner','unemployed','private_job'] = Field(..., title="The occupation of the patient")
    
    @field_validator('name')
    def name_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError('Name must not be empty')
        return value
    
    @field_validator('email')
    def email_must_be_valid(cls, value):
        if '@' not in value:
            raise ValueError('Invalid email address')
        return value

    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate the Body Mass Index (BMI) of the patient."""
        height_in_meters = self.height # Convert height from cm to meters
        return round(self.weight / (height_in_meters ** 2), 2)  # BMI formula
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        """Determine the lifestyle risk based on smoking status and BMI."""
        if self.smoker and self.bmi > 30:
            return 'high'
        elif self.smoker or self.bmi > 27:
            return 'medium'
        else:
            return 'low'
        
    @computed_field
    @property
    def age_group(self) -> str:
        """Categorize the patient into an age group."""
        if self.age <25:
            return 'young'
        elif self.age < 45:
            return 'adult'
        elif self.age < 60:
            return 'middle_aged'
        else:
            return 'senior'
    
class PatientUpdate(BaseModel):
    name: Optional[str] = Field(None, title="The name of the patient")
    email: Optional[str] = Field(None, title="The email of the patient")
    city: Optional[str] = Field(None, title="The city of the patient")
    gender: Optional[Gender] = Field(None, title="The gender of the patient")
    age: Optional[int] = Field(None, title="The age of the patient", gt=0, lt=120)
    weight: Optional[float] = Field(None, title="The weight of the patient in kg")
    height: Optional[float] = Field(None, title="The height of the patient in m", gt=0, lt=3)
    smoker: Optional[bool] = Field(None, title="Whether the patient is a smoker")
    income_lpa: Optional[float] = Field(None, title="The income of the patient in lakhs per annum")
    occupation: Optional[Literal['retired','freelancer','student','government_job','business_owner','unemployed','private_job']] = Field(None, title="The occupation of the patient")


class ListPatientsResponse(BaseModel):
    total: int
    patients: List[Patient]


class PredictionResponse(BaseModel):
    predicted_category: str = Field(..., description="The predicted insurance premium category")
    confidence: float = Field(..., description="The confidence of the prediction")
    class_probabilities: Dict[str, float] = Field(..., description="The probabilities of each insurance premium category")