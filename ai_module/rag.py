import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vertex_init import init_vertex_ai
init_vertex_ai()

from vertexai import rag
from vertexai.generative_models import GenerativeModel, Tool


embedding_model_config = rag.RagEmbeddingModelConfig(
    vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
        publisher_model="publishers/google/models/text-embedding-005"
    )
)

rag_corpus = rag.create_corpus(
    display_name="test",
    backend_config=rag.RagVectorDbConfig(
        rag_embedding_model_config=embedding_model_config
    ),
)

rag.upload_file(
    rag_corpus.name,
    path="docs/the-water-cycle-lesson-plans.pdf",
    display_name="waterclycle.pdf",
    )
    
# Direct context retrieval
rag_retrieval_config = rag.RagRetrievalConfig(
    top_k=3,  # Optional
    filter=rag.Filter(vector_distance_threshold=0.5),  # Optional
)
response = rag.retrieval_query(
    rag_resources=[
        rag.RagResource(
            rag_corpus=rag_corpus.name,
            # Optional: supply IDs from `rag.list_files()`.
            # rag_file_ids=["rag-file-1", "rag-file-2", ...],
        )
    ],
    text="what is water cylce and why it is helpful?",
    rag_retrieval_config=rag_retrieval_config,
)
print(response)

# Enhance generation
# Create a RAG retrieval tool
rag_retrieval_tool = Tool.from_retrieval(
    retrieval=rag.Retrieval(
        source=rag.VertexRagStore(
            rag_resources=[
                rag.RagResource(
                    rag_corpus=rag_corpus.name,  # Currently only 1 corpus is allowed.
                    # Optional: supply IDs from `rag.list_files()`.
                    # rag_file_ids=["rag-file-1", "rag-file-2", ...],
                )
            ],
            rag_retrieval_config=rag_retrieval_config,
        ),
    )
)

# Create a Gemini model instance
rag_model = GenerativeModel(
    model_name="gemini-2.0-flash-001", tools=[rag_retrieval_tool]
)

# Generate response
response = rag_model.generate_content("what is water cylce and why it is helpful")
print(response.text)
# Example response:
#   RAG stands for Retrieval-Augmented Generation.
#   It's a technique used in AI to enhance the quality of responses
# ...