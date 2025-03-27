import numpy as np
from typing import List, Dict, Any, Union
from sentence_transformers import SentenceTransformer
import os
from app.function_registry.functions import function_metadata
from app.rag.vector_store import VectorStore

class EmbeddingGenerator:
    """
    Class for generating embeddings using Sentence Transformers
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding generator
        
        Args:
            model_name: Name of the sentence-transformers model to use
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.vector_store = None
        
    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for the given texts
        
        Args:
            texts: A string or list of strings to encode
            
        Returns:
            Numpy array of embeddings
        """
        return self.model.encode(texts, convert_to_numpy=True)
    
    def initialize_vector_store(self, save_dir: str = "vector_db") -> VectorStore:
        """
        Initialize the vector store with function metadata
        
        Args:
            save_dir: Directory to save the vector store
            
        Returns:
            Initialized VectorStore
        """
        # Check if vector store already exists
        if os.path.exists(save_dir) and os.path.isfile(os.path.join(save_dir, "index.faiss")):
            print(f"Loading existing vector store from {save_dir}")
            self.vector_store = VectorStore.load(save_dir)
            return self.vector_store
        
        # Create function descriptions for embedding
        texts = []
        for func in function_metadata:
            # Create rich description combining name, description, and keywords
            description = f"{func['name']}: {func['description']}. Keywords: {', '.join(func['keywords'])}"
            texts.append(description)
            
        # Generate embeddings
        embeddings = self.encode(texts)
        
        # Create and populate vector store
        self.vector_store = VectorStore(dimension=embeddings.shape[1])
        self.vector_store.add_items(embeddings, function_metadata)
        
        # Save the vector store
        os.makedirs(save_dir, exist_ok=True)
        self.vector_store.save(save_dir)
        
        return self.vector_store
    
    def find_matching_function(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Find the most matching functions for a given query
        
        Args:
            query: User query
            k: Number of matches to return
            
        Returns:
            List of matching function metadata sorted by relevance
        """
        if self.vector_store is None:
            self.initialize_vector_store()
            
        # Generate embedding for the query
        query_embedding = self.encode(query)
        
        # Search for matches
        matches = self.vector_store.search(query_embedding, k=k)
        
        # Return the metadata only
        return [metadata for metadata, _ in matches]

# Singleton instance for reuse
embedding_generator = None

def get_embedding_generator(model_name: str = "all-MiniLM-L6-v2") -> EmbeddingGenerator:
    """
    Get or create a singleton EmbeddingGenerator instance
    
    Args:
        model_name: Name of the sentence-transformers model to use
        
    Returns:
        EmbeddingGenerator instance
    """
    global embedding_generator
    
    if embedding_generator is None:
        embedding_generator = EmbeddingGenerator(model_name)
        
    return embedding_generator
