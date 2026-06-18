from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal,Annotated, List, Optional,cast
from langchain_core.messages import HumanMessage,SystemMessage,BaseMessage
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from gap_schema import SkillGapAnalysis
load_dotenv()
import fitz
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)
def analyse_skillgap(profile,job_description)->SkillGapAnalysis:
    structured_llm = llm.with_structured_output(SkillGapAnalysis)
    prompt = PromptTemplate(
        template="""
        Candidate Skills:
        {skills}

        Job Description:
        {job_description}

        Identify:

        1. Skills already matched
        2. Missing skills
        3. Learning priority order

        """,
        input_variables=[
            "skills",
            "job_description"
        ]
    )
    chain = prompt | structured_llm
    result = chain.invoke({
    "skills": profile.skills,
    "job_description": job_description
})
    return cast(SkillGapAnalysis, result)