# PGVector LLM Memory Implementation

This implementation demonstrates how to create a memory system for Large Language Models (LLMs) using PostgreSQL's pgvector extension and Django. The system enables storing and retrieving contextually relevant conversation history using vector similarity search.

## Core Components

### VectorEntry Model

The implementation uses a custom Django model to store vector embeddings. But modify this model implementation as per your stack:

```python
class VectorEntry(models.Model):
    content = models.TextField()
    embedding = VectorField(dimensions=1536)  # OpenAI's embedding size
    conversation_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
```

Key features:
- Custom `VectorField` implementation using Django's `ArrayField`
- Indexed `conversation_id` for efficient queries
- Automatic timestamp tracking
- Supports OpenAI's 1536-dimensional embeddings

### Key Functions

#### Adding Memories

The `add_to_memory` function stores new conversation entries:

```python
def add_to_memory(conversation_id, content):
    embedding = create_embedding(content)
    VectorEntry.objects.create(
        conversation_id=conversation_id,
        content=content,
        embedding=embedding
    )
```

This function:
1. Generates an embedding for the input text
2. Creates a new VectorEntry with the content and its embedding
3. Associates it with a specific conversation

#### Retrieving Relevant Memories

The `get_relevant_memories` function retrieves contextually similar entries:

```python
def get_relevant_memories(conversation_id, query, limit=5):
    query_embedding = create_embedding(query)
    memories = VectorEntry.objects.filter(conversation_id=conversation_id)
    similarities = [(memory, cosine_similarity(memory.embedding, query_embedding)) 
                   for memory in memories]
    relevant_memories = sorted(similarities, key=lambda x: x[1], reverse=True)[:limit]
    return [memory.content for memory, _ in relevant_memories]
```

This function:
1. Creates an embedding for the query text
2. Retrieves all memories for the given conversation
3. Calculates cosine similarity between the query and stored embeddings
4. Returns the most relevant memories, sorted by similarity

## Features

1. **Embedding Generation**
   - Supports OpenAI's text-embedding-ada-002 model
   - Alternative implementation for Google's text-embedding-004 model
   - Error handling for embedding generation failures

2. **Vector Similarity Search**
   - Uses cosine similarity for comparing embeddings
   - Configurable limit for number of relevant memories to retrieve
   - Conversation-specific memory isolation

3. **Database Organization**
   - Efficient indexing for conversation lookups
   - Timestamp tracking for potential time-based features
   - PostgreSQL-compatible vector storage

## Setup Requirements

1. PostgreSQL with pgvector extension
2. Django with psycopg2
3. OpenAI API key configured in Django settings
4. Required Python packages:
   - openai
   - numpy
   - google.generativeai (optional, for alternative embedding generation)

## Usage Example

```python
# Store a new memory
add_to_memory(
    conversation_id=123,
    content="The user mentioned they prefer Python over JavaScript"
)

# Retrieve relevant memories
relevant_memories = get_relevant_memories(
    conversation_id=123,
    query="What programming languages were discussed?",
    limit=5
)
```

## Implementation Notes

1. The system uses cosine similarity for memory retrieval, which could be optimized using pgvector's native similarity search capabilities
2. Embedding generation is currently synchronous and could be moved to an asynchronous task queue for better performance
3. The implementation includes both OpenAI and Google AI embedding options, allowing for flexibility in embedding provider choice

## Future Improvements

1. Implement native pgvector similarity search
2. Add memory cleanup/pruning mechanisms
3. Implement caching for frequently accessed memories
4. Add support for batch memory operations
5. Implement memory age weighting in relevance calculations