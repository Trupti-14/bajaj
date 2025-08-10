from PyPDF2 import PdfReader

def extract_clauses(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    clauses = text.split("Clause")
    cleaned_clauses = [f"Clause{clause.strip()}" for clause in clauses if clause.strip()]
    return cleaned_clauses

if __name__ == "__main__":
    pdf_path = "policy.pdf"
    clauses = extract_clauses(pdf_path)
    for i, clause in enumerate(clauses[:5], 1):
        print(f"\nClause {i}:\n{clause}\n")