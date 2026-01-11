"""
Debug RAG response to see what's happening
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'agent'))

from agent.rag import RAGEngine

def debug_rag():
    """Debug RAG response"""
    
    rag_engine = RAGEngine("knowledge_base/autostream_data.json")
    
    test_query = "Tell me about Pro plan"
    
    print("🔍 Debugging RAG Response")
    print("=" * 40)
    print(f"📝 Query: '{test_query}'")
    print("-" * 40)
    
    result = rag_engine.generate_response(test_query, "INQUIRY")
    
    print(f"🤖 Response: {result['response']}")
    print(f"📚 Context: {result['context']}")
    print(f"📄 Sources: {result['sources']}")
    print(f"📊 Data used: {result.get('data_used', 'N/A')}")

if __name__ == "__main__":
    debug_rag()
