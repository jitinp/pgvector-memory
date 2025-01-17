import os 
from openai import OpenAI

from django.conf import settings
from .models import VectorEntry
import numpy as np

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def create_embedding(text):
    try:
        response = client.embeddings.create(input=text, model="text-embedding-ada-002")
        return response.data[0].embedding
    except Exception as err:
        print("Error in saving embedding", err)
        return None

def create_embedding__(text):
    try:
        print("Text for embedding", text)
        response = genai.embed_content(model="models/text-embedding-004", content=text)

        return response.embedding
    except Exception as err:
        print("Error in saving embedding", err)
        return None


def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def add_to_memory(conversation_id, content):
    embedding = create_embedding(content)
    VectorEntry.objects.create(
        conversation_id=conversation_id,
        content=content,
        embedding=embedding
    )


def get_relevant_memories(conversation_id, query, limit=5):
    query_embedding = create_embedding(query)

    memories = VectorEntry.objects.filter(conversation_id=conversation_id)

    similarities = [(memory, cosine_similarity(memory.embedding, query_embedding)) for memory in memories]
    relevant_memories = sorted(similarities, key=lambda x: x[1], reverse=True)[:limit]

    return [memory.content for memory, _ in relevant_memories]