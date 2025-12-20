import sys
from typing import List, Dict

from src.components.vector_db_client import VectorDBClient
from src.utils.prompt_templates import explanation_prompt_template, quiz_prompt_template, summary_prompt_template
from src.logger import logging
from src.exception import CustomException



class RAGEngine:
    def __init__(self):
        try:
            logging.info("Initializing RAGEngine")
            self.vector_db_client = VectorDBClient()
            logging.info("RAGEngine initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing RAGEngine: {str(e)}")
            raise CustomException(e, sys)
        

    # format context helper function
    def _format_context(self, similar_results: List[Dict]) -> str:
        try:
            logging.info("Formatting context from similar results")
            context = ""
            for result in similar_results:
                metadata = result['metadata']
                score  = result.get('score', 0)
                chunk_text = metadata.get('text', '')
                source = metadata.get('source', 'Unknown Source')
                chunk_index = metadata.get('chunk_index', 'N/A')
                context += f"Source: {source}, Chunk Index: {chunk_index}, Similarity Score: {score:.4f}\n{chunk_text}\n\n"
            logging.info("Context formatted successfully")
            return context.strip()
        except Exception as e:
            logging.error(f"Error formatting context: {str(e)}")
            raise CustomException(e, sys)
        

    ## retrieve context
    def retrieve_context(self, user_query: str, top_k: int = 5, relevance_threshold: float = 0.5) -> str:
        try:
            logging.info(f"Retrieving context for user query: {user_query}")
            similar_results = self.vector_db_client.query_similar(user_query, top_k=top_k)
            # Filter results based on relevance threshold
            filtered_results = [res for res in similar_results if res['score'] >= relevance_threshold]
            # Handle case with no relevant documents
            if not filtered_results:
                logging.info("No relevant documents found above the relevance threshold")
                return "No relevant documents found for the query."
            else:
                # Sort filtered results by score descending
                sorted_results = sorted(filtered_results, key=lambda x: x['score'], reverse=True)
                # Format context
                context = self._format_context(sorted_results)
                logging.info("Context retrieved and formatted successfully")
                return context 
        except Exception as e:
            logging.error(f"Error retrieving context: {str(e)}")
            raise CustomException(e, sys)
        

    # Assemble prompt
    def assemble_prompt(self, context: str, user_query: str, content_type: str = "Explain") -> str:
        try:
            logging.info(f"Assembling prompt for content type: {content_type}")
            if content_type.strip().lower() == "explain":
                prompt = explanation_prompt_template(context, user_query)
            elif content_type.strip().lower() == "quiz":
                prompt = quiz_prompt_template(context, user_query)
            elif content_type.strip().lower() == "summary":
                prompt = summary_prompt_template(context, user_query)
            else:
                raise ValueError(f"Unsupported content type: {content_type}. Must be 'Explain', 'Quiz', or 'Summary'.")
            logging.info("Prompt assembled successfully")
            return prompt
        except Exception as e:
            logging.error(f"Error assembling prompt: {str(e)}")
            raise CustomException(e, sys)