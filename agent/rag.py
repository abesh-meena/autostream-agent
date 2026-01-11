"""
Retrieval-Augmented Generation (RAG) module for AutoStream Agent
Handles knowledge retrieval and context-aware responses
"""

from typing import List, Dict, Optional
import json
import os
from pathlib import Path

class KnowledgeBase:
    """Manages the knowledge base for RAG operations"""
    
    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.knowledge_data = {}
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load knowledge base from JSON file"""
        try:
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                self.knowledge_data = json.load(f)
        except FileNotFoundError:
            print(f"Knowledge base file not found: {self.knowledge_base_path}")
            self.knowledge_data = {}
        except json.JSONDecodeError as e:
            print(f"Error parsing knowledge base: {e}")
            self.knowledge_data = {}
    
    def retrieve_relevant_info(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Retrieve relevant information based on query
        
        Args:
            query: User query string
            max_results: Maximum number of results to return
            
        Returns:
            List of relevant knowledge items
        """
        query_lower = query.lower()
        relevant_items = []
        
        # Enhanced keyword matching for pricing and plans
        for key, value in self.knowledge_data.items():
            if isinstance(value, dict):
                # Handle nested structures like pricing and policies
                for sub_key, sub_value in value.items():
                    if self._is_relevant_to_query(query_lower, key, sub_key, sub_value):
                        relevant_items.append({
                            "key": f"{key}.{sub_key}",
                            "content": sub_value if isinstance(sub_value, str) else json.dumps(sub_value),
                            "full_data": sub_value,
                            "relevance_score": self._calculate_relevance(query_lower, key, sub_key, sub_value)
                        })
            elif isinstance(value, str):
                if self._is_relevant_to_query(query_lower, key, None, value):
                    relevant_items.append({
                        "key": key,
                        "content": value,
                        "full_data": value,
                        "relevance_score": self._calculate_relevance(query_lower, key, None, value)
                    })
        
        # Sort by relevance and return top results
        relevant_items.sort(key=lambda x: x["relevance_score"], reverse=True)
        return relevant_items[:max_results]
    
    def _is_relevant_to_query(self, query: str, main_key: str, sub_key: str, value) -> bool:
        """
        Check if content is relevant to the query
        
        Args:
            query: Lowercase query string
            main_key: Main key in JSON (e.g., 'pricing', 'policies')
            sub_key: Sub key in JSON (e.g., 'Basic', 'Pro', 'refund')
            value: The actual value
            
        Returns:
            Boolean indicating relevance
        """
        # Check if query mentions pricing-related terms
        pricing_keywords = ['price', 'pricing', 'cost', 'plan', 'plans', 'basic', 'pro']
        policy_keywords = ['refund', 'support', 'policy', 'policies']
        
        # Check main key relevance
        if any(keyword in query for keyword in pricing_keywords) and main_key == 'pricing':
            return True
        
        if any(keyword in query for keyword in policy_keywords) and main_key == 'policies':
            return True
        
        # Check sub key relevance (for specific plans)
        if sub_key:
            sub_key_lower = sub_key.lower()
            if sub_key_lower in query or any(word in sub_key_lower for word in query.split()):
                return True
        
        # Check value content
        if isinstance(value, str) and any(word in value.lower() for word in query.split()):
            return True
        
        return False
    
    def _calculate_relevance(self, query: str, main_key: str, sub_key: str, value) -> float:
        """
        Calculate relevance score between query and content
        
        Args:
            query: Query string
            main_key: Main key in JSON
            sub_key: Sub key in JSON
            value: The actual value
            
        Returns:
            Relevance score (0-1)
        """
        score = 0.0
        query_words = set(query.split())
        
        if not query_words:
            return 0.0
        
        # High relevance for exact plan matches
        if sub_key:
            sub_key_lower = sub_key.lower()
            if sub_key_lower in query:
                score += 0.8
            for word in query_words:
                if word in sub_key_lower:
                    score += 0.3
        
        # Medium relevance for main category matches
        main_key_lower = main_key.lower()
        if main_key_lower in query:
            score += 0.5
        
        # Content relevance
        if isinstance(value, str):
            content_lower = value.lower()
            for word in query_words:
                if word in content_lower:
                    score += 0.2
        
        return min(score, 1.0)

class RAGEngine:
    """Main RAG engine for generating context-aware responses"""
    
    def __init__(self, knowledge_base_path: str):
        self.knowledge_base = KnowledgeBase(knowledge_base_path)
    
    def generate_response(self, query: str, intent: Optional[str] = None) -> Dict:
        """
        Generate a response using retrieved knowledge
        
        Args:
            query: User query
            intent: Optional intent classification
            
        Returns:
            Dictionary containing response and context
        """
        # Retrieve relevant information
        relevant_info = self.knowledge_base.retrieve_relevant_info(query)
        
        # Build context
        context = self._build_context(relevant_info, intent)
        
        # Generate response using ONLY retrieved knowledge
        response = self._generate_llm_response(query, context, relevant_info)
        
        return {
            "response": response,
            "context": context,
            "sources": [item["key"] for item in relevant_info],
            "data_used": {item["key"]: item["full_data"] for item in relevant_info}
        }
    
    def _build_context(self, relevant_info: List[Dict], intent: Optional[str]) -> str:
        """Build context string from relevant information"""
        context_parts = []
        
        if intent:
            context_parts.append(f"Intent: {intent}")
        
        for item in relevant_info:
            context_parts.append(f"{item['key']}: {item['content']}")
        
        return "\n".join(context_parts)
    
    def _generate_llm_response(self, query: str, context: str, relevant_info: List[Dict]) -> str:
        """
        Generate response using ONLY retrieved knowledge to prevent hallucination
        
        Args:
            query: User query
            context: Retrieved context
            relevant_info: List of relevant knowledge items
            
        Returns:
            Generated response based strictly on knowledge base
        """
        if not relevant_info:
            return f"I don't have specific information about '{query}' in my knowledge base."
        
        # Extract data from knowledge base
        response_parts = []
        
        for item in relevant_info:
            key = item['key']
            data = item['full_data']
            
            # Format response based on the type of information
            if 'pricing' in key:
                if '.' in key:
                    plan_name = key.split('.')[1]
                    response_parts.append(self._format_plan_info(plan_name, data))
                else:
                    response_parts.append(f"Pricing information: {json.dumps(data, indent=2)}")
            
            elif 'policies' in key:
                if '.' in key:
                    policy_type = key.split('.')[1]
                    response_parts.append(f"{policy_type.title()}: {data}")
                else:
                    response_parts.append(f"Policies: {json.dumps(data, indent=2)}")
            
            else:
                response_parts.append(f"{key}: {data}")
        
        # Combine response parts
        if len(response_parts) == 1:
            return response_parts[0]
        else:
            return "\n\n".join(response_parts)
    
    def _format_plan_info(self, plan_name: str, plan_data: Dict) -> str:
        """
        Format plan information in a readable way
        
        Args:
            plan_name: Name of the plan (Basic/Pro)
            plan_data: Plan details dictionary
            
        Returns:
            Formatted string with plan information
        """
        if not isinstance(plan_data, dict):
            return f"{plan_name}: {plan_data}"
        
        parts = [f"{plan_name} Plan:"]
        
        # Add price
        if 'price' in plan_data:
            parts.append(f"Price: {plan_data['price']}")
        
        # Add videos
        if 'videos' in plan_data:
            parts.append(f"Videos: {plan_data['videos']}")
        
        # Add resolution
        if 'resolution' in plan_data:
            parts.append(f"Resolution: {plan_data['resolution']}")
        
        # Add features
        if 'features' in plan_data:
            features = plan_data['features']
            if isinstance(features, list):
                parts.append(f"Features: {', '.join(features)}")
            else:
                parts.append(f"Features: {features}")
        
        return "\n".join(parts)
