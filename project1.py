from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal,Annotated, List, Optional
from langchain_core.messages import HumanMessage,SystemMessage,BaseMessage
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import MemorySaver
load_dotenv()
import fitz

llm = ChatGroq(
    model="llama-3.1-8b-instant"
)
def extract_text(pdf_path:str) -> str: # type: ignore
    doc = fitz.open(pdf_path)
    text=""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += str(page.get_text("text"))+"\n"
    return text

class Workexperience(BaseModel):
    company:Optional[str] = Field(description="Name of the company")
    title: Optional[str] = Field(description="Job title")
    start_date: Optional[str] = Field(description="Start date of employment")
    end_date: Optional[str] = Field(description="End date of employment, or 'Present'")
    responsibilities: Optional[List[str]] = Field(description="List of key duties and achievements")

class Education(BaseModel):
    institution:Optional[str] = Field(description="Name of the university or school")
    degree: Optional[str] = Field(description="Degree obtained")
    graduation_year: Optional[str] = Field(description="Year of graduation")

class CandidateProfile(BaseModel):
    name:Optional[str] = Field(description="Full name of the candidate")
    email: Optional[str] = Field(description="Email address")
    phone: Optional[str] = Field(description="Phone number")
    skills: Optional[List[str]] = Field(description="List of all technical and soft skills mentioned")
    experience: Optional[List[Workexperience]] = Field(description="List of work experiences")
    education: Optional[List[Education]] = Field(description="List of educational background")

def parse_resume(raw_text: str)-> CandidateProfile: # type: ignore
    structured_llm = llm.with_structured_output(CandidateProfile)
    prompt = PromptTemplate(
        template="""
    You are an expert HR assistant.

    Extract information from the resume.

IMPORTANT:
- Never invent information.
- Never use placeholder values such as John Doe, Jane Doe, john@example.com.
- If information is missing, return null or an empty value.
- Only return information explicitly present in the resume.

    Resume:
    {resume_text}

    Return all available information in the required structured format.
    If a field is missing, leave it empty.
    """,
        input_variables= ["resume_text"]
    )
    chain = prompt| structured_llm
    result = chain.invoke({"resume_text":raw_text})
    return result # type: ignore
