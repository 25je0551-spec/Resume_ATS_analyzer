import streamlit as st
from project1 import extract_text, parse_resume
from ats_agent import analyse_resume
import tempfile
from myschema import ATSanalysis
from skill_gap_agent import analyse_skillgap
from resume_improvement_agent import improved_resume

from extraction_agent import rank_jobs
from query_agent import generate_search_query
from extraction_agent import extract
from tavily_agent import search_internships
from job_schema import Internship, InternshipList



# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Agentic ATS Resume Analyzer")
st.markdown(
    "Upload a resume and paste a job description to get an AI-powered ATS evaluation."
)

# -----------------------------
# Input Section
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume")
    uploaded_file = st.file_uploader(
        "Upload PDF Resume",
        type=["pdf"]
    )

with col2:
    st.subheader("2. Target Job Description")
    job_desc = st.text_area(
        "Paste the job description here",
        height=200
    )

# -----------------------------
# Analyze Button
# -----------------------------

if st.button("Analyze Resume", type="primary"):

    if uploaded_file is None:
        st.warning("Please upload a resume PDF.")
        st.stop()

    if not job_desc.strip():
        st.warning("Please paste a job description.")
        st.stop()

    try:

        # -----------------------------
        # Save Uploaded PDF
        # -----------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp_file:

            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name

        # -----------------------------
        # Extract Text
        # -----------------------------

        with st.spinner("Extracting text from resume..."):
            raw_text = extract_text(temp_path)

        # -----------------------------
        # Parse Resume
        # -----------------------------

        with st.spinner("Parsing resume..."):
            profile = parse_resume(raw_text)
        # -----------------------------
        # ATS Analysis
        # -----------------------------

        with st.spinner("Running ATS analysis..."):
            analysis = analyse_resume(profile,job_desc)
            gap_analysis = analyse_skillgap(profile,job_desc)
            improvement = improved_resume(raw_text,job_desc)

        st.success("Analysis Complete!")
        st.markdown("---")
        st.header("Resume Improvement Suggestions")
        for items in improvement.improved_bullets[:3]:
            st.subheader("Original")
            st.error(items.original)
            st.subheader("Improved")
            st.success(items.improved)
        st.markdown("---")
        st.subheader("General Feedback")
        for feedback in improvement.overall_feedback:
            st.info(feedback)

        st.markdown("---")
        st.header("Skill Gap Analysis")
        st.subheader("✅ Matching Skills")
        st.success(", ".join(gap_analysis.matching_skills))
        st.subheader("❌ Missing Skills")
        st.error(", ".join(gap_analysis.missing_skills))
        st.subheader("📚 Learning Priority")
        st.info(", ".join(gap_analysis.learning_priority))
        st.subheader("📋 Assessment")
        st.write(gap_analysis.overall_gap_assessment)


        st.markdown("---")

        # -----------------------------
        # Candidate Info
        # -----------------------------

        st.header(f"Candidate: {profile.name}")

        score_col, info_col = st.columns([1, 2])

        with score_col:
            st.metric(
                label="ATS Score",
                value=f"{analysis.ats_score}/100"
            )

        with info_col:
            st.write(f"**Email:** {profile.email}")
            st.write(f"**Phone:** {profile.phone}")

        st.markdown("---")

        # -----------------------------
        # Skills
        # -----------------------------

        st.subheader("Skills")

        if profile.skills:
            st.write(f", " .join(profile.skills))

        # -----------------------------
        # Education
        # -----------------------------

        st.subheader("Education")

        if profile.education:
            for edu in profile.education:

                st.markdown(
                    f"""
                    **Institution:** {edu.institution}

                    **Degree:** {edu.degree}

                    **Graduation Year:** {edu.graduation_year}
                    """
                )

        # -----------------------------
        # Experience
        # -----------------------------

        st.subheader("Experience")

        if profile.experience:

            for exp in profile.experience:

                st.markdown(
                    f"""
                    **Company:** {exp.company}

                    **Role:** {exp.title}

                    **Duration:** {exp.start_date} - {exp.end_date}
                    """
                )

                if exp.responsibilities:
                    for responsibility in exp.responsibilities:
                        st.write(f"• {responsibility}")

                st.markdown("---")

        # -----------------------------
        # ATS Feedback
        # -----------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.subheader("🟢 Strengths")

            for item in analysis.strengths:
                st.success(item)

        with col2:

            st.subheader("🔴 Weaknesses")

            for item in analysis.weaknesses:
                st.error(item)

        with col3:

            st.subheader("💡 Suggestions")

            for item in analysis.suggestions:
                st.info(item)

        st.markdown("---")
        query = generate_search_query(profile)
        search_query=query[:350] # type: ignore
        search_results = search_internships(search_query)
        for item in search_results:
            if "content" in item:
                item["content"] = item["content"][:500]
        jobs = extract(search_results)
        ranked_jobs = rank_jobs(profile,jobs)
        st.header("🎯 Top Internship Matches")
        for job in ranked_jobs[:5]:
            st.subheader(f"{job['title']} ")
            st.write(f"🏢 {job['company']}")
            st.write("Skills Match: "+", ".join(job['matching_skills']))
            st.link_button("Apply Here",job['application_link'])
            st.divider()
        

        

        # -----------------------------
        # Debug Section
        # -----------------------------

        with st.expander("View Parsed Resume Data"):

            st.json(profile.model_dump())

        with st.expander("View Extracted Resume Text"):

            st.text(raw_text[:5000])

    except Exception as e:

        st.error(f"Error: {str(e)}")