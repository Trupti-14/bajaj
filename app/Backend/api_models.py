from pydantic import BaseModel
from typing import List, Optional

class QueryResponse(BaseModel):
    query: str
    decision: str
    amount: Optional[float]
    justification: str
    source_document: str
    matched_clauses: List[str]
    