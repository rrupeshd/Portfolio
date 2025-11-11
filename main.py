# app.py  — Rupesh Portfolio (fixed Gemini check + stronger fallback)
import os
from pathlib import Path
import json
import streamlit as st

# Optional: Google Gemini (guarded imports)
try:
    import google.generativeai as genai
except Exception:
    genai = None

# Fallback NLP (cosine similarity)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ------------------------------
# PAGE SETUP & THEME
# ------------------------------
st.set_page_config(page_title="Rupesh Dubey | Digital Portfolio", page_icon="🤖", layout="wide")
st.markdown("""
<style>
  .stApp { background-color: #1a1a2e; color: #e0e0e0; }
  .block-container { padding-top: 2rem; }
  .hero-card { background-color: #162447; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25); border: 1px solid #4a4e69; }
  .hero-card h1, .hero-card h2, .hero-card p { color: #f2f2f2; }
  .stTabs [data-baseweb="tab-list"] { gap: 24px; }
  .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 4px 4px 0px 0px; gap: 8px; padding-top: 10px; padding-bottom: 10px; }
  .stTabs [aria-selected="true"] { background-color: #1f4068; }
  .mode-badge { display:inline-block; padding:.25rem .5rem; border-radius:8px; font-size:.85rem; margin-left:.5rem; }
  .mode-ok { background:#143d2d; color:#c2f0da; border:1px solid #2d7f5b; }
  .mode-fb { background:#5a3c00; color:#ffe2a8; border:1px solid #b57f0a; }
</style>
""", unsafe_allow_html=True)

# ------------------------------
# CONSTANTS & CONTEXT
# ------------------------------
APP_DIR = Path(__file__).parent
TRAINING_JSON = APP_DIR / "training_data.json"  # robust path (works local & on Streamlit Cloud)

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

# ------------------------------
# GEMINI AVAILABILITY (robust)
# ------------------------------
@st.cache_resource(show_spinner=False)
def init_gemini():
    """Return (model, available_bool) after a lightweight positive check."""
    api_key = None
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        api_key = os.environ.get("GOOGLE_API_KEY", None)

    if not api_key or genai is None:
        return None, False

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        # Low-cost ping; if this fails we consider Gemini unavailable
        _ = model.count_tokens("ping")
        return model, True
    except Exception:
        return None, False

gemini_model, GEMINI_OK = init_gemini()

# ------------------------------
# FALLBACK: Intent matcher (TF-IDF cosine)
# ------------------------------
@st.cache_resource(show_spinner=False)
def load_training():
    # If your JSON is missing, we still boot with a minimal default
    if TRAINING_JSON.exists():
        try:
            training = json.loads(TRAINING_JSON.read_text())
        except Exception:
            training = {}
    else:
        training = {}

    # Default intents if file empty/broken
    if not training:
        training = {
            "greetings": ["hello", "hi", "hey", "how are you", "good morning", "greetings"],
            "skills": ["what are his skills?", "skills", "technical abilities", "tech stack", "tools"],
            "skills_python": ["python skills", "does he know python?", "python"],
            "skills_dashboard": ["dashboard experience", "dashboards", "power bi", "tableau", "looker studio"],
            "experience_general": ["what is his work experience?", "career summary", "experience", "work history"],
            "education": ["education", "degree", "college", "university"],
            "contact": ["contact", "email", "phone", "reach out"],
            "achievements": ["achievements", "awards"]
        }

    # Build phrase -> label list
    phrases, labels = [], []
    for intent, examples in training.items():
        for p in examples:
            phrases.append(p.lower().strip())
            labels.append(intent)

    # Vectorizer tuned for very short queries (char n-grams handle typos & short words well)
    vect = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5))
    X = vect.fit_transform(phrases)

    # Pre-baked responses
    responses = {
        "greetings": "Hello! How can I help you learn more about Rupesh's career?",
        "skills": "Rupesh is skilled in Gen AI, Python (Pandas, NumPy, Scikit-Learn), R, SQL, Power BI, Looker Studio, Tableau, Excel VBA, and Azure Databricks.",
        "skills_python": "Yes—Rupesh is proficient in Python and common data science libraries like Pandas, NumPy, and Scikit-Learn.",
        "skills_dashboard": "He has extensive dashboarding experience with Power BI, Looker Studio, and Tableau (custom KPI views, campaign reporting, automation).",
        "experience_ugam": "Senior Data Analyst @ Ugam (2017–2022): BI reporting, warehousing, and automated data visualizations.",
        "experience_merkle": "Lead Analyst @ Merkle (2022–2023): custom dashboards and predictive models (>99% accuracy) for business KPIs.",
        "experience_annalect": "Lead – Marketing Science @ Annalect (2023–present): leads 6 analysts, THD campaign analytics, automated reporting.",
        "experience_tcs": "Data Analyst @ TCS (2016–2017): data extraction, cleaning, ad-hoc reporting, and performance dashboards.",
        "experience_general": "Rupesh has 9+ years across Annalect, Merkle, Ugam (Merkle), and TCS—covering analytics, dashboards, forecasting, and automation.",
        "education": "BCA (Computer Applications), North Maharashtra University, India.",
        "contact": "Email: rupeshdubey999@gmail.com • LinkedIn: linkedin.com/in/rupeshdubey9/",
        "achievements": "Highlights: ~70% cost savings via automation; ~99% revenue forecast accuracy; 16+ monthly performance awards; Golden Pyramid Award.",
        "where_based": "He is based in Vapi, Gujarat, India.",
        "yoe": "He has 9+ years of professional experience.",
        "projects": "Recent focus areas: THD creative-campaign analytics (BBDO NY), automated reporting pipelines, AI-assisted insight generation.",
        "fallback": "That’s outside of the provided resume details. Here’s what I can share that’s related: "
    }

    return (vect, X, phrases, labels, responses)

VECT, X_TRAIN, TRAIN_PHRASES, TRAIN_LABELS, RESPONSES = load_training()

def fallback_intent(query: str, min_sim: float = 0.18) -> str:
    """Return best intent (or 'fallback') based on cosine similarity."""
    q = (query or "").lower().strip()
    if not q:
        return "greetings"
    q_vec = VECT.transform([q])
    sims = cosine_similarity(q_vec, X_TRAIN)[0]

    # Aggregate by intent: take best score per intent
    best_by_intent = {}
    for sim, label in zip(sims, TRAIN_LABELS):
        if sim > best_by_intent.get(label, 0.0):
            best_by_intent[label] = sim

    # Pick top
    if not best_by_intent:
        return "fallback"
    intent, score = max(best_by_intent.items(), key=lambda kv: kv[1])
    return intent if score >= min_sim else "fallback"

def fallback_reply(query: str) -> str:
    intent = fallback_intent(query)
    if intent in RESPONSES:
        return RESPONSES[intent]
    return RESPONSES["fallback"]

# ------------------------------
# HERO
# ------------------------------
with st.container():
    st.markdown('<div class="hero-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        st.image('https://raw.githubusercontent.com/rrupeshd/Portfolio/refs/heads/main/Profile_Pic.png', width=250)
    with col2:
        st.title("Rupesh Dubey")
        st.subheader("Lead - Marketing Science")
        st.write("Data Science professional with 9+ years of AI-driven analytics, forecasting, and automation experience.")
        st.write("📍 Vapi, Gujarat, India")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# ------------------------------
# TABS
# ------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["🤖 RupeshBot", "🏢 Work Experience", "🔗 Projects & Links", "📄 Download Resume"])

# ------------------------------
# TAB 1: Chat (Gemini + Fallback)
# ------------------------------
with tab1:
    st.header("Meet RupeshBot - Quick answers from my resume")

    # Mode badge (truthful!)
    if GEMINI_OK:
        st.caption('Primary model: Google Gemini <span class="mode-badge mode-ok">AVAILABLE</span>', unsafe_allow_html=True)
    else:
        st.caption('Primary model: Google Gemini <span class="mode-badge mode-fb">**Notice:** The primary Gemini AI is currently unavailable. You are interacting with a local NLP-powered fallback bot. \n It can answer specific questions about skills and experience, but its understanding is limited. For the full AI experience, please contact Rupesh personally to enable it.</span>', unsafe_allow_html=True)

    # Start conversation
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you learn more about Rupesh's professional background today?"}]

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Ask about his dashboard experience..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Try Gemini if available, else fallback
        with st.chat_message("assistant"):
            answer = None
            if GEMINI_OK and gemini_model is not None:
                try:
                    sys_prompt = f"""
You are RupeshBot, answering ONLY from the resume block delimited by --- below.
Rules:
- Use only this context; no external knowledge.
- If a detail isn't in the resume, reply: "That specific detail isn't mentioned in Rupesh's resume, but here is what I can tell you about his related experience."
- "he"/"him" refers to Rupesh.
- Be concise and factual.

--- RESUME ---
{resume_context}
--- END RESUME ---

User: {prompt}
"""
                    resp = gemini_model.generate_content(sys_prompt)
                    answer = (resp.text or "").strip()
                except Exception:
                    # Flip local flag so next messages don't show the Gemini-available banner until refresh
                    answer = None

            if not answer:
                answer = fallback_reply(prompt)

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

# ------------------------------
# TAB 2–4 (unchanged, with safer file handling)
# ------------------------------
with tab2:
    st.header("Interactive Career Timeline")
    with st.expander("🏢 **Lead Analyst - Marketing Science | Annalect India**", expanded=True):
        st.markdown("**📅 August 2023 - Present**")
        st.markdown("""
- Utilized AI agents to deliver next-generation insights and deliverables.
- Led a team of six analysts, overseeing daily operations.
- Managed creative-campaign analytics for The Home Depot (BBDO NY) to inform optimization.
- Automated reporting pipelines to reduce manual effort.
        """)
    with st.expander("🏢 **Lead Analyst | Merkle**"):
        st.markdown("**📅 March 2022 - August 2023**")
        st.markdown("""
- Developed custom reports and dashboards to monitor key performance indicators.
- Built and deployed predictive analytics models to forecast future trends with 99%+ accuracy.
- Wrote and optimized scripts/queries for multi-source data extraction and analysis.
        """)
    with st.expander("🏢 **Senior Data Analyst | Ugam Solutions (A Merkle Company)**"):
        st.markdown("**📅 May 2017 - March 2022**")
        st.markdown("""
- Analyzed large datasets to uncover patterns, signals, and actionable insights.
- Utilized Business Objects, BI tools, and data-warehouse solutions for reporting.
- Automated data visualizations and crafted compelling stories to drive decisions.
        """)
    with st.expander("🏢 **Data Analyst | Tata Consultancy Services**"):
        st.markdown("**📅 January 2016 - May 2017**")
        st.markdown("""
- Extracted, cleaned, and analyzed project data to support client deliverables.
- Created ad-hoc reports and basic dashboards to track performance metrics.
        """)

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
        cimg = "https://s3.amazonaws.com/coursera_assets/meta_images/generated/CERTIFICATE_LANDING_PAGE/CERTIFICATE_LANDING_PAGE"
        st.image(f"{cimg}~0N5VQAGERT8F/CERTIFICATE_LANDING_PAGE~0N5VQAGERT8F.jpeg", caption="Python for Everybody")

    st.write("---")
    st.subheader("My Certifications Showcase")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    cimg = "https://s3.amazonaws.com/coursera_assets/meta_images/generated/CERTIFICATE_LANDING_PAGE/CERTIFICATE_LANDING_PAGE"
    with col1: st.image(f"{cimg}~7FLA7JPYU273/CERTIFICATE_LANDING_PAGE~7FLA7JPYU273.jpeg", caption="Python for Data Science, AI & Development")
    with col2: st.image(f"{cimg}~DZSE9773S8A2/CERTIFICATE_LANDING_PAGE~DZSE9773S8A2.jpeg", caption="SQL for Data Science")
    with col3: st.image(f"{cimg}~9CLH6FXWBB3G/CERTIFICATE_LANDING_PAGE~9CLH6FXWBB3G.jpeg", caption="Data Visualization with Tableau")
    with col4: st.image(f"{cimg}~NAJL962VEGM5/CERTIFICATE_LANDING_PAGE~NAJL962VEGM5.jpeg", caption="Basic Statistics")
    with col5: st.image(f"{cimg}~DFU5L2ABS8TD/CERTIFICATE_LANDING_PAGE~DFU5L2ABS8TD.jpeg", caption="Business Metrics for Data-Driven Companies")
    with col6: st.image(f"{cimg}~THW33CM8UBUH/CERTIFICATE_LANDING_PAGE~THW33CM8UBUH.jpeg", caption="Tools for Data Science")

with tab4:
    st.header("Download My Resume")
    st.write("Click the button below to download the latest version of my resume in PDF format.")
    resume_pdf = APP_DIR / "Rupesh_Resume.pdf"
    if resume_pdf.exists():
        with open(resume_pdf, "rb") as f:
            st.download_button("📄 Download Resume PDF", f.read(), file_name="Rupesh_Dubey_Resume.pdf", mime="application/pdf")
    else:
        st.error("Resume PDF not found. Place 'Rupesh_Resume.pdf' next to this app file.")
