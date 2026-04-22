from app.services.rag_service import build_and_save_vector_store

if __name__ == "__main__":
    build_and_save_vector_store()
    print("RAG cache built successfully.")