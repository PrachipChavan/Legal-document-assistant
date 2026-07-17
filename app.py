import os
import streamlit as st
from dotenv import load_dotenv
import utils
import prompts

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="LegalDoc Assistant - Smart Contract Analytics",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Styling for Legal Executive look
st.markdown("""
<style>
    /* Global styles and backgrounds */
    .stApp {
        background-color: #0B132B;
        color: #F4F6F9;
    }
    
    /* Top banner */
    .header-container {
        background: linear-gradient(135deg, #1C2541 0%, #0B132B 100%);
        padding: 2.5rem;
        border-radius: 12px;
        border-left: 5px solid #E0A96D;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .header-title {
        color: #FFFFFF;
        font-family: 'Outfit', 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .header-subtitle {
        color: #B2C1D4;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }

    /* Cards styling */
    .metric-card {
        background: rgba(28, 37, 65, 0.6);
        border: 1px solid rgba(224, 169, 109, 0.2);
        padding: 1.25rem;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, border 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(224, 169, 109, 0.5);
    }
    
    .metric-title {
        color: #E0A96D;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    
    .metric-value {
        color: #FFFFFF;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 0;
    }

    /* Risk Score meter styling */
    .risk-banner {
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.25);
    }
    
    .risk-low {
        background: linear-gradient(90deg, #1B4332 0%, #2D6A4F 100%);
        border: 1px solid #52B788;
        color: #D8F3DC;
    }
    
    .risk-medium {
        background: linear-gradient(90deg, #7F5539 0%, #9C6644 100%);
        border: 1px solid #DDB892;
        color: #EDE0D4;
    }
    
    .risk-high {
        background: linear-gradient(90deg, #641212 0%, #800f2f 100%);
        border: 1px solid #ff4d6d;
        color: #fff0f3;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1C2541;
        padding: 6px 12px;
        border-radius: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px;
        color: #B2C1D4;
        font-weight: 600;
        font-size: 1rem;
        border: none;
        padding: 0px 20px;
        transition: background-color 0.2s, color 0.2s;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #FFFFFF;
        background-color: rgba(255, 255, 255, 0.05);
    }

    .stTabs [aria-selected="true"] {
        background-color: #E0A96D !important;
        color: #0B132B !important;
    }
    
    /* Risk item card */
    .risk-card {
        background-color: #1C2541;
        border-left: 4px solid #E0A96D;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    .risk-card-high {
        border-left-color: #EF4444;
    }
    
    .risk-card-medium {
        border-left-color: #F59E0B;
    }
    
    .risk-card-low {
        border-left-color: #10B981;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        font-size: 0.75rem;
        font-weight: 700;
        border-radius: 4px;
        text-transform: uppercase;
        margin-right: 0.5rem;
    }
    
    .badge-high { background-color: #EF4444; color: #FFFFFF; }
    .badge-medium { background-color: #F59E0B; color: #1E293B; }
    .badge-low { background-color: #10B981; color: #FFFFFF; }

    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #64748B;
        font-size: 0.85rem;
        border-top: 1px solid #1E293B;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE SETUP -----------------
if "doc_text" not in st.session_state:
    st.session_state["doc_text"] = None
if "doc_name" not in st.session_state:
    st.session_state["doc_name"] = None
if "analysis_results" not in st.session_state:
    st.session_state["analysis_results"] = None
if "risk_results" not in st.session_state:
    st.session_state["risk_results"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "drafted_contract" not in st.session_state:
    st.session_state["drafted_contract"] = None

# Helper to clear session state when a new file is uploaded
def reset_document():
    st.session_state["doc_text"] = None
    st.session_state["doc_name"] = None
    st.session_state["analysis_results"] = None
    st.session_state["risk_results"] = None
    st.session_state["chat_history"] = []

# ----------------- SIDEBAR CONFIGURATION -----------------
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <h2 style="color: #E0A96D; margin: 0;">⚖️ LegalDoc</h2>
    <p style="color: #B2C1D4; font-size: 0.85rem; margin-top: 0.2rem;">AI-Powered Contract Intelligence</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.subheader("🔑 Credentials & Settings")

# 1. API Key Input
env_api_key = os.getenv("GROQ_API_KEY")
if env_api_key:
    api_key_placeholder = "Loaded from Env/dotenv"
    groq_api_key = env_api_key
else:
    api_key_placeholder = "Enter your Groq API Key..."
    groq_api_key = ""

user_api_key = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    placeholder=api_key_placeholder,
    help="Add your Groq API Key. Get one from console.groq.com"
)

# Prioritize user input over env variable if provided
if user_api_key:
    groq_api_key = user_api_key

# Validate API key exists
api_key_configured = bool(groq_api_key)

# 2. Model Selection
model_choice = st.sidebar.selectbox(
    "Select LLM Model",
    options=["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
    help="llama-3.3-70b-versatile is highly recommended for complex legal analysis and drafting."
)

st.sidebar.markdown("---")

# 3. Document Source Selection
st.sidebar.subheader("📄 Document Upload")
uploaded_file = st.sidebar.file_uploader(
    "Upload Contract (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"],
    on_change=reset_document
)

# Option to load sample contract
st.sidebar.markdown("<p style='text-align: center; color: #64748B;'>OR</p>", unsafe_allow_html=True)
if st.sidebar.button("💡 Load Sample Contract (Mutual NDA)"):
    st.session_state["doc_text"] = prompts.SAMPLE_CONTRACT
    st.session_state["doc_name"] = "Sample_Mutual_NDA.txt"
    st.session_state["analysis_results"] = None
    st.session_state["risk_results"] = None
    st.session_state["chat_history"] = []
    st.sidebar.success("Loaded Sample Mutual NDA!")

st.sidebar.markdown("---")
# Quick status indicators in sidebar
if st.session_state["doc_text"]:
    st.sidebar.info(f"Active Document:\n**{st.session_state['doc_name']}**")
    char_count = len(st.session_state["doc_text"])
    st.sidebar.text(f"Document Size: {char_count:,} chars")
    if st.sidebar.button("❌ Clear Document"):
        reset_document()
        st.rerun()

# ----------------- MAIN APP HEADER -----------------
st.markdown("""
<div class="header-container">
    <h1 class="header-title">⚖️ Legal Document Assistant</h1>
    <div class="header-subtitle">Analyze clauses, evaluate liability risks, chat with contracts, and draft templates instantly using Groq.</div>
</div>
""", unsafe_allow_html=True)

# Warn if API key is not configured
if not api_key_configured:
    st.warning("⚠️ **Groq API Key is missing!** Please enter your API key in the sidebar configuration to unlock the AI analytics features. You can still view and extract text, but AI analysis, risk scoring, Q&A, and drafting will be unavailable.")

# If file is uploaded but not processed yet
if uploaded_file and not st.session_state["doc_text"]:
    with st.spinner("Extracting text from uploaded file..."):
        try:
            extracted_text = utils.extract_text_from_file(uploaded_file)
            st.session_state["doc_text"] = extracted_text
            st.session_state["doc_name"] = uploaded_file.name
            st.success(f"Successfully extracted text from {uploaded_file.name}!")
            st.rerun()
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

# Define Tab layout
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Document Overview & Metadata", 
    "⚠️ Risk Assessment & Red Flags", 
    "💬 Grounded Q&A Chatbot", 
    "✍️ Interactive Template Drafting"
])

# ----------------- TAB 1: DOCUMENT OVERVIEW -----------------
with tab1:
    if st.session_state["doc_text"]:
        doc_text = st.session_state["doc_text"]
        
        # Trigger AI Analysis if not already done
        if st.session_state["analysis_results"] is None and api_key_configured:
            with st.spinner("Analyzing document structure & extracting metadata with Groq..."):
                try:
                    analysis = utils.analyze_document(doc_text, groq_api_key, model_choice)
                    st.session_state["analysis_results"] = analysis
                except Exception as e:
                    st.error(f"Error performing AI analysis: {str(e)}")
        
        analysis = st.session_state["analysis_results"]
        
        if analysis:
            # Metadata Grid
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Document Type</div>
                    <div class="metric-value">{analysis.get('document_type', 'N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                # Format parties display
                parties = analysis.get('parties', [])
                parties_str = ", ".join(parties) if isinstance(parties, list) else str(parties)
                if len(parties_str) > 25:
                    parties_str = parties_str[:22] + "..."
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Primary Parties</div>
                    <div class="metric-value" title="{', '.join(parties) if isinstance(parties, list) else ''}">{parties_str or 'N/A'}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Governing Law</div>
                    <div class="metric-value">{analysis.get('governing_law', 'N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Effective Date</div>
                    <div class="metric-value">{analysis.get('effective_date', 'N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Additional detail columns
            m_col1, m_col2 = st.columns([2, 1])
            with m_col1:
                st.subheader("📝 Executive Summary")
                st.write(analysis.get('summary', 'No summary generated.'))
                
                st.subheader("🔍 Key Clauses Extracted")
                clauses = analysis.get('key_clauses', [])
                if clauses:
                    for i, clause in enumerate(clauses):
                        with st.expander(f"🔑 {clause.get('clause_name', f'Clause {i+1}')}"):
                            st.markdown(f"**Summary:** {clause.get('summary', 'N/A')}")
                            if clause.get('clause_text_snippet'):
                                st.markdown(f"```text\n{clause.get('clause_text_snippet')}\n```")
                else:
                    st.info("No key clauses categorized in the overview.")
                    
            with m_col2:
                st.subheader("📌 Document Properties")
                st.markdown(f"""
                - **Dispute Jurisdiction:** {analysis.get('jurisdiction', 'Not specified')}
                - **Term/Expiration:** {analysis.get('expiration_date', 'Not specified')}
                - **Contract Parties Listed:**
                """)
                for party in parties:
                    st.markdown(f"  - 🏢 {party}")
                    
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("📄 View Raw Extracted Text"):
                    st.text_area("Raw Text Content", doc_text, height=350)
        else:
            st.info("AI Analysis is pending. Input your Groq API Key and select model to start. Meanwhile, you can inspect the raw text below.")
            st.text_area("Raw Text Content", doc_text, height=450)
            
    else:
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem;">
            <h3>No Contract Loaded</h3>
            <p style="color: #B2C1D4;">Please upload a PDF, DOCX, or TXT legal document using the sidebar, or click "Load Sample Contract" to test the app.</p>
            <div style="font-size: 5rem; margin-top: 1rem; color: #E0A96D;">📄</div>
        </div>
        """, unsafe_allow_html=True)

# ----------------- TAB 2: RISK ASSESSMENT -----------------
with tab2:
    if st.session_state["doc_text"]:
        doc_text = st.session_state["doc_text"]
        
        # Trigger AI Risk Assessment if not already done
        if st.session_state["risk_results"] is None and api_key_configured:
            with st.spinner("Conducting comprehensive risk analysis & vulnerability check..."):
                try:
                    risk_assessment = utils.assess_risks(doc_text, groq_api_key, model_choice)
                    st.session_state["risk_results"] = risk_assessment
                except Exception as e:
                    st.error(f"Error performing risk assessment: {str(e)}")
                    
        risk_results = st.session_state["risk_results"]
        
        if risk_results:
            # Overall Score Banner
            score = risk_results.get("overall_risk_score", 50)
            
            risk_class = "risk-low"
            risk_label = "LOW RISK"
            if score >= 70:
                risk_class = "risk-high"
                risk_label = "HIGH RISK / UNFAVORABLE"
            elif score >= 35:
                risk_class = "risk-medium"
                risk_label = "MEDIUM RISK"
                
            st.markdown(f"""
            <div class="risk-banner {risk_class}">
                <div style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px;">Overall Risk Rating</div>
                <div style="font-size: 2.8rem; font-weight: 800; margin: 0.5rem 0;">{score} / 100</div>
                <div style="font-size: 1.1rem; font-weight: 600;">{risk_label}</div>
            </div>
            """, unsafe_allow_html=True)
            
            r_col1, r_col2 = st.columns([1, 2])
            
            with r_col1:
                st.subheader("📊 Category Risk Levels")
                categories = risk_results.get("risk_categories", {})
                for cat_name, cat_lvl in categories.items():
                    lvl_color = "🟢" if cat_lvl.lower() == "low" else ("🟡" if cat_lvl.lower() == "medium" else "🔴")
                    st.markdown(f"""
                    **{cat_name}**
                    {lvl_color} {cat_lvl}
                    <hr style="margin: 0.5rem 0; border-color: rgba(255,255,255,0.05);">
                    """, unsafe_allow_html=True)
                    
                st.subheader("💡 General Assessment")
                st.write(risk_results.get("overall_assessment", "No general assessment provided."))
                
            with r_col2:
                st.subheader("🚩 Specific Red Flags & Clauses")
                risks = risk_results.get("risks", [])
                
                if risks:
                    for i, r in enumerate(risks):
                        lvl = r.get("risk_level", "Medium").lower()
                        border_class = "risk-card-low" if lvl == "low" else ("risk-card-medium" if lvl == "medium" else "risk-card-high")
                        badge_class = "badge-low" if lvl == "low" else ("badge-medium" if lvl == "medium" else "badge-high")
                        
                        st.markdown(f"""
                        <div class="risk-card {border_class}">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                                <strong style="font-size: 1.1rem; color: #FFFFFF;">⚠️ {r.get('clause_type', 'Clause Risk')}</strong>
                                <span class="badge {badge_class}">{lvl} Risk</span>
                            </div>
                            <div style="margin-bottom: 0.5rem;"><strong>Wording Risk:</strong> {r.get('description', 'N/A')}</div>
                            <div style="margin-bottom: 0.5rem; color: #B2C1D4;"><strong>Legal Implication:</strong> {r.get('implication', 'N/A')}</div>
                            <div style="background-color: rgba(224, 169, 109, 0.08); padding: 0.75rem; border-radius: 6px; border-left: 3px solid #E0A96D; margin-top: 0.5rem; color: #E0A96D;">
                                <strong>💡 Negotiation Mitigation:</strong> {r.get('mitigation_suggestion', 'N/A')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("🎉 No significant red flags or unfavorable clauses identified by the model!")
        else:
            st.info("AI Risk Analysis is pending. Input your Groq API Key and select model to start.")
    else:
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem;">
            <h3>No Contract Loaded</h3>
            <p style="color: #B2C1D4;">Please upload a contract or load the sample contract in the sidebar to review potential risks.</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------- TAB 3: GROUNDED Q&A CHATBOT -----------------
with tab3:
    if st.session_state["doc_text"]:
        st.subheader("💬 Ask Your Contract Anything")
        st.write("Pose questions regarding termination clauses, payment metrics, dispute resolutions, or liability caps. Answers are strictly grounded in the document text.")
        
        # Display chat messages
        for msg in st.session_state["chat_history"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        # User input query
        if not api_key_configured:
            st.info("Chat is disabled because Groq API Key is not configured.")
        else:
            if prompt := st.chat_input("e.g., What are the confidentiality exclusions?"):
                # Display user message
                with st.chat_message("user"):
                    st.write(prompt)
                
                # Append to history
                st.session_state["chat_history"].append({"role": "user", "content": prompt})
                
                # Call AI and display response
                with st.chat_message("assistant"):
                    with st.spinner("Searching document details..."):
                        try:
                            response = utils.answer_question(
                                document_text=st.session_state["doc_text"],
                                chat_history=st.session_state["chat_history"],
                                question=prompt,
                                api_key=groq_api_key,
                                model=model_choice
                            )
                            st.write(response)
                            st.session_state["chat_history"].append({"role": "assistant", "content": response})
                        except Exception as e:
                            st.error(f"Error in chat assistant: {str(e)}")
                            
            # Add a button to reset conversation
            if st.session_state["chat_history"]:
                st.button("🧹 Clear Chat History", on_click=lambda: st.session_state.update({"chat_history": []}))
    else:
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem;">
            <h3>No Contract Loaded</h3>
            <p style="color: #B2C1D4;">Please upload a contract or load the sample contract in the sidebar to initiate the chatbot.</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------- TAB 4: INTERACTIVE DRAFTING -----------------
with tab4:
    st.subheader("✍️ Draft Custom Agreements")
    st.write("Answer a few key questions to generate a tailored legal document draft using Groq's reasoning models.")
    
    # Form layout
    with st.form("drafting_form"):
        draft_col1, draft_col2 = st.columns(2)
        
        with draft_col1:
            contract_type = st.selectbox(
                "Agreement Type",
                options=[
                    "Mutual Nondisclosure Agreement (NDA)",
                    "Employment Agreement",
                    "Residential Lease Agreement",
                    "Freelance Services Contract / Independent Contractor Agreement"
                ]
            )
            effective_date = st.text_input("Effective Date", placeholder="e.g., October 15, 2026 or 'Upon execution'")
            governing_law = st.text_input("Governing Law Jurisdiction", placeholder="e.g., State of California, United Kingdom, etc.")
            
        with draft_col2:
            parties_details = st.text_area(
                "Parties Involved (Names, entity types, addresses)",
                placeholder="e.g.,\n1. Disclosing Party: TechStart Inc., a Delaware Corp.\n2. Receiving Party: DevConsult Ltd., a UK Private Limited Company.",
                height=110
            )
            key_terms = st.text_area(
                "Key Parameters & Custom Clauses",
                placeholder="NDA: Confidentiality term is 3 years, exceptions include public info.\nLease: Rent is $2,500/mo, deposit is $5,000, pets allowed.\nEmployment: Annual salary $120,000, 15 days PTO, full-time remote.",
                height=110
            )
            
        submit_draft = st.form_submit_button("🔨 Generate Legal Draft")
        
    if submit_draft:
        if not api_key_configured:
            st.error("Cannot generate draft. Groq API Key is not configured. Please input the key in the sidebar.")
        else:
            with st.spinner("Drafting contract with standard boilerplates using Groq..."):
                try:
                    draft = utils.draft_contract(
                        contract_type=contract_type,
                        effective_date=effective_date,
                        governing_law=governing_law,
                        parties_details=parties_details,
                        key_terms=key_terms,
                        api_key=groq_api_key,
                        model=model_choice
                    )
                    st.session_state["drafted_contract"] = draft
                    st.success("Agreement draft generated successfully!")
                except Exception as e:
                    st.error(f"Error drafting agreement: {str(e)}")
                    
    # Display and download generated draft
    if st.session_state["drafted_contract"]:
        st.subheader("📄 Generated Contract Draft")
        st.markdown("""
        > **Note:** This draft is automatically generated. Please review, customize, and consult legal counsel before signing.
        """)
        
        # Display the draft inside a nice code text area
        st.text_area("Contract Text", st.session_state["drafted_contract"], height=500)
        
        # Download buttons
        down_col1, down_col2 = st.columns(2)
        with down_col1:
            st.download_button(
                label="📥 Download as Markdown (.md)",
                data=st.session_state["drafted_contract"],
                file_name="drafted_agreement.md",
                mime="text/markdown"
            )
        with down_col2:
            st.download_button(
                label="📥 Download as Plain Text (.txt)",
                data=st.session_state["drafted_contract"],
                file_name="drafted_agreement.txt",
                mime="text/plain"
            )

# ----------------- FOOTER -----------------
st.markdown("""
<div class="footer">
    <p><strong>Disclaimer:</strong> This application is powered by Groq LLMs. It is designed to assist with document navigation and drafting. It does NOT constitute legal advice. Please consult with a qualified attorney for any legal matters.</p>
    <p>© 2026 LegalDoc Assistant. Crafted with Streamlit & Groq.</p>
</div>
""", unsafe_allow_html=True)
