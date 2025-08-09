from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def build_index(clauses):
    embeddings = model.encode(clauses)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index, embeddings

def search(query, clauses, index):
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), k=5)
    return [clauses[i] for i in I[0]]

if __name__ == "__main__":
    clauses = [
        "Clause 3.2: Knee replacement is covered for individuals below 65 years.",
        "Clause 5.1: Coverage amount is ₹50,000 for orthopedic procedures.",
        "Clause 2.1: Only outpatient treatments are covered.",
        "Clause 4.3: Dental procedures are excluded.",
        "Clause 1.1: Policy is valid for individuals aged 18 to 65."
    ]
    index, _ = build_index(clauses)
    query = "Is a 62-year-old eligible for knee replacement?"
    results = search(query, clauses, index)
    print("\nTop Matching Clauses:")
    for clause in results:
        print(f"- {clause}")