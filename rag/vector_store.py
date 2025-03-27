import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Any, Tuple

class VectorStore:
    """
    Vector store implementation using FAISS for efficient similarity search
    """
    
    def __init__(self, dimension: int = 384):
        """
        Initialize the vector store with a specific embedding dimension
        
        Args:
            dimension: The dimension of the embedding vectors
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance
        self.metadata = []  # Store metadata alongside vectors
        
    def add_items(self, embeddings: np.ndarray, metadata_list: List[Dict[str, Any]]) -> None:
        """
        Add items (vectors and their metadata) to the index
        
        Args:
            embeddings: Numpy array of embeddings with shape (n, dimension)
            metadata_list: List of metadata dictionaries corresponding to each embedding
        """
        if len(embeddings) != len(metadata_list):
            raise ValueError("Number of embeddings must match number of metadata items")
            
        # Add vectors to the index
        self.index.add(embeddings)
        
        # Store metadata
        self.metadata.extend(metadata_list)
    
    def search(self, query_embedding: np.ndarray, k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        """
        Search for the k most similar items to the query embedding
        
        Args:
            query_embedding: The query embedding vector
            k: Number of results to return
            
        Returns:
            List of tuples containing (metadata, distance)
        """
        # Ensure query is in the right shape
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
            
        # Search the index
        distances, indices = self.index.search(query_embedding, k)
        
        # Get the corresponding metadata
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):  # -1 means no result found
                results.append((self.metadata[idx], float(distances[0][i])))
                
        return results
    
    def save(self, directory: str) -> None:
        """
        Save the vector store to disk
        
        Args:
            directory: Directory to save the vector store
        """
        os.makedirs(directory, exist_ok=True)
        
        # Save the FAISS index
        faiss.write_index(self.index, os.path.join(directory, "index.faiss"))
        
        # Save the metadata
        with open(os.path.join(directory, "metadata.pkl"), "wb") as f:
            pickle.dump(self.metadata, f)
            
        # Save the dimension
        with open(os.path.join(directory, "config.pkl"), "wb") as f:
            pickle.dump({"dimension": self.dimension}, f)
    
    @classmethod
    def load(cls, directory: str) -> 'VectorStore':
        """
        Load a vector store from disk
        
        Args:
            directory: Directory containing the saved vector store
            
        Returns:
            Loaded VectorStore instance
        """
        # Load the dimension
        with open(os.path.join(directory, "config.pkl"), "rb") as f:
            config = pickle.load(f)
            
        # Create a new instance
        vector_store = cls(dimension=config["dimension"])
        
        # Load the FAISS index
        vector_store.index = faiss.read_index(os.path.join(directory, "index.faiss"))
        
        # Load the metadata
        with open(os.path.join(directory, "metadata.pkl"), "rb") as f:
            vector_store.metadata = pickle.load(f)
            
        return vector_store
