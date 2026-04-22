from typing import List
from app.services.wiki_service import query_wikipedia


def rewrite_query(question: str) -> str:
    q = question.strip().lower()

    # simple rule-based query rewrite
    if q == "what is api":
        return "Application Programming Interface"
    if q == "what is rag":
        return "Retrieval-Augmented Generation"
    if q == "what is llm":
        return "Large language model"
    if q == "what is nlp":
        return "Natural language processing"

    return question.strip()


def synthesize_answer(question: str, wiki_results: List[dict]) -> str:
    if not wiki_results:
        return "No relevant Wikipedia information was found for your question."

    top = wiki_results[0]
    extract = top.get("extract", "").strip()

    if not extract:
        return "A relevant Wikipedia page was found, but no readable summary was returned."

    return extract


def answer_question(question: str):
    rewritten_query = rewrite_query(question)
    wiki_results = query_wikipedia(rewritten_query, limit=3)

    if not wiki_results:
        return {
            "answer": "No relevant Wikipedia information was found for your question.",
            "sources": [],
            "retrieved_chunks": []
        }

    answer_text = synthesize_answer(question, wiki_results)

    sources = []
    retrieved_chunks = []

    for item in wiki_results:
        title = item.get("title", "Unknown")
        url = item.get("url", "")
        source_label = f"{title} (Wikipedia)"
        if url:
            source_label = f"{source_label} - {url}"

        sources.append(source_label)
        retrieved_chunks.append({
            "source": title,
            "content": item.get("extract", "")
        })

    return {
        "answer": answer_text,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks
    }


def get_rag_status():
    return {
        "status": "ready",
        "error": None
    }