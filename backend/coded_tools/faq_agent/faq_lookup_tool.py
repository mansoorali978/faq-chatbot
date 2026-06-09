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
        # Load FAQ data once at init
        data_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "faq.json"
        )
        with open(data_path, "r") as f:
            self.faq_data = json.load(f)

    async def async_invoke(
        self, args: Dict[str, Any], sly_data: Dict[str, Any]
    ) -> Any:
        """
        args["query"]: the search string from the LLM.
        Returns the best matching FAQ entries as a formatted string.
        """
        query = args.get("query", "").lower()
        if not query:
            return "No query provided."

        results = []
        query_words = set(query.split())

        for item in self.faq_data:
            # Score each FAQ item by keyword overlap
            question_words = set(item["question"].lower().split())
            answer_words = set(item["answer"].lower().split())
            category_words = set(item["category"].lower().split())

            all_words = question_words | answer_words | category_words
            score = len(query_words & all_words)

            if score > 0:
                results.append((score, item))

        if not results:
            return (
                "No matching FAQ found for this query. "
                "Please advise the user to contact customer support at 1860-266-7766."
            )

        # Sort by score descending, return top 3
        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:3]

        output = "Relevant FAQ entries found:\n\n"
        for _, item in top_results:
            output += f"Category: {item['category']}\n"
            output += f"Q: {item['question']}\n"
            output += f"A: {item['answer']}\n\n"

        return output