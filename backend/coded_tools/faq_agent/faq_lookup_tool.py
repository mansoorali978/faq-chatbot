"""
FaqLookupTool — a Neuro-SAN CodedTool that searches the FAQ JSON dataset.
"""
import json
import os
from typing import Any, Dict
from neuro_san.interfaces.coded_tool import CodedTool


class FaqLookupTool(CodedTool):
    """
    Searches a static FAQ JSON file for answers matching the user's query.
    Uses simple keyword matching — can be upgraded to vector search / RAG.
    """

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_dir, "..", "..", "data", "faq.json")
        data_path = os.path.normpath(data_path)
        
        with open(data_path, "r") as f:
            self.faq_data = json.load(f)

    async def async_invoke(
        self, args: Dict[str, Any], sly_data: Dict[str, Any]
    ) -> Any:
        query = args.get("query", "").lower()
        if not query:
            return "No query provided."

        results = []
        # Split query into individual words for matching
        query_words = set(query.split())
        
        # Remove common stop words that add noise
        stop_words = {"how", "do", "i", "can", "what", "is", "are", "the", 
                    "a", "an", "my", "to", "for", "in", "of", "and", "or"}
        query_words = query_words - stop_words

        for item in self.faq_data:
            question_words = set(item["question"].lower().split()) - stop_words
            answer_words = set(item["answer"].lower().split()) - stop_words
            category_words = set(item["category"].lower().split()) - stop_words

            all_words = question_words | answer_words | category_words
            score = len(query_words & all_words)

            if score > 0:
                results.append((score, item))

        if not results:
            # Return ALL FAQ entries so agent can still try to help
            output = "No exact match found. Here are all available FAQ topics:\n\n"
            for item in self.faq_data:
                output += f"Category: {item['category']}\n"
                output += f"Q: {item['question']}\n"
                output += f"A: {item['answer']}\n\n"
            return output

        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:3]

        output = "Relevant FAQ entries found:\n\n"
        for _, item in top_results:
            output += f"Category: {item['category']}\n"
            output += f"Q: {item['question']}\n"
            output += f"A: {item['answer']}\n\n"

        return output