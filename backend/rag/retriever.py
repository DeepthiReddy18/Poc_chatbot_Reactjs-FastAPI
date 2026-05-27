from rag.embeddings import generate_embedding
from rag.vectordb import collection

def retrieve_relavant_chunks(query, top_k=3):
    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings = [query_embedding],
        n_results = top_k        
    )

    return results["documents"][0]