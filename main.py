import streamlit as st
from pathlib import Path

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Rupesh Dubey | Digital Portfolio",
    page_icon="🤖",
    layout="wide"
)

# --- INJECT CUSTOM CSS ---
# This CSS enhances the UI, adds a hero card, and improves button styling
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background-color: #1a1a2e; /* Dark blue-purple background */
        color: #e0e0e0;
    }

    /* Hero section card */
    .hero-card {
        background-color: #162447; /* Slightly lighter card color */
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        border: 1px solid #4a4e69;
    }
    
    .hero-card h1, .hero-card h2, .hero-card p {
        color: #f2f2f2; /* Ensure high contrast text */
    }

    /* Style for the expander headers */
    .st-emotion-cache-1de5w8g {
        background-color: #1f4068; /* Expander header color */
        border-radius: 10px;
        border: 1px solid #4a4e69;
    }

    /* Style for download button */
    .stDownloadButton > button {
        background-color: #e43f5a; /* A vibrant accent color */
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .stDownloadButton > button:hover {
        background-color: #b8324f;
        border: none;
    }
    
    /* Streamlit tabs styling */
    .stTabs [data-baseweb="tab-list"] {
		gap: 24px;
	}
	.stTabs [data-baseweb="tab"] {
		height: 50px;
        white-space: pre-wrap;
		background-color: transparent;
		border-radius: 4px 4px 0px 0px;
		gap: 8px;
		padding-top: 10px;
		padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
  		background-color: #1f4068;
	}

</style>
""", unsafe_allow_html=True)


# --- HERO SECTION (UPDATED) ---
# We wrap the hero section in a container with our custom CSS class
with st.container():
    st.markdown('<div class="hero-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        # Using a reliable URL for the image to avoid broken paths
        st.image('https://raw.githubusercontent.com/rrupeshd/Portfolio/refs/heads/main/Profile_Pic.png', width=250) 
    with col2:
        st.title("Rupesh Dubey")
        st.subheader("Lead - Marketing Science")
        st.write(
            """
            [cite_start]Data Science professional with 9+ years of expertise in AI-driven analytics, forecasting, and automation[cite: 5].
            [cite_start]Proven ability to lead teams, optimize workflows, and translate complex data into strategic business insights[cite: 7].
            """
        )
        st.write("📍 Vapi, Gujarat, India") # This location is from the context, not the resume text.
    st.markdown('</div>', unsafe_allow_html=True)


st.write("---")

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🤖 RupeshBot", "🏢 Work Experience", "🔗 Projects & Links", "📄 Download Resume"])

# --- TAB 1: RUPESHBOT ---
with tab1:
    st.header("RupeshBot: Your AI Career Assistant")
    st.write("Ask me anything about Rupesh's skills, experience, or education. I'm trained on his resume.")
    st.write("*Note: I am a simple rule-based bot and can only answer specific questions based on keywords.*")

def get_bot_response(user_input):
    text = user_input.lower()
    responses = {
        # --- THIS IS THE CORRECTED PART ---
        "skills": """
        Rupesh is skilled in:
          - **Gen AI:** ChatGPT, GPT Agents, Agentic AI, MCP, Prompt Engineering
          - **Programming & Analysis:** Python (Pandas, NumPy, Scikit-Learn), R
          - **Databases:** SQL (MSSQL, MySQL)
          - **Dashboards & BI:** Power BI, Looker Studio, Tableau
          - **Automation:** Excel VBA, Python scripting
          - **Cloud:** Azure Databricks
          - **ML:** Regression, predictive modeling
        """,
        # --- END OF CORRECTION ---
        "experience": "Rupesh has 9+ years of experience. He is currently a Lead Analyst at Annalect India. Previously, he worked at Merkle, Ugam Solutions, and Tata Consultancy Services.",
        "annalect": "At **Annalect India** (Aug 2023 - Present), Rupesh is a **Lead Analyst - Marketing Science**. He leads a team of six, manages The Home Depot campaign analytics, and automates reporting pipelines.",
        "merkle": "Rupesh worked at **Merkle** (Mar 2022 - Aug 2023) as a **Lead Analyst**. He developed custom dashboards, built predictive models with over 99% accuracy, and collaborated with stakeholders on data solutions.",
        "ugam": "As a **Senior Data Analyst** at **Ugam Solutions** (May 2017 - Mar 2022), he analyzed large datasets, used BI tools for reporting, and automated data visualizations.",
        "tcs": "At **Tata Consultancy Services** (Jan 2016 - May 2017), Rupesh worked as a **Data Analyst**, where he extracted, cleaned, and analyzed project data and created ad-hoc reports.",
        "education": "Rupesh holds a **Bachelor of Computer Applications (BCA)** from North Maharashtra University, India.",
        "contact": "You can contact Rupesh via:\n"
                   "  - **Email:** rupeshdubey999@gmail.com\n"
                   "  - **Phone:** +91 820-054-2230\n"
                   "  - **LinkedIn:** linkedin.com/in/rupeshdubey9/",
        "achievements": "Key achievements include: 70% cost savings by automating analytics workflows, 99% accuracy in revenue forecasts, and receiving 16+ 'Best Performer' awards in one year.",
        "python": "Rupesh is proficient in Python and its data science libraries like Pandas, NumPy, Scikit-Learn, and Streamlit.",
        "hello": "Hello! How can I help you learn more about Rupesh's career?",
        "hi": "Hi there! Feel free to ask me about Rupesh's skills, experience, or education."
    }
    for keyword, response in responses.items():
        if keyword in text:
            return response.strip() # Using .strip() to remove any leading/trailing whitespace
    return "I'm sorry, I can only answer questions about Rupesh Dubey's professional background. Please ask about his skills, experience, education, or achievements."

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Ask me about Rupesh's career!"}]
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("Ask about skills, experience, education..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            response = get_bot_response(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --- TAB 2: WORK EXPERIENCE ---
with tab2:
    st.header("Interactive Career Timeline")

    # --- Annalect ---
    with st.expander("🏢 **Lead Analyst - Marketing Science | Annalect India**", expanded=True):
        st.markdown("**📅 August 2023 - Present**")
        st.markdown(
            """
            - Utilized AI agents to deliver next-generation insights and deliverables.
            - Led a team of six analysts, overseeing daily operations.
            - Managed creative-campaign analytics for The Home Depot (BBDO NY) to inform optimization.
            - Automated reporting pipelines to reduce manual effort.
            """
        )

    # --- Merkle ---
    with st.expander("🏢 **Lead Analyst | Merkle**"):
        st.markdown("**📅 March 2022 - August 2023**")
        st.markdown(
            """
            - Developed custom reports and dashboards to monitor key performance indicators.
            - Built and deployed predictive analytics models to forecast future trends with 99% + accuracy.
            - Wrote and optimized scripts/queries for multi-source data extraction and analysis.
            """
        )

    # --- Ugam Solutions ---
    with st.expander("🏢 **Senior Data Analyst | Ugam Solutions (A Merkle Company)**"):
        st.markdown("**📅 May 2017 - March 2022**")
        st.markdown(
            """
            - Analyzed large datasets to uncover patterns, signals, and actionable insights.
            - Utilized Business Objects, BI tools, and data-warehouse solutions for reporting.
            - Automated data visualizations and crafted compelling stories to drive decisions.
            """
        )

    # --- Tata Consultancy Services ---
    with st.expander("🏢 **Data Analyst | Tata Consultancy Services**"):
        st.markdown("**📅 January 2016 - May 2017**")
        st.markdown(
            """
            - Extracted, cleaned, and analyzed project data to support client deliverables.
            - Created ad-hoc reports and basic dashboards to track performance metrics.
            """
        )
# --- TAB 3: PROJECTS & LINKS ---
with tab3:
    st.header("Find Me Online")
    st.write("Links to my socials, professional profiles, and project repositories.")
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.subheader("🌐 Socials")
        st.markdown("🔗 [LinkedIn](https://linkedin.com/in/rupeshdubey9/)")
        st.markdown("🔗 [Twitter / X](https://twitter.com/your-username-placeholder)")
        st.markdown("🔗 [Instagram](https://instagram.com/your-username-placeholder)")
    with col2:
        st.subheader("💻 Professional")
        st.markdown("🔗 [GitHub](https://github.com/your-username-placeholder)")
        st.markdown("🔗 [My App Portfolio](https://your-app-portfolio-link.com)")
        st.markdown("🔗 [Kaggle](https://kaggle.com/your-username-placeholder)")
    with col3:
        st.subheader("📜 Certifications")
        st.markdown("🔗 [Google Data Analytics](https://your-cert-link-placeholder.com)")
        st.markdown("🔗 [Azure Data Scientist](https://your-cert-link-placeholder.com)")
        st.markdown("🔗 [Python for Data Science](https://your-cert-link-placeholder.com)")

# --- TAB 4: DOWNLOAD RESUME ---
with tab4:
    st.header("Download My Resume")
    st.write("Click the button below to download the latest version of my resume in PDF format.")
    resume_file = Path(__file__).parent / "resume.pdf"
    if resume_file.exists():
        with open(resume_file, "rb") as pdf_file:
            PDFbyte = pdf_file.read()
        st.download_button(
            label="📄 Download Resume PDF",
            data=PDFbyte,
            file_name="Rupesh_Dubey_Resume.pdf",
            mime="application/octet-stream"
        )
    else:
        st.error("Resume PDF not found. Please make sure 'resume.pdf' is in the same folder as the app.py file.")
