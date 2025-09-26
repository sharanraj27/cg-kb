# embed_and_store.py
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
import pandas as pd
from neo4j import GraphDatabase

model = SentenceTransformer("all-MiniLM-L6-v2")  # small & fast

client = chromadb.Client()
collection = client.create_collection(name="careers")

# load careers
df = pd.read_csv("data/careers.csv")
for _, row in df.iterrows():
    txt = row['description']
    emb = model.encode(txt).tolist()
    collection.add(
        ids=[row['id']],
        embeddings=[emb],
        metadatas=[{"title": row['title']}],
        documents=[txt]
    )
print("Embeddings stored.")
