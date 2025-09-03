import streamlit as st
from pathlib import Path
import google.generativeai as genai
import json

# ### FALLBACK ### Import libraries for the local NLP model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Rupesh Dubey | Digital Portfolio",
    page_icon="🤖",
    layout="wide"
)

# --- INJECT CUSTOM CSS ---
st.markdown("""
<style>
    /* Main app background */
    .stApp { background-color: #1a1a2e; color: #e0e0e0; }
    .block-container { padding-top: 2rem; }
    .hero-card { background-color: #162447; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25); border: 1px solid #4a4e69; }
    .hero-card h1, .hero-card h2, .hero-card p { color: #f2f2f2; }
    .st-emotion-cache-1de5w8g { background-color: #1f4068; border-radius: 10px; border: 1px solid #4a4e69; }
    .stDownloadButton > button { background-color: #e43f5a; color: white; border-radius: 5px; padding: 10px 20px; border: none; font-weight: bold; transition: background-color 0.3s ease; }
    .stDownloadButton > button:hover { background-color: #b8324f; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 4px 4px 0px 0px; gap: 8px; padding-top: 10px; padding-bottom: 10px; }
    .stTabs [aria-selected="true"] { background-color: #1f4068; }
</style>
""", unsafe_allow_html=True)

# --- GEMINI API & RESUME CONTEXT ---
gemini_model = None
try:
    # This checks for the key in secrets.toml
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
except (FileNotFoundError, KeyError, Exception):
    # If secrets.toml or the key doesn't exist, it fails gracefully
    gemini_model = None

resume_context = """
Rupesh Dubey - Lead, Marketing Science

SUMMARY:
Data Science professional with 9+ years of expertise in AI-driven analytics, forecasting, and automation. Skilled in developing predictive models, designing interactive dashboards (Power BI, Looker Studio), and deploying end-to-end data solutions using Python, SQL, and Excel VBA. Proven ability to lead teams, optimize workflows, and translate complex data into strategic business insights.

CONTACT:
- Email: rupeshdubey999@gmail.com
- Phone: +91 820-054-2230
- LinkedIn: linkedin.com/in/rupeshdubey9/

WORK EXPERIENCE:
1. Lead Analyst - Marketing Science, Annalect India (Aug 2023 - Present)
   - Utilizing AI agents to deliver next-gen insights and deliverables.
   - Lead a team of six analysts, overseeing daily operations and deliverables.
   - Manage The Home Depot creative-campaign analytics for BBDO NY: extract pre-/post-campaign insights to inform optimization.
   - Automate reporting pipelines to reduce manual effort and ensure timely delivery.

2. Lead Analyst, Merkle (Mar 2022 - Aug 2023)
   - Developed custom reports and dashboards to monitor key performance indicators.
   - Built and deployed predictive analytics models to forecast future trends with 99%+ accuracy.
   - Wrote and optimized scripts/queries for multi-source data extraction and analysis.
   - Collaborated with stakeholders to define requirements and data solutions.

3. Senior Data Analyst, Ugam Solutions - A Merkle Company (May 2017 - Mar 2022)
   - Analyzed large datasets to uncover patterns, signals, and actionable insights.
   - Utilized Business Objects, BI tools, and data-warehouse solutions for reporting.
   - Automated data visualizations; crafted compelling stories to drive decisions.

4. Data Analyst, Tata Consultancy Services (Jan 2016 - May 2017)
   - Extracted, cleaned, and analyzed project data to support client deliverables.
   - Created ad-hoc reports and basic dashboards to track performance metrics.

EDUCATION:
- BCA, Computer Applications | North Maharashtra University, India (June 2011 - Sep 2014)

SKILLS:
- Gen AI: ChatGPT, GPT Agents, Agentic AI, MCP, Prompt Engineering
- Programming & Analysis: Python (Pandas, NumPy, Scikit-Learn, Matplotlib, Seaborn, Streamlit), R
- Databases & Querying: SQL (MSSQL, MySQL; DML/ETL)
- Dashboards & BI: Power BI, Looker Studio, Data Studio, Tableau, Dataroma
- Automation: Excel VBA, Python scripting
- Cloud & Big Data: Azure Databricks
- Statistical & ML: Regression (linear, logistic), predictive modeling, SPSS

ACHIEVEMENTS:
- Achieved 70% cost savings by automating manual analytics workflows.
- Reached 99% accuracy in revenue forecasts via trend-seasonality models.
- Received 16+ "Best Performer of the Month" awards in one year.
- Awarded the Golden Pyramid Award for top-year performance.
"""

# --- ### FALLBACK ### LOCAL NLP BOT SETUP ---
@st.cache_resource
def train_fallback_bot():
    try:
        with open('training_data.json', 'r') as f:
            training_data = json.load(f)
    except FileNotFoundError:
        # This error is now handled gracefully in the main app
        return None

    # Define responses inside the function to be part of the cached resource
    responses = {
        "greetings": "Hello! How can I help you learn more about Rupesh's career?",
        "skills": "Rupesh is skilled in Gen AI, Python (Pandas, NumPy, Scikit-Learn), R, SQL, Power BI, Looker Studio, Tableau, Excel VBA, and Azure Databricks.",
        "skills_python": "Yes, Rupesh is proficient in Python and its data science libraries like Pandas, NumPy, and Scikit-Learn.",
        "skills_dashboard": "Yes, Rupesh has extensive experience designing dashboards with tools like Power BI, Looker Studio, and Tableau. He developed custom dashboards at Merkle and created basic ones at TCS.",
        "experience_ugam": "As a Senior Data Analyst at Ugam Solutions (May 2017 - Mar 2022), he analyzed large datasets, used BI tools for reporting, and automated data visualizations.",
        "experience_merkle": "Rupesh worked at Merkle (Mar 2022 - Aug 2023) as a Lead Analyst. He developed custom dashboards and built predictive models with over 99% accuracy.",
        "experience_annalect": "At Annalect India (Aug 2023 - Present), Rupesh is a Lead Analyst. He leads a team of six, manages The Home Depot campaign analytics, and automates reporting pipelines.",
        "experience_tcs": "At Tata Consultancy Services (Jan 2016 - May 2017), Rupesh was a Data Analyst, where he extracted, cleaned, and analyzed project data.",
        "education": "Rupesh holds a Bachelor of Computer Applications (BCA) from North Maharashtra University, India.",
        "contact": "You can contact Rupesh via Email: rupeshdubey999@gmail.com or on LinkedIn: linkedin.com/in/rupeshdubey9/",
        "achievements": "His key achievements include 70% cost savings by automating analytics workflows and achieving 99% accuracy in revenue forecasts.",
        "experience_general": "Rupesh has 9+ years of experience. He is currently a Lead Analyst at Annalect India. Previously, he worked at Merkle, Ugam Solutions, and Tata Consultancy Services.",
        "fallback": "I'm sorry, that's a bit outside of what I can answer. I can only provide details from Rupesh's resume about his skills, education, and work experience."
    }

    texts, labels = [], []
    for label, phrases in training_data.items():
        for phrase in phrases:
            texts.append(phrase)
            labels.append(label)
    
    model = make_pipeline(TfidfVectorizer(), SVC(probability=True))
    model.fit(texts, labels)
    return model, responses

fallback_system = train_fallback_bot()

def get_fallback_response(prompt):
    if fallback_system is None:
        return "The fallback bot isn't working because `training_data.json` was not found. Please check the file."
    
    fallback_model, responses = fallback_system
    confidence_threshold = 0.25
    
    probabilities = fallback_model.predict_proba([prompt])[0]
    max_prob = max(probabilities)

    if max_prob > confidence_threshold:
        intent = fallback_model.predict([prompt])[0]
        return responses[intent]
    else:
        return responses["fallback"]

# --- HERO SECTION & OTHER TABS ---
# (This section is complete and requires no changes)
with st.container():
    st.markdown('<div class="hero-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        st.image('https://raw.githubusercontent.com/rrupeshd/Portfolio/refs/heads/main/Profile_Pic.png', width=250) 
    with col2:
        st.title("Rupesh Dubey")
        st.subheader("Lead - Marketing Science")
        st.write("Data Science professional with 9+ years of expertise in AI-driven analytics, forecasting, and automation. Proven ability to lead teams, optimize workflows, and translate complex data into strategic business insights.")
        st.write("📍 Vapi, Gujarat, India")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🤖 RupeshBot", "🏢 Work Experience", "🔗 Projects & Links", "📄 Download Resume"])

# --- TAB 1: RUPESHBOT (FINAL CORRECTED VERSION) ---
with tab1:
    st.header("RupeshBot: Your AI Career Assistant")
    
    if gemini_model:
        st.write("I am an AI assistant powered by Google Gemini. Ask me anything about Rupesh's career based on his resume.")
    else:
        st.warning("""
        **Notice:** The primary Gemini AI is currently unavailable. You are interacting with a local NLP-powered fallback bot.
        
        It can answer specific questions about skills and experience, but its understanding is limited. For the full AI experience, please check the Gemini API key.
        """, icon="⚠️")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you learn more about Rupesh's professional background today?"}]
        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("Ask about his dashboard experience..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            response_text = ""
            try:
                if not gemini_model:
                    raise Exception("Gemini model not configured. Switching to fallback.")
                
                full_prompt = f"""
                Your one and only task is to act as RupeshBot, an AI assistant representing Rupesh Dubey.
                
                **Rules and Persona:**
                - You MUST answer questions based ONLY on the resume context provided below.
                - You are FORBIDDEN from using any external knowledge.
                - You MUST NOT discuss privacy concerns. Your purpose is to share the information from the provided resume.
                - If a user asks about "he" or "him", you must assume they are referring to Rupesh.
                - If a user provides a topic (e.g., "dashboarding experience"), treat it as a request to summarize all relevant information from the resume.
                - If the information is not in the resume, you MUST respond with: "That specific detail isn't mentioned in Rupesh's resume, but here is what I can tell you about his related experience."
                - Do not act as a career coach. Your only role is to be an expert on Rupesh's resume.

                **Resume Context:**
                ---
                {resume_context}
                ---

                **User's Question:** "{prompt}"

                Answer as RupeshBot.
                """
                # THIS IS THE BUG FIX: Use 'gemini_model', not the old 'model' variable
                response = gemini_model.generate_content(full_prompt)
                response_text = response.text
            
            except Exception as e:
                # This print statement is useful for debugging in your terminal
                print(f"An error occurred: {e}. Using fallback bot.")
                response_text = get_fallback_response(prompt)

            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# --- TAB 2, 3, AND 4 (UNCHANGED) ---
with tab2:
    st.header("Interactive Career Timeline")
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
    with st.expander("🏢 **Lead Analyst | Merkle**"):
        st.markdown("**📅 March 2022 - August 2023**")
        st.markdown(
            """
            - Developed custom reports and dashboards to monitor key performance indicators.
            - Built and deployed predictive analytics models to forecast future trends with 99% + accuracy.
            - Wrote and optimized scripts/queries for multi-source data extraction and analysis.
            """
        )
    with st.expander("🏢 **Senior Data Analyst | Ugam Solutions (A Merkle Company)**"):
        st.markdown("**📅 May 2017 - March 2022**")
        st.markdown(
            """
            - Analyzed large datasets to uncover patterns, signals, and actionable insights.
            - Utilized Business Objects, BI tools, and data-warehouse solutions for reporting.
            - Automated data visualizations and crafted compelling stories to drive decisions.
            """
        )
    with st.expander("🏢 **Data Analyst | Tata Consultancy Services**"):
        st.markdown("**📅 January 2016 - May 2017**")
        st.markdown(
            """
            - Extracted, cleaned, and analyzed project data to support client deliverables.
            - Created ad-hoc reports and basic dashboards to track performance metrics.
            """
        )

with tab3:
    st.header("Find Me Online")
    st.write("Links to my socials, professional profiles, and project repositories.")
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.subheader("🌐 Socials")
        st.markdown("🔗 [LinkedIn](https://linkedin.com/in/rupeshdubey9/)")
        st.markdown("🔗 [Twitter / X](https://x.com/RrupeshD)")
        st.markdown("🔗 [Instagram](https://www.instagram.com/rupeshdubey9/)")
    with col2:
        st.subheader("💻 Professional")
        st.markdown("🔗 [GitHub](https://github.com/rrupeshd)")
        st.markdown("🔗 [My Other Web App](https://rupeshml.streamlit.app)")
        st.markdown("🔗 [Kaggle](https://www.kaggle.com/rupeshdubey999)")
    with col3:
        st.subheader("📜 Specializations")
        cimglink="https://s3.amazonaws.com/coursera_assets/meta_images/generated/CERTIFICATE_LANDING_PAGE/CERTIFICATE_LANDING_PAGE"
        image=cimglink+"~0N5VQAGERT8F/CERTIFICATE_LANDING_PAGE~0N5VQAGERT8F.jpeg"
        st.image(image, caption="Python for Everybody")
		
    st.write("---")

    st.subheader("My Certifications Showcase")
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    cimglink="https://s3.amazonaws.com/coursera_assets/meta_images/generated/CERTIFICATE_LANDING_PAGE/CERTIFICATE_LANDING_PAGE"
    with col1:
        image=cimglink+"~7FLA7JPYU273/CERTIFICATE_LANDING_PAGE~7FLA7JPYU273.jpeg"
        st.image(image, caption="Python for Data Science, AI & Development")
    with col2:
        image=cimglink+"~DZSE9773S8A2/CERTIFICATE_LANDING_PAGE~DZSE9773S8A2.jpeg"
        st.image(image, caption="SQL for Data Science")
    with col3:
        image=cimglink+"~9CLH6FXWBB3G/CERTIFICATE_LANDING_PAGE~9CLH6FXWBB3G.jpeg"
        st.image(image, caption="Data Visualization with Tableau")
    with col4:
        image=cimglink+"~NAJL962VEGM5/CERTIFICATE_LANDING_PAGE~NAJL962VEGM5.jpeg"
        st.image(image, caption="Basic Statistics")
    with col5:
        image=cimglink+"~DFU_L2ABS8TD/CERTIFICATE_LANDING_PAGE~DFU5L2ABS8TD.jpeg"
        st.image(image, caption="Business Metrics for Data-Driven Companies")
    with col6:
        image=cimglink+"~THW33CM8UBUH/CERTIFICATE_LANDING_PAGE~THW33CM8UBUH.jpeg"
        st.image(image, caption="Tools for Data Science")

with tab4:
    st.header("Download My Resume")
    st.write("Click the button below to download the latest version of my resume in PDF format.")
    resume_file = Path(__file__).parent / "Rupesh_Resume.pdf"
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
        st.error("Resume PDF not found. Please make sure 'Rupesh_Resume.pdf' is in the same folder as the main.py file.")
