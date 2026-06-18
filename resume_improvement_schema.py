from pydantic import BaseModel,Field
from typing import List
class ImprovedBullets(BaseModel):
    original:str = Field(description="Original resume bullets")
    improved : str = Field(description="improved ATS friendly bullets")

class ResumeImprovement(BaseModel):
    improved_bullets : List[ImprovedBullets] = Field(description="A list of the top 2 bullet points that needed the most improvement, along with their rewritten versions.")
    overall_feedback : List[str] = Field(description=" 2-3 sentence professional summary to give overall feedback.")