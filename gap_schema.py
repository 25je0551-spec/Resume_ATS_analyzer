from pydantic import BaseModel,Field
from typing import List

class SkillGapAnalysis(BaseModel):
    matching_skills: List[str] = Field(description="Skills the candidate possesses that match the job description.")
    missing_skills: List[str] = Field(description="Key skills required by the job that are missing from the resume.")
    learning_priority: list[str] = Field(description="arrange the missing skills in priority order starting from highly required skills to least required skills")
    overall_gap_assessment: str = Field(description="A 1-2 sentence summary of the candidate's skill alignment.")