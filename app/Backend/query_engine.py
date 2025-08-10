from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from evaluate_decision import evaluate_decision
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
model = SentenceTransformer('all-MiniLM-L6-v2')

def process_query(query, clauses, source_doc):
    query_embedding = model.encode(query)
    clause_embeddings = model.encode(clauses)
    index = faiss.IndexFlatL2(query_embedding.shape[0])
    index.add(np.array(clause_embeddings))
    D, I = index.search(np.array([query_embedding]), k=min(5, len(clauses)))
    top_clauses = [clauses[i] for i in I[0]]
    decision = evaluate_decision(query, top_clauses)
    return {
        "query": query,
        "decision": decision["status"],
        "amount": decision["amount"],
        "justification": decision["justification"],
        "source_document": source_doc,
        "matched_clauses": top_clauses
    }