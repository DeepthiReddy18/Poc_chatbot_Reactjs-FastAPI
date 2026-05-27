import chromadb
from rag.embeddings import generate_embedding
import uuid

client = chromadb.PersistentClient(path = "./chroma_db")
collection = client.get_or_create_collection(
    name = "hr_policies"
)

def store_chunks(chunks, source):
    for chunk in chunks:
        embedding = generate_embedding(chunk)

        collection.add(
            ids = [str(uuid.uuid4())],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{
                "source":source
            }]            
        )

