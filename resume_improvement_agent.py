from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from resume_improvement_schema import ResumeImprovement, ImprovedBullets
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)
def improved_resume(resume_text,job_description)->ResumeImprovement:
    structured_llm = llm.with_structured_output(ResumeImprovement)
    prompt = PromptTemplate(template="""
You are an expert resume coach.

Resume:
{resume}

Job Description:
{job_description}
IMPORTANT:
Return valid structured output.

improved_bullets MUST be a list.
Do NOT return improved_bullets as a string.

Tasks:

1. Rewrite weak resume bullet points.
2. Improve ATS keywords.
3. Add measurable impact where appropriate.
4. Make the resume more attractive to recruiters.

Return:
- improved_bullets
- overall_feedback
""",
        input_variables=[
            "resume",
            "job_description"
        ]
    )
    chain = prompt| structured_llm
    try:
        return chain.invoke({
            "resume":resume_text[:3000],
            "job_description":job_description[:1000]
            }) # type: ignore
    except Exception:
         return chain.invoke({
            "resume":resume_text[:3000],
            "job_description":job_description[:1000]
            }) # type: ignore

