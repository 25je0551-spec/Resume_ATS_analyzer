from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal,Annotated, List, Optional,cast
from langchain_core.messages import HumanMessage,SystemMessage,BaseMessage
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from gap_schema import SkillGapAnalysis
from job_schema import InternshipList
load_dotenv()
import fitz
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)
def extract(search_results):
    structured_llm=llm.with_structured_output(InternshipList)
    prompt= PromptTemplate(
        template="""
        You are an internship extraction agent.
        Search Results:
        {results}
        Tasks:
        1. Find actual internships/jobs only.
        2. Ignore blogs.
        3. Ignore tutorials.
        4. Ignore news articles.
        5. Ignore career guides.
        For each internship extract:
        - title
        - company
        - application_link
        Return structured output.
        """,
        input_variables=["results"]
    )
    chain = prompt|structured_llm
    return chain.invoke({
        "results": str(search_results)
    })


def rank_jobs(profile, jobs):

    candidate_skills = {
        skill.lower()
        for skill in profile.skills
    }

    ranked_jobs = []

    for job in jobs.internships:

        job_text = (job.title).lower()

        matched_skills = []

        for skill in candidate_skills:

            if skill in job_text:
                matched_skills.append(skill)

        score = int(
            len(matched_skills)
            /
            max(len(candidate_skills), 1)
            * 100
        )

        ranked_jobs.append({
            "title": job.title,
            "company": job.company,
            "score": score,
            "matching_skills": matched_skills,
            "application_link": job.application_link
        })

    ranked_jobs.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked_jobs
    
    