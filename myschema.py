from pydantic import BaseModel, Field
from typing import List
class ATSanalysis(BaseModel):
    ats_score:int =Field(description="An overall alignment score from 0 to 100 evaluating how well the candidate fits the job description and resume best practices.")
    strengths:List[str] = Field(description="3-5 key areas where the candidate's profile strongly matches the requirements or demonstrates excellence.")
    weaknesses:List[str] = Field(description="Areas where the candidate is missing key requirements, links, or fails to show impact")
    suggestions:List[str] = Field(description="Actionable, concrete steps the candidate can take to improve their resume and match percentage.")
    