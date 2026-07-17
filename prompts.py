# Expert-level system prompts for the Legal Document Assistant

SYSTEM_PROMPT = """You are a highly experienced corporate attorney and legal tech expert. 
Your role is to analyze legal documents, assess contract risks, answer legal questions grounded in provided texts, and draft standard agreements.
Provide accurate, professional, and structured analysis. 
Always maintain a balanced, objective tone and clarify that your outputs are for educational/informational purposes and do not constitute formal legal advice."""

ANALYSIS_PROMPT = """You are analyzing the text of a legal document. Extract the key metadata and summary in valid JSON format.
Strictly output ONLY valid JSON. Do not include markdown formatting (like ```json ... ```) or any pre/post text.

The JSON structure must match this template:
{
  "document_type": "Document Type (e.g., NDA, Lease Agreement, Employment Contract)",
  "parties": ["List of parties involved"],
  "effective_date": "Effective Date of the contract",
  "expiration_date": "Expiration Date or Term, if applicable",
  "governing_law": "Governing Law / State / Country",
  "jurisdiction": "Jurisdiction / Courts for disputes",
  "summary": "A concise executive summary of the agreement (2-3 paragraphs)",
  "key_clauses": [
    {
      "clause_name": "Clause Name (e.g., Confidentiality, Indemnification)",
      "clause_text_snippet": "A key short snippet of text from the contract corresponding to this clause",
      "summary": "A brief summary of what this clause details"
    }
  ]
}

Document text:
---
{document_text}
---
"""

RISK_PROMPT = """You are conducting a legal risk assessment of the provided contract. Identify potential red flags, liabilities, unilateral terms, or risky clauses.
Strictly output ONLY valid JSON. Do not include markdown formatting (like ```json ... ```) or any pre/post text.

The JSON structure must match this template:
{
  "overall_risk_score": 45,  // A score between 0 (safe/standard) and 100 (extreme risk/highly unfavorable)
  "overall_assessment": "Summary of the risk profile",
  "risk_categories": {
    "Liability & Indemnity": "Low/Medium/High",
    "Termination & Auto-renewals": "Low/Medium/High",
    "Intellectual Property": "Low/Medium/High",
    "Payment & Financials": "Low/Medium/High"
  },
  "risks": [
    {
      "clause_type": "Clause Type (e.g., Limitation of Liability)",
      "risk_level": "Low/Medium/High",
      "description": "Describe the specific unfavorable or risky wording in the contract.",
      "implication": "What is the real-world business or legal risk if this clause stands?",
      "mitigation_suggestion": "Alternative text or negotiation suggestion to propose to the counterparty."
    }
  ]
}

Document text:
---
{document_text}
---
"""

CHAT_PROMPT = """You are a legal Q&A assistant. The user will ask a question about the document provided below.
Your answer must be grounded strictly in the document text. If the answer cannot be determined or is not addressed in the contract, explicitly state that it is not found in the document. Do not hallucinate.
Provide references or quotes to support your answers.

Document text:
---
{document_text}
---

Conversation History:
{chat_history}

User Question: {question}
"""

DRAFTING_PROMPT = """Draft a standard legal contract based on the following specifications.
Use clear, professional legal drafting language. Include standard boilerplate clauses (Severability, Entire Agreement, Governing Law, Counterparts).
Structure the output using clean Markdown with clear headings.

Contract Details:
- Contract Type: {contract_type}
- Effective Date: {effective_date}
- Governing Law: {governing_law}
- Parties:
{parties_details}
- Key Terms & Parameters:
{key_terms}

Ensure the draft is complete and ready to customize, with placeholders like [insert name/date] clearly marked if any detail was not provided.
"""

SAMPLE_CONTRACT = """MUTUAL NONDISCLOSURE AGREEMENT

This Mutual Nondisclosure Agreement (the "Agreement") is entered into on October 15, 2025 (the "Effective Date"), by and between:
1. Apex Technologies Corp., a Delaware corporation with its principal place of business at 100 Innovation Way, Wilmington, DE 19801 ("Apex"); and
2. Summit Analytics LLC, a California limited liability company with its principal place of business at 500 Data Boulevard, San Francisco, CA 94105 ("Summit").

Apex and Summit may collectively be referred to as the "Parties" or individually as a "Party."

1. Purpose. The Parties wish to explore a potential business relationship concerning data analytics integration (the "Relationship"). In connection with the Relationship, each Party may disclose to the other Party certain proprietary and confidential information.

2. Confidential Information. "Confidential Information" means any information disclosed by one Party ("Disclosing Party") to the other Party ("Receiving Party") that is marked as confidential or should reasonably be understood to be confidential given the nature of the information. Confidential Information does not include information that: (a) is or becomes publicly known through no breach of this Agreement; (b) was already in the Receiving Party's possession without restriction prior to disclosure; (c) is independently developed by the Receiving Party without reference to the Disclosing Party's Confidential Information; or (d) is rightfully received from a third party without restriction.

3. Obligations of Confidentiality. The Receiving Party agrees:
(a) To hold the Disclosing Party's Confidential Information in strict confidence and take reasonable precautions to protect it (at least equal to the precautions it takes for its own confidential information, but in no event less than a reasonable degree of care);
(b) Not to use the Confidential Information except for the Purpose of the Relationship; and
(c) Not to disclose Confidential Information to any third parties, except to its employees, directors, or advisors who have a need to know and who are bound by confidentiality obligations at least as restrictive as those herein.

4. Term and Termination. This Agreement shall commence on the Effective Date and remain in effect for a period of one (1) year. Either Party may terminate this Agreement upon thirty (30) days written notice to the other Party. The Receiving Party's obligations with respect to Confidential Information disclosed during the term shall survive for a period of three (3) years from the date of disclosure.

5. Remedies. The Receiving Party acknowledges that any breach of this Agreement may cause irreparable harm for which monetary damages would be inadequate, and agrees that the Disclosing Party shall be entitled to seek injunctive relief in addition to any other remedies available at law.

6. Governing Law and Jurisdiction. This Agreement shall be governed by and construed in accordance with the laws of the State of New York, without regard to its conflict of law principles. Any legal action arising under this Agreement shall be brought exclusively in the state or federal courts located in New York County, New York.

7. Miscellaneous. This Agreement constitutes the entire agreement between the Parties regarding this subject matter and supersedes all prior discussions. This Agreement may only be amended in writing signed by both Parties. If any provision is found unenforceable, the remaining provisions shall continue in full force.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the Effective Date.

APEX TECHNOLOGIES CORP.
By: /s/ John Doe
Name: John Doe
Title: CEO

SUMMIT ANALYTICS LLC
By: /s/ Jane Smith
Name: Jane Smith
Title: Managing Director
"""

