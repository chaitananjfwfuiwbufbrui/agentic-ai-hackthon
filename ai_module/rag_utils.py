import logging
from typing import Optional, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vertex_init import init_vertex_ai
init_vertex_ai()
from vertexai import rag
from vertexai.generative_models import Tool

logger = logging.getLogger(__name__)

__all__ = [
    "create_rag_corpus",
    "create_rag_retrieval_tool",
    "run_rag_retrieval_query",
]

def create_rag_corpus(
    display_name: str,
    embedding_model: str = "publishers/google/models/text-embedding-005",
) -> rag.RagCorpus:
    """
    Create a new RAG corpus with the specified display name and embedding model.
    """
    logger.info(f"Creating RAG corpus: {display_name} using embedding model {embedding_model}")
    embedding_model_config = rag.RagEmbeddingModelConfig(
        vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
            publisher_model=embedding_model
        )
    )
    try:
        rag_corpus = rag.create_corpus(
            display_name=display_name,
            backend_config=rag.RagVectorDbConfig(
                rag_embedding_model_config=embedding_model_config
            ),
        )
        logger.info(f"RAG corpus created: {rag_corpus.name}")
        return rag_corpus
    except Exception as e:
        logger.error(f"Failed to create RAG corpus: {e}")
        raise

def create_rag_retrieval_tool(
    rag_corpus: rag.RagCorpus,
    top_k: int = 3,
    vector_distance_threshold: float = 0.5,
    filter_kwargs: Optional[dict] = None,
) -> Tool:
    """
    Create a VertexAI Tool for RAG retrieval.
    """
    logger.debug(f"Creating RAG retrieval tool for corpus: {rag_corpus.name}")
    filter_cfg = rag.Filter(vector_distance_threshold=vector_distance_threshold)
    if filter_kwargs:
        for key, value in filter_kwargs.items():
            setattr(filter_cfg, key, value)
    rag_retrieval_config = rag.RagRetrievalConfig(
        top_k=top_k, filter=filter_cfg
    )
    tool = Tool.from_retrieval(
        retrieval=rag.Retrieval(
            source=rag.VertexRagStore(
                rag_resources=[
                    rag.RagResource(rag_corpus=rag_corpus.name),
                ],
                rag_retrieval_config=rag_retrieval_config,
            ),
        )
    )
    logger.info("RAG retrieval tool created.")
    return tool

def run_rag_retrieval_query(
    rag_corpus: rag.RagCorpus,
    text: str,
    top_k: int = 3,
    vector_distance_threshold: float = 0.5,
    filter_kwargs: Optional[dict] = None,
) -> Any:
    """
    Run a RAG retrieval query for the provided text using the given corpus.
    Returns the query response.
    """
    logger.debug(
        f"Running RAG retrieval query on corpus '{rag_corpus.name}', top_k={top_k}, threshold={vector_distance_threshold}"
    )
    filter_cfg = rag.Filter(vector_distance_threshold=vector_distance_threshold)
    if filter_kwargs:
        for key, value in filter_kwargs.items():
            setattr(filter_cfg, key, value)
    rag_retrieval_config = rag.RagRetrievalConfig(
        top_k=top_k, filter=filter_cfg
    )
    try:
        response = rag.retrieval_query(
            rag_resources=[rag.RagResource(rag_corpus=rag_corpus.name)],
            text=text,
            rag_retrieval_config=rag_retrieval_config,
        )
        logger.debug("RAG retrieval query successful.")
        return response
    except Exception as e:
        logger.error(f"RAG retrieval query failed: {e}")
        raise

# Example usage:
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    corpus = create_rag_corpus("My Test Corpus")
    # tool = create_rag_retrieval_tool(corpus)
    rag.upload_file(
    corpus.name,
    path=r"E:\ai projects 2025\hackthon\docs\the-water-cycle-lesson-plans.pdf",
    display_name="waterclycle.pdf",
    )
    resp = run_rag_retrieval_query(corpus, "what is this pdf about?")
    print(resp)

    
