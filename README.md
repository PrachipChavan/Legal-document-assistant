# ⚖️ LegalDoc Assistant: AI-Powered Contract Intelligence

LegalDoc Assistant is a premium, state-of-the-art web application built with **Python**, **Streamlit**, and **Groq** to assist legal professionals, developers, and businesses in understanding, analyzing, and drafting contracts. By leveraging the ultra-fast reasoning capabilities of models like `llama-3.3-70b-versatile`, the assistant accelerates contract reviews, identifies hidden liabilities, and drafts custom agreements.

---

## 🌟 Key Features

### 1. 📋 Document Overview & Metadata Extraction
- **Smart Parsing:** Supports `.pdf`, `.docx`, and `.txt` files.
- **Auto-Metadata Extraction:** Automatically identifies document types, primary parties, effective dates, governing laws, and dispute jurisdictions.
- **Executive Summaries:** Provides a clear, high-level summary of the contract text.
- **Clause Inspector:** Extracts and organizes key clauses (e.g., Confidentiality, Indemnification) into readable summaries with exact snippets.

### 2. ⚠️ Risk Assessment & Red Flags
- **Overall Risk Scoring:** Evaluates documents on a scale of 0 (standard/safe) to 100 (extreme risk/unfavorable).
- **Vulnerability Indicators:** Rates individual categories (Liability, Termination, IP, Payment) as Low, Medium, or High risk.
- **Actionable Mitigations:** Highlights specific unfavourable clauses, explains their legal implications, and suggests alternative wording for negotiations.

### 3. 💬 Grounded Q&A Chatbot
- **Context-Locked Answers:** Answer queries (e.g., *"What is the notice period for termination?"*) grounded strictly in the document text to eliminate hallucinations.
- **Source Referencing:** Integrates citations and references directly from the contract terms.

### 4. ✍️ Custom Document Drafting
- **Interactive Forms:** Input key parameters (Parties, effective dates, governing law, custom parameters).
- **Tailored Outputs:** Automatically generates professional agreements (NDAs, Leases, Employment, Service Contracts) with standard boilerplate clauses.
- **Formats:** Download drafted agreements as Markdown (`.md`) or Plain Text (`.txt`).

---

## 🛠️ Technology Stack

- **Frontend:** Streamlit (Custom styled with a premium Dark "Legal Executive" theme)
- **AI Engine:** Groq API (Defaulting to `llama-3.3-70b-versatile` & `llama-3.1-8b-instant`)
- **Document Extractors:** `pypdf` (PDF reader) & `python-docx` (Word document parser)
- **Configuration:** `python-dotenv` (Local credential loading)

---

## 📂 Project Directory Structure

```text
legal_document_assistant/
│
├── app.py              # Main Streamlit frontend and UI navigation
├── utils.py            # Text extraction and Groq API call wrappers
├── prompts.py          # Isolated expert prompt templates & sample NDA text
├── requirements.txt    # Python dependencies
├── .env                # API credential file (ignored in git)
│
├── samples/            # Pre-loaded documents for quick testing
│   ├── sample_mutual_nda.txt
│   └── sample_employment_agreement.docx
│
└── README.md           # Project documentation
```

---

## 🚀 Installation & Local Setup

### Prerequisites
Make sure you have **Python 3.10+** installed on your system.

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/legal-document-assistant.git
cd legal-document-assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Your Groq API Key
1. Get an API key from the [Groq Console](https://console.groq.com/).
2. Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your-actual-groq-api-key-here
   ```
   *(Alternatively, you can input the API key directly in the sidebar input field when the app is running.)*

### 4. Run the Application
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser to start analyzing documents!

---

## ⚖️ Disclaimer

**This software is an AI prototype and does not constitute formal legal advice.** The analysis, risk scores, and generated drafts are for educational and informational purposes only. Always consult a qualified attorney before signing or executing any legal document.

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
