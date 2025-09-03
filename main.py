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
        st.image('https://i.imgur.com/pyfGL7D.png', width=250) 
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
            "skills": "Rupesh is skilled in:\n"
                      [cite_start]"  - **Gen AI:** ChatGPT, GPT Agents, Agentic AI, MCP, Prompt Engineering [cite: 29]\n"
                      [cite_start]"  - **Programming & Analysis:** Python (Pandas, NumPy, Scikit-Learn), R [cite: 33]\n"
                      [cite_start]"  - **Databases:** SQL (MSSQL, MySQL) [cite: 34]\n"
                      [cite_start]"  - **Dashboards & BI:** Power BI, Looker Studio, Tableau [cite: 35]\n"
                      [cite_start]"  - **Automation:** Excel VBA, Python scripting [cite: 36]\n"
                      [cite_start]"  - **Cloud:** Azure Databricks [cite: 37]\n"
                      [cite_start]"  - **ML:** Regression, predictive modeling [cite: 38]",
            [cite_start]"experience": "Rupesh has 9+ years of experience[cite: 5]. [cite_start]He is currently a Lead Analyst at Annalect India[cite: 9]. [cite_start]Previously, he worked at Merkle [cite: 14][cite_start], Ugam Solutions [cite: 20][cite_start], and Tata Consultancy Services[cite: 23].",
            [cite_start]"annalect": "At **Annalect India** (Aug 2023 - Present), Rupesh is a **Lead Analyst - Marketing Science**[cite: 9]. [cite_start]He leads a team of six [cite: 11][cite_start], manages The Home Depot campaign analytics [cite: 13][cite_start], and automates reporting pipelines[cite: 14].",
            [cite_start]"merkle": "Rupesh worked at **Merkle** (Mar 2022 - Aug 2023) as a **Lead Analyst**[cite: 14]. [cite_start]He developed custom dashboards [cite: 16][cite_start], built predictive models with over 99% accuracy [cite: 17][cite_start], and collaborated with stakeholders on data solutions[cite: 19].",
            [cite_start]"ugam": "As a **Senior Data Analyst** at **Ugam Solutions** (May 2017 - Mar 2022), he analyzed large datasets [cite: 21][cite_start], used BI tools for reporting [cite: 22][cite_start], and automated data visualizations[cite: 22].",
            [cite_start]"tcs": "At **Tata Consultancy Services** (Jan 2016 - May 2017), Rupesh worked as a **Data Analyst**, where he extracted, cleaned, and analyzed project data and created ad-hoc reports[cite: 24, 25].",
            [cite_start]"education": "Rupesh holds a **Bachelor of Computer Applications (BCA)** from North Maharashtra University, India[cite: 27].",
            "contact": "You can contact Rupesh via:\n"
                       [cite_start]"  - **Email:** rupeshdubey999@gmail.com [cite: 3]\n"
                       [cite_start]"  - **Phone:** +91 820-054-2230 [cite: 3]\n"
                       [cite_start]"  - **LinkedIn:** linkedin.com/in/rupeshdubey9/ [cite: 3]",
            [cite_start]"achievements": "Key achievements include: 70% cost savings by automating analytics workflows [cite: 42][cite_start], 99% accuracy in revenue forecasts [cite: 42][cite_start], and receiving 16+ 'Best Performer' awards in one year[cite: 43].",
            [cite_start]"python": "Rupesh is proficient in Python and its data science libraries like Pandas, NumPy, Scikit-Learn, and Streamlit[cite: 33].",
            "hello": "Hello! How can I help you learn more about Rupesh's career?",
            "hi": "Hi there! Feel free to ask me about Rupesh's skills, experience, or education."
        }
        for keyword, response in responses.items():
            if keyword in text:
                return response
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
    with st.expander("🏢 **Lead Analyst - Marketing Science | Annalect India**", expanded=True):
        [cite_start]st.markdown("**📅 August 2023 - Present** [cite: 12]")
        st.markdown(
            """
            - [cite_start]Utilized AI agents to deliver next-generation insights and deliverables[cite: 10].
            - [cite_start]Led a team of six analysts, overseeing daily operations[cite: 11].
            - [cite_start]Managed creative-campaign analytics for The Home Depot (BBDO NY) to inform optimization[cite: 13].
            - [cite_start]Automated reporting pipelines to reduce manual effort[cite: 14].
            """
        )
    with st.expander("🏢 **Lead Analyst | Merkle**"):
        [cite_start]st.markdown("**📅 March 2022 - August 2023** [cite: 15]")
        st.markdown(
            """
            - [cite_start]Developed custom reports and dashboards to monitor key performance indicators[cite: 16].
            - [cite_start]Built and deployed predictive analytics models to forecast future trends with 99% + accuracy[cite: 17].
            - [cite_start]Wrote and optimized scripts/queries for multi-source data extraction and analysis[cite: 18].
            """
        )
    with st.expander("🏢 **Senior Data Analyst | Ugam Solutions (A Merkle Company)**"):
        [cite_start]st.markdown("**📅 May 2017 - March 2022** [cite: 30]")
        st.markdown(
            """
            - [cite_start]Analyzed large datasets to uncover patterns, signals, and actionable insights[cite: 21].
            - [cite_start]Utilized Business Objects, BI tools, and data-warehouse solutions for reporting[cite: 22].
            - [cite_start]Automated data visualizations and crafted compelling stories to drive decisions[cite: 22].
            """
        )
    with st.expander("🏢 **Data Analyst | Tata Consultancy Services**"):
        [cite_start]st.markdown("**📅 January 2016 - May 2017** [cite: 31]")
        st.markdown(
            """
            - [cite_start]Extracted, cleaned, and analyzed project data to support client deliverables[cite: 24].
            - [cite_start]Created ad-hoc reports and basic dashboards to track performance metrics[cite: 25].
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
