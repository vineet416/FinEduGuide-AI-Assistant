import sys
from pinecone import Pinecone
from typing import List, Dict
from langchain_core.documents import Document
from euriai.langchain import EuriaiEmbeddings

from src.config import Config
from src.logger import logging
from src.exception import CustomException


class VectorDBClient:
    def __init__(self):
        try:
            logging.info("Initializing VectorDBClient")
            self.config = Config()
            # Initialize Pinecone
            self.pc = Pinecone(api_key=self.config.PINECONE_API_KEY.strip('"').strip("'"))
            self.index = self.pc.Index(self.config.PINECONE_INDEX_NAME.strip('"').strip("'"))
            # Initialize Embeddings
            self.embeddings_model = EuriaiEmbeddings(api_key=self.config.EURIAI_API_KEY.strip('"').strip("'"), model=self.config.OPENAI_EMBEDDING_MODEL.strip('"').strip("'"))
        except Exception as e:
            logging.error(f"Error initializing VectorDBClient: {str(e)}")
            raise CustomException(e, sys)
        

    def store_embeddings(self, documents: List[Document]) -> bool:
        try:
            logging.info(f"Storing {len(documents)} document embeddings to Pinecone.")
            # validate documents
            if not documents:
                raise ValueError("No documents provided for embedding storage.")
            # Generate embeddings
            texts = [doc.page_content for doc in documents]
            embeddings = self.embeddings_model.embed_documents(texts)
            # Prepare data for upsert
            to_upsert = []
            for idx, (doc, embedding) in enumerate(zip(documents, embeddings)):
                # Create unique ID for each chunk
                chunk_id = f"{documents[idx].metadata['source']}_{idx}"
                # Create record
                record = {
                    "id": chunk_id,
                    "values": embedding,
                    "metadata": documents[idx].metadata
                }
                to_upsert.append(record)
            # Upsert to Pinecone
            try:
                self.index.upsert(vectors=to_upsert)
                logging.info("Embeddings stored successfully.")
                return True
            except Exception as e:
                logging.error(f"Error upserting embeddings to Pinecone: {str(e)}")
                return False
        except Exception as e:
            logging.error(f"Error in store_embeddings: {str(e)}")
            raise CustomException(e, sys)
        
        
    def query_similar(self, query: str, top_k: int = 5) -> List[Dict]:
        try:
            logging.info(f"Querying similar documents for query: {query}")
            # Generate embedding for the query
            query_embedding = self.embeddings_model.embed_query(query)
            # Query Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            logging.info(f"Retrieved {len(results['matches'])} similar documents.")
            return results['matches']
        except Exception as e:
            logging.error(f"Error in query_similar: {str(e)}")
            raise CustomException(e, sys)