from pydantic import BaseModel, Field
from typing import List

class Internship(BaseModel):
    title: str = Field(description="Internship title")
    company: str = Field(description="Company name")
    application_link: str

class InternshipList(BaseModel):
    internships: List[Internship]


