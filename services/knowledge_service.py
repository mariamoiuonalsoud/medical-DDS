from config.database import knowledge_db
from models.schemas import KnowledgeEntry

def search_knowledge(query, top_k=3):
    query_tokens = set(query.lower().split())
    results = []

    for doc in knowledge_db.find({}):
        score = _compute_similarity(query_tokens, doc)
        if score > 0:
            results.append(KnowledgeEntry(
                drug=doc["drug"],
                description=doc["description"],
                uses=doc.get("uses", []),
                score=score
            ))

    results.sort(key=lambda x: x.score, reverse=True)
    return results[:top_k]


def _compute_similarity(query_tokens, doc):
    doc_tokens = set()
    doc_tokens.add(doc["drug"].lower())
    doc_tokens.update(doc.get("keywords", []))
    doc_tokens.update(u.lower() for u in doc.get("uses", []))

    matches = sum(1 for t in query_tokens if len(t) > 2 and t in doc_tokens)
    return min(1.0, matches / max(len(query_tokens), 1))


def get_knowledge_stats():
    return knowledge_db.count_documents({})