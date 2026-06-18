from pydantic import BaseModel, Field

class SearchQuery(BaseModel):
    query: str = Field(
        description="Search query for finding internships"
    )

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
from langchain_core.output_parsers import StrOutputParser

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2
)

def generate_search_query(profile)->SearchQuery:
    parser = StrOutputParser()

    

    prompt = PromptTemplate(
        template="""
Generate a SHORT search query (maximum 10 words).
Examples:

Java Spring Boot Internship
Frontend React Internship
Data Analyst Internship SQL Excel
Python Backend Internship FastAPI



Return ONLY the search query.
Do not use AND, OR, brackets, explanations, or Boolean operators.

Candidate Skills:
{skills}
Rules:
1.Focus on internships.
2.Prioritize internships posted in the last 60 days.
3.Prioritize opportunities that are currently accepting applications.
4. Do NOT search for:
   - Reddit posts
   - Courses
   - Tutorials
   - YouTube videos
   - Certifications
   - Bootcamps
   - Training programs
   - Blogs
   - Career guides
   - Learning resources
5. Prioritize actual hiring opportunities from:
   - Internshala
   - Wellfound
   - Naukri
   - LinkedIn
   - Indeed
   - Company career pages
6. Use the candidate's strongest skills.
7. Do not assume AI/ML unless present in the resume.
8. Return only one concise search query.
9. Maximum 10 words.
""",
        input_variables=[
            "skills"
        ]
    )

    chain = prompt|llm|parser

    return chain.invoke({
        "skills": ", ".join(profile.skills[:20])
    }) # type: ignore