from langchain_core.prompts import PromptTemplate
from myschema import ATSanalysis
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from project1 import CandidateProfile
load_dotenv()
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2
)
def analyse_resume(profile: CandidateProfile, job_description)->ATSanalysis:
    structured_llm=llm.with_structured_output(ATSanalysis)
    prompt = PromptTemplate(
        template="""
        You are an ATS (Applicant Tracking System) expert.

        Analyze the following candidate profile.

        Candidate Profile:
        {profile}
        Job Description:
        {job_description}

        Evaluate:

        1. Resume completeness
        2. Skill relevance
        3. Education
        4. Experience
        5. Project quality
        6. ATS friendliness

        Return:
        - score (0-100)
        - strengths
        - weaknesses
        - suggestions
        """,
        input_variables=["profile","job_description"]

    )
    chain = prompt | structured_llm
    return chain.invoke({
        "job_description":job_description,
        "profile":profile.model_dump_json()
    }) # pyright: ignore[reportReturnType]