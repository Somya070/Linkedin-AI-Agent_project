import streamlit as st
import pdfplumber #extracting text from PDF
from few_shot import FewShotPosts
from post_gen import generate_post
from db import init_db, save_post, get_all_posts
from utils import summarize_url
from calendar_db import init_calendar_db, add_calendar_entry, get_all_entries, update_status
import requests
import os

# ----------------- Initialization -----------------
init_db() #stores posts
init_calendar_db()  #content calender


#This function takes a PDF file, reads the text, and splits it into different sections like skills, experience, and
# education.
#It uses keyword matching to detect which section the text belongs to, cleans the data, and returns it in a structured
# dictionary format.
def extract_profile_data_from_pdf(file) -> dict:
    try:
        with pdfplumber.open(file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        skills, experience, education = [], [], []
        current_section = None
        for line in lines:
            low = line.lower()
            if any(h in low for h in ["skill", "skills", "technical skills", "core skills"]):
                current_section = "skills"
                continue
            if any(h in low for h in ["experience", "work experience", "professional experience", "intern"]):
                current_section = "experience"
                continue
            if any(h in low for h in ["education", "academic", "qualification", "degree", "bachelor", "master", "college", "university"]):
                current_section = "education"
                continue
            if current_section is None:
                if any(k in low for k in ["company", "inc", "ltd", "pvt", "intern", "internship", "worked", "project"]):
                    current_section = "experience"
                elif any(k in low for k in ["bachelor", "master", "b.sc", "b.tech", "bachelor's", "university", "college", "graduat"]):
                    current_section = "education"
                elif ("," in line and len(line.split()) <= 12) or any(k in low for k in ["python", "java", "excel", "sql", "machine learning", "ml"]):
                    current_section = "skills"
            if current_section == "skills":
                skills.append(line)
            elif current_section == "experience":
                experience.append(line)
            elif current_section == "education":
                education.append(line)
        parsed_skills = []
        for s in skills:
            if "," in s:
                parts = [p.strip() for p in s.split(",") if p.strip()]
                parsed_skills.extend(parts)
            else:
                parsed_skills.append(s.strip())
        def clean_list(lst):
            cleaned = []
            seen = set()
            for item in lst:
                x = item.strip()
                if len(x) < 3:
                    continue
                if x.lower() in seen:
                    continue
                seen.add(x.lower())
                cleaned.append(x)
            return cleaned
        parsed_skills = clean_list(parsed_skills)
        experience = clean_list(experience)
        education = clean_list(education)
        return {
            "skills": parsed_skills,
            "experience": experience,
            "education": education,
            "raw_text_preview": "\n".join(lines[:25])
        }
    except Exception as e:
        return {"error": str(e)}

#This function takes your profile data, topic, length, and language, and creates a custom AI prompt for generating
# LinkedIn posts.
#The prompt includes your skills, experience, and education so the AI can make the post more personal.
def build_prompt_from_profile_and_topic(profile_data: dict, topic: str, length: str, language: str) -> str:
    skills = profile_data.get("skills", [])
    experience = profile_data.get("experience", [])
    education = profile_data.get("education", [])
    preview = profile_data.get("raw_text_preview", "")
    prompt_lines = [
        "You are a professional LinkedIn content writer. Write a single LinkedIn post (no preamble).",
        f"Tone: motivational, professional, slightly personal. Keep it concise as per length requirement.",
        f"Length: {length} (Short = 1-5 lines, Medium = 6-10 lines, Long = 11-15 lines).",
        f"Language: {language} (use Hinglish format if requested, but script must be English).",
        f"Topic: {topic}.",
        "",
        "Profile information (use this to make the post personal and relevant):",
    ]
    if skills:
        prompt_lines.append(f"- Skills: {', '.join(skills)}")
    if experience:
        prompt_lines.append(f"- Experience (examples): {', '.join(experience[:5])}")
    if education:
        prompt_lines.append(f"- Education: {', '.join(education[:3])}")
    if preview:
        prompt_lines.append("\nRaw profile text preview (for context):")
        prompt_lines.append(preview)
    prompt_lines.append("\nGuidelines:")
    prompt_lines.append("- Start with a hook (1 line) and then add a short personal insight or story if possible.")
    prompt_lines.append("- Include 1 relevant hashtag or 2 short hashtags.")
    prompt_lines.append("- Add a call-to-action (connect, comment, share, or reach out).")
    prompt_lines.append("- Avoid filler and generic phrases. Make it feel like a real person.")
    return "\n".join(prompt_lines)


#This function connects to the Groq API, sends the query you type, and gets back AI-generated industry insights
def fetch_industry_trends(query: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY not set in environment."
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are an expert market research assistant. Provide concise, trend-focused insights."},
            {"role": "user", "content": query}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    try:
        res = requests.post(url, headers=headers, json=payload)
        res.raise_for_status()
        data = res.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error fetching trends: {str(e)}"

# ----------------- Streamlit App -----------------
def main():
    st.set_page_config(page_title="LinkedIn AI Agent", layout="wide",initial_sidebar_state="expanded")
    st.title("LinkedIn AI Agent")

    if "profile_data" not in st.session_state:
        st.session_state.profile_data = {}

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Profile Analysis", "Generate Post", "Link Saver", "Content Calendar", "Industry Research", "Engagement Optimization","Performance Analysis"])

    with tab1:
        st.header("Step 1 — Upload & Analyze Profile PDF")
        uploaded_pdf = st.file_uploader("Upload PDF (LinkedIn profile export / resume)", type=["pdf"])
        if st.button("Analyze Profile"):
            if uploaded_pdf:
                with st.spinner("Analyzing profile PDF..."):
                    result = extract_profile_data_from_pdf(uploaded_pdf)
                if "error" in result:
                    st.error(f"Error while analyzing PDF: {result['error']}")
                else:
                    st.success("Profile analyzed successfully!")
                    st.session_state.profile_data = result
                    st.subheader("Extracted Profile Data")
                    st.markdown("**Skills**")
                    if result["skills"]:
                        for s in result["skills"]:
                            st.write(f"- {s}")
                    else:
                        st.write("_No skills detected_")
                    st.markdown("**Experience (examples)**")
                    if result["experience"]:
                        for e in result["experience"][:10]:
                            st.write(f"- {e}")
                    else:
                        st.write("_No experience lines detected_")
                    st.markdown("**Education**")
                    if result["education"]:
                        for ed in result["education"][:5]:
                            st.write(f"- {ed}")
                    else:
                        st.write("_No education lines detected_")
                    st.subheader("Raw text preview (first 25 lines)")
                    st.code(result.get("raw_text_preview", "No preview available"))
            else:
                st.warning("Please upload a PDF file first to analyze.")

    with tab2:
        st.header("Step 2 — Generate Personalized LinkedIn Post")
        fs = FewShotPosts()
        tag_options = fs.get_tags() if hasattr(fs, "get_tags") else ["Networking", "Growth", "Rejection", "Career Change"]
        selected_tag = st.selectbox("Select topic", options=tag_options)
        selected_length = st.selectbox("Select length", options=["Short", "Medium", "Long"])
        selected_language = st.selectbox("Select language", options=["English", "Hinglish"])
        use_profile_checkbox = st.checkbox("Use analyzed profile data (if available)", value=True)
        if st.button("Generate Post"):
            profile_data = st.session_state.get("profile_data", {}) if use_profile_checkbox else {}
            prompt = build_prompt_from_profile_and_topic(profile_data, selected_tag, selected_length, selected_language)
            with st.spinner("Generating post..."):
                post = generate_post(selected_length, selected_language, prompt)
            st.subheader("Generated Post")
            st.write(post)
            save_post(content=post, tag=selected_tag, length=selected_length, language=selected_language)
            st.success("Post saved to database!")
        st.markdown("### Saved Posts")
        saved_posts = get_all_posts()
        for p in saved_posts:
            st.markdown(f"**[{p[1]}]** {p[2]}")

    with tab3:
        st.header("Link Saver — Paste a URL to summarize")
        url = st.text_input("Enter URL to summarize")
        if st.button("Summarize Link"):
            if url:
                with st.spinner("Fetching and summarizing..."):
                    summary = summarize_url(url)
                st.subheader("Summary")
                st.write(summary)
                save_post(content=summary, tag="Link Summary", length="N/A", language="English", url=url)
                st.success("Summary saved to database!")
            else:
                st.warning("Please enter a valid URL")

    with tab4:
        st.header("Content Calendar")
        with st.form("add_calendar_form"):
            title = st.text_input("Title")
            description = st.text_area("Description")
            date = st.date_input("Date")
            submitted = st.form_submit_button("Add Entry")
            if submitted and title and description:
                add_calendar_entry(title, description, str(date))
                st.success("Entry added to calendar!")
        st.subheader("All Calendar Entries")
        entries = get_all_entries()
        if entries:
            st.table(entries)
        else:
            st.info("No calendar entries yet.")
        st.write("Update entry status")
        entry_id = st.number_input("Entry ID to update", min_value=1, step=1)
        new_status = st.selectbox("New Status", ["Planned", "Completed"])
        if st.button("Update Status"):
            update_status(entry_id, new_status)
            st.success("Status updated!")

    with tab5:
        st.header("Industry Research — Powered by Groq")
        user_query = st.text_area("Enter your research query", placeholder="e.g. Latest AI trends in 2025")
        if st.button("Get Trends"):
            if user_query.strip():
                with st.spinner("Fetching industry insights..."):
                    insights = fetch_industry_trends(user_query)
                st.subheader("Industry Insights")
                st.write(insights)
            else:
                st.warning("Please enter a query to research.")

    with tab6:
        st.header("Engagement Optimization — Make Your Post Go Viral 🚀")
        post_input = st.text_area("Paste your LinkedIn post here")

        if st.button("Optimize for Engagement"):
            if post_input.strip():
                with st.spinner("Optimizing post for higher engagement..."):
                    from groq import Groq
                    import os
                    from dotenv import load_dotenv

                    # Load API key from .env
                    load_dotenv()
                    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
                    client = Groq(api_key=GROQ_API_KEY)

                    prompt = f"""
                    You are a LinkedIn growth expert. 
                    Take the following LinkedIn post and optimize it for maximum engagement while keeping its core message.
                    - Make the hook stronger in the first line.
                    - Use concise, emotional, and actionable language.
                    - Include relevant hashtags (2-3 max).
                    - Make it feel authentic and relatable.

                    Original Post:
                    {post_input}
                    """

                    response = client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        max_tokens=500
                    )

                    optimized_post = response.choices[0].message.content

                st.subheader("Optimized Post")
                st.write(optimized_post)
            else:
                st.warning("Please paste a LinkedIn post first!")

    with tab7:
        st.header("📊 Performance Analytics — Track & Improve Your LinkedIn Posts")
        analytics_input = st.text_area("Paste your LinkedIn post(s) here for performance analysis")

        if st.button("Analyze Performance"):
            if analytics_input.strip():
                with st.spinner("Analyzing your post performance..."):
                    from groq import Groq
                    import os
                    from dotenv import load_dotenv

                    # Load API key from .env
                    load_dotenv()
                    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
                    client = Groq(api_key=GROQ_API_KEY)

                    prompt = f"""
                    You are a LinkedIn post analytics expert.
                    Analyze the given LinkedIn post(s) and provide:
                    1. Engagement Score (0–10)
                    2. Clarity Score (0–10)
                    3. Emotional Appeal Score (0–10)
                    4. Tone & Style Feedback
                    5. 3 actionable improvement suggestions to boost engagement.

                    Post(s):
                    {analytics_input}
                    """

                    response = client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.5,
                        max_tokens=500
                    )

                    analytics_result = response.choices[0].message.content

                st.subheader("Performance Analysis Report")
                st.write(analytics_result)
            else:
                st.warning("Please paste a LinkedIn post first!")


if __name__ == "__main__":
    main()
