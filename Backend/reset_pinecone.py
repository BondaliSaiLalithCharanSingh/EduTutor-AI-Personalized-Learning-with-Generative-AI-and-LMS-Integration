from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

load_dotenv()

# Load from .env
api_key = os.getenv("PINECONE_API_KEY")
env = os.getenv("PINECONE_ENVIRONMENT")
index_name = os.getenv("PINECONE_INDEX")

# Connect
pc = Pinecone(api_key=api_key)

# Step 1: Delete old index if exists
if index_name in pc.list_indexes().names():
    pc.delete_index(index_name)
    print(f"✅ Deleted old index '{index_name}'")

# Step 2: Create new index with correct dimension
pc.create_index(
    name=index_name,
    dimension=1024,  # ✅ Important fix!
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region=env)
)

print(f"✅ Created new index '{index_name}' with dimension 1024")